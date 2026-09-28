$ErrorActionPreference = 'Stop'
$root = "E:\AIGC\课件\12小说"
$port = 18080
$serveScript = Join-Path $root "scripts\serve-nocache.py"
$py = "D:\Tools\python\python.exe"
$logRoot = Join-Path $root "logs"
if (-not (Test-Path $logRoot)) { New-Item -ItemType Directory -Path $logRoot | Out-Null }

function Test-ServerAlive {
  param([int]$Port)
  try {
    $client = New-Object System.Net.Sockets.TcpClient
    $iar = $client.BeginConnect("127.0.0.1", $Port, $null, $null)
    $ok = $iar.AsyncWaitHandle.WaitOne(2000, $false)
    if (-not $ok) { $client.Close(); return $false }
    $client.EndConnect($iar)
    # HTTP HEAD 探活,3 秒内必须返回
    $req = [System.Net.HttpWebRequest]::Create("http://127.0.0.1:$Port/site/index.html")
    $req.Method = "HEAD"
    $req.Timeout = 3000
    $resp = $req.GetResponse()
    $code = [int]$resp.StatusCode
    $resp.Close()
    $client.Close()
    return ($code -ge 200 -and $code -lt 500)
  } catch {
    return $false
  }
}

function Start-Server {
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = $py
  $psi.Arguments = "-u scripts\serve-nocache.py"
  $psi.WorkingDirectory = $root
  $psi.UseShellExecute = $false
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true
  $psi.CreateNoWindow = $true
  $proc = [System.Diagnostics.Process]::Start($psi)
  return $proc.Id
}

$log = Join-Path $logRoot "guard-$(Get-Date -Format 'yyyyMMdd').log"
"  -- internal-restart-guard  -- $(date -Format 'yyyy-MM-dd HH:mm:ss')  -- port=$port" | Out-File -Append -FilePath $log -Encoding utf8
Write-Host "[guard] 启动 · 每 30 秒探活 18080"

while ($true) {
  Start-Sleep -Seconds 30
  if (Test-ServerAlive -Port $port) { continue }
  $msg = "[$(Get-Date -Format 'HH:mm:ss')] server 没响应,准备重启"
  Write-Host $msg
  $msg | Out-File -Append -FilePath $log -Encoding utf8
  # 杀掉旧 python 进程(尝试,可能已经死了)
  Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Start-Sleep -Seconds 2
  try {
    $newId = Start-Server
    $msg2 = "[$(Get-Date -Format 'HH:mm:ss')] 重启成功 · new PID=$newId"
    Write-Host $msg2
    $msg2 | Out-File -Append -FilePath $log -Encoding utf8
  } catch {
    $err = "[$(Get-Date -Format 'HH:mm:ss')] 重启失败: $($_.Exception.Message)"
    Write-Host $err
    $err | Out-File -Append -FilePath $log -Encoding utf8
  }
}
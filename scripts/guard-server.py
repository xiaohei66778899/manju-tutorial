import os, sys, time, subprocess, socket, urllib.request, urllib.error
ROOT = r"E:\AIGC\课件\12小说"
PORT = 18080
SCRIPT = os.path.join(ROOT, "scripts", "serve-nocache.py")
LOG = os.path.join(ROOT, "logs", f"guard-{time.strftime('%Y%m%d')}.log")
os.makedirs(os.path.dirname(LOG), exist_ok=True)

def alive(port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect(("127.0.0.1", port))
        s.close()
        req = urllib.request.Request(f"http://127.0.0.1:{port}/site/index.html", method="HEAD")
        r = urllib.request.urlopen(req, timeout=3)
        return 200 <= r.status < 500
    except Exception:
        return False

def start_server():
    kwargs = dict(cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                  creationflags=0x08000008 if sys.platform == "win32" else 0)
    return subprocess.Popen([r"D:\Tools\python\python.exe", "-u", SCRIPT], **kwargs)

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}\n"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line)
    sys.stdout.write(line); sys.stdout.flush()

log("guard 启动 · 每 30s 探活")
while True:
    time.sleep(30)
    if alive(PORT):
        continue
    log("server 没响应,准备重启")
    subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True)
    time.sleep(2)
    try:
        p = start_server()
        log(f"重启成功 · PID={p.pid}")
    except Exception as e:
        log(f"重启失败: {e}")

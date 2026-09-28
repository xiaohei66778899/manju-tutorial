Add-Type -AssemblyName PresentationCore
Add-Type -AssemblyName PresentationFramework

function Render-Logo {
    param([string]$OutPath, [string]$PathData, [int]$Size, [string]$Color1, [string]$Color2)

    $xaml = "<Border xmlns=`"http://schemas.microsoft.com/winfx/2006/xaml/presentation`" Width=`"$Size`" Height=`"$Size`" CornerRadius=`"16`"><Border.Background><LinearGradientBrush StartPoint=`"0,0`" EndPoint=`"1,1`"><GradientStop Color=`"$Color1`" Offset=`"0`"/><GradientStop Color=`"$Color2`" Offset=`"1`"/></LinearGradientBrush></Border.Background><Viewbox Margin=`"24`"><Path Fill=`"White`" Data=`"$PathData`"/></Viewbox></Border>"

    $reader = New-Object System.Xml.XmlTextReader (New-Object System.IO.StringReader $xaml)
    $border = [Windows.Markup.XamlReader]::Load($reader)

    $sz = New-Object System.Windows.Size ($Size, $Size)
    $border.Measure($sz)
    $rt = New-Object System.Windows.Rect (0, 0, $Size, $Size)
    $border.Arrange($rt)
    $border.UpdateLayout()

    $rtb = New-Object System.Windows.Media.Imaging.RenderTargetBitmap ($Size, $Size, 96, 96, [System.Windows.Media.PixelFormats]::Pbgra32)
    $rtb.Render($border)

    $encoder = New-Object System.Windows.Media.Imaging.PngBitmapEncoder
    $encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($rtb))

    $fs = [System.IO.File]::Open($OutPath, [System.IO.FileMode]::Create)
    $encoder.Save($fs)
    $fs.Close()

    return (Get-Item $OutPath).Length
}

$bytedancePath = "M19.8772 1.4685L24 2.5326v18.9426l-4.1228 1.0563V1.4685zm-13.3481 9.428l4.115 1.0641v8.9786l-4.115 1.0642v-11.107zM0 2.572l4.115 1.0642v16.7354L0 21.428V2.572zm17.4553 5.6205v11.107l-4.1228-1.0642V9.2568l4.1228-1.0642z"
$targetPath = "M12.0005 0C18.627 0 24 5.373 24 12.0005 24 18.627 18.627 24 11.9995 24 5.373 24 0 18.627 0 11.9995 0 5.373 5.373 0 12.0005 0zm0 19.826a7.8265 7.8265 0 10-.001-15.652C7.7133 4.2246 4.2653 7.7136 4.2653 12c0 4.2864 3.448 7.7754 7.7342 7.826h.001zm0-3.9853a3.8402 3.8402 0 110-7.6803c2.1204.0006 3.839 1.7197 3.839 3.8401s-1.7186 3.8396-3.839 3.8402z"
$trendingUpPath = "M16 7h6v6 M22 7l-8.5 8.5-5-5L2 17"

Set-Location "E:\AIGC\课件\12小说\site\assets\icons"

$size1 = Render-Logo "qianchuan-bytedance.png" $bytedancePath 128 "#635BFF" "#8B5CF6"
Write-Host "OK  qianchuan-bytedance.png  $size1 bytes" -ForegroundColor Green

$size2 = Render-Logo "qianchuan-target.png" $targetPath 128 "#635BFF" "#A78BFA"
Write-Host "OK  qianchuan-target.png  $size2 bytes" -ForegroundColor Green

$size3 = Render-Logo "qianchuan-trend.png" $trendingUpPath 128 "#4F46E5" "#8B5CF6"
Write-Host "OK  qianchuan-trend.png  $size3 bytes" -ForegroundColor Green

Get-ChildItem | Where-Object Name -like "qianchuan-*" | Select-Object Name, Length | Format-Table -AutoSize
# 以管理员身份运行
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "请以管理员身份运行此脚本！"
    Write-Host "右键点击 PowerShell，选择'以管理员身份运行'"
    exit 1
}

Write-Host "==========================================" -ForegroundColor Green
Write-Host "  FFmpeg 自动配置脚本" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# FFmpeg 路径
$ffmpegPath = "C:\ffmpeg\bin"

# 检查 FFmpeg 是否存在
if (-Not (Test-Path "$ffmpegPath\ffmpeg.exe")) {
    Write-Host "✗ 未找到 FFmpeg！" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先下载 FFmpeg：" -ForegroundColor Yellow
    Write-Host "1. 访问: https://www.gyan.dev/ffmpeg/builds/" -ForegroundColor Cyan
    Write-Host "2. 下载 ffmpeg-release-essentials.zip" -ForegroundColor Cyan
    Write-Host "3. 解压到 C:\ffmpeg" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "完成后再次运行此脚本"
    exit 1
}

Write-Host "✓ 找到 FFmpeg: $ffmpegPath" -ForegroundColor Green

# 获取当前系统环境变量 Path
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")

# 检查是否已存在
if ($currentPath -notlike "*$ffmpegPath*") {
    Write-Host "正在添加到环境变量..." -ForegroundColor Yellow
    
    # 添加 FFmpeg 到 Path
    $newPath = $currentPath + ";" + $ffmpegPath
    [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
    
    Write-Host "✓ FFmpeg 已添加到系统环境变量" -ForegroundColor Green
} else {
    Write-Host "✓ FFmpeg 已在环境变量中" -ForegroundColor Green
}

# 验证安装
Write-Host ""
Write-Host "验证安装..." -ForegroundColor Yellow
Write-Host "------------------------------------------"

# 刷新环境变量
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")

try {
    $version = & "$ffmpegPath\ffmpeg.exe" -version 2>&1 | Select-Object -First 1
    Write-Host $version -ForegroundColor Cyan
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "  ✓ FFmpeg 配置成功！" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "现在可以运行自动剪辑脚本了：" -ForegroundColor White
    Write-Host "  cd C:\Users\ZhuanZ\.openclaw\workspace\scripts" -ForegroundColor Cyan
    Write-Host "  python auto_clipper.py" -ForegroundColor Cyan
} catch {
    Write-Host "✗ 验证失败，请检查安装" -ForegroundColor Red
}

Write-Host ""
Read-Host "按 Enter 键退出"

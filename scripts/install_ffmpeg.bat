@echo off
chcp 65001 >nul
echo ==========================================
echo FFmpeg 自动剪辑工具 - 快速安装
echo ==========================================
echo.

REM 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 请以管理员身份运行此脚本！
    echo 右键点击脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo [1/3] 检查 Chocolatey 是否已安装...
where choco >nul 2>&1
if %errorLevel% neq 0 (
    echo 正在安装 Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    set "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
) else (
    echo ✓ Chocolatey 已安装
)

echo.
echo [2/3] 安装 FFmpeg...
choco install ffmpeg -y
if %errorLevel% neq 0 (
    echo FFmpeg 安装失败，请手动安装
    pause
    exit /b 1
)
echo ✓ FFmpeg 安装完成

echo.
echo [3/3] 验证安装...
ffmpeg -version | findstr "ffmpeg version" >nul
if %errorLevel% equ 0 (
    echo ✓ FFmpeg 安装验证成功
    ffmpeg -version | findstr "ffmpeg version"
) else (
    echo ✗ FFmpeg 安装验证失败
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 安装完成！
echo ==========================================
echo.
echo 现在可以运行自动剪辑脚本了：
echo   python auto_clipper.py
echo.
pause

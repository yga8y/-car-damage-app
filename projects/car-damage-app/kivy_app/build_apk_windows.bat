@echo off
chcp 65001 >nul
echo ==========================================
echo 车辆定损AI APP - 快速构建工具
echo ==========================================
echo.

REM 检查Docker
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: Docker未安装
    echo 请访问 https://docs.docker.com/desktop/install/windows/ 下载安装
    pause
    exit /b 1
)

echo [1/4] 检查Docker环境...
docker --version
echo.

REM 项目目录
set "PROJECT_DIR=%~dp0"
echo 项目目录: %PROJECT_DIR%

REM 创建输出目录
if not exist "%PROJECT_DIR%\bin" mkdir "%PROJECT_DIR%\bin"

echo.
echo [2/4] 准备构建环境...
echo 使用预配置构建镜像...

REM 使用kivy/buildozer官方镜像
docker pull kivy/buildozer:latest 2>nul || echo 使用本地镜像...

echo.
echo [3/4] 开始构建APK...
echo 注意: 首次构建需要下载依赖，可能需要30-60分钟
echo.

REM 运行构建
docker run --rm -it ^
    -v "%PROJECT_DIR%:/home/user/app" ^
    -v "%PROJECT_DIR%\bin:/home/user/app/bin" ^
    kivy/buildozer ^
    bash -c "cd /home/user/app && buildozer android debug"

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo 构建成功!
    echo ==========================================
    echo.
    echo APK文件位置:
    dir /b "%PROJECT_DIR%\bin\*.apk" 2>nul || echo   %PROJECT_DIR%\bin\
    echo.
    echo 下一步:
    echo   1. 将APK传输到手机
    echo   2. 安装并运行
    echo.
) else (
    echo.
    echo ==========================================
    echo 构建失败
    echo ==========================================
    echo.
    echo 可能原因:
    echo   1. 网络连接问题
    echo   2. 磁盘空间不足(需要10GB+)
    echo   3. Docker配置问题
    echo.
    echo 解决方案:
    echo   - 检查网络连接
    echo   - 清理Docker空间: docker system prune
    echo   - 使用GitHub Actions自动构建
    echo.
)

pause

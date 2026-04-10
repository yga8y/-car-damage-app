#!/bin/bash
# 使用Docker构建APK

echo "=========================================="
echo "车辆定损AI APP - Docker构建"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装"
    echo "请安装Docker:"
    echo "  Windows: https://docs.docker.com/desktop/install/windows/"
    echo "  Mac: https://docs.docker.com/desktop/install/mac/"
    echo "  Linux: https://docs.docker.com/engine/install/"
    exit 1
fi

echo "✓ Docker已安装"
docker --version
echo ""

# 项目目录
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "项目目录: $PROJECT_DIR"

# 创建输出目录
mkdir -p "$PROJECT_DIR/bin"

echo ""
echo "步骤1: 构建Docker镜像..."
echo "（首次构建需要5-10分钟）"
docker build -t car-damage-app-builder "$PROJECT_DIR"

echo ""
echo "步骤2: 运行构建容器..."
echo "（这可能需要20-40分钟）"
echo ""

# 运行构建
docker run --rm \
    -v "$PROJECT_DIR:/app" \
    -v "$PROJECT_DIR/bin:/app/bin" \
    car-damage-app-builder \
    bash -c "
        echo '开始构建APK...'
        buildozer android debug 2>&1 | tee build.log
        
        if [ -f bin/*.apk ]; then
            echo ''
            echo '✓ 构建成功!'
            echo ''
            echo 'APK文件:'
            ls -lh bin/*.apk
            
            # 复制到主机目录
            cp bin/*.apk /app/bin/车辆定损AI-v1.0.0.apk
        else
            echo ''
            echo '✗ 构建失败'
            echo '查看日志: build.log'
            exit 1
        fi
    "

# 检查结果
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ APK构建完成!"
    echo "=========================================="
    echo ""
    echo "APK文件位置:"
    ls -lh "$PROJECT_DIR/bin/"*.apk 2>/dev/null || echo "  $PROJECT_DIR/bin/"
    echo ""
    echo "安装到手机:"
    echo "  1. 开启手机USB调试"
    echo "  2. 连接手机到电脑"
    echo "  3. 运行: adb install '$PROJECT_DIR/bin/车辆定损AI-v1.0.0.apk'"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "✗ 构建失败"
    echo "=========================================="
    echo ""
    echo "请检查:"
    echo "  1. Docker是否正常运行"
    echo "  2. 网络连接是否正常"
    echo "  3. 磁盘空间是否充足（需要10GB+）"
    echo ""
fi

echo "按Enter键退出..."
read

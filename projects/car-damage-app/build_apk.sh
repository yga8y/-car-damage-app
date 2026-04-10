#!/bin/bash
# 车辆定损APP - Docker构建脚本
# 使用Flutter Docker镜像构建APK

set -e

echo "=========================================="
echo "车辆定损APP - Docker构建"
echo "=========================================="

# 项目目录
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
FRONTEND_DIR="$PROJECT_DIR/frontend"

echo ""
echo "项目目录: $PROJECT_DIR"
echo "前端目录: $FRONTEND_DIR"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装"
    echo "请安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

echo ""
echo "Docker版本:"
docker --version

# 创建输出目录
mkdir -p "$PROJECT_DIR/build"

echo ""
echo "=========================================="
echo "开始构建APK..."
echo "=========================================="

# 使用Flutter Docker镜像构建
docker run --rm \
    -v "$FRONTEND_DIR:/app" \
    -v "$PROJECT_DIR/build:/output" \
    -w /app \
    cirrusci/flutter:stable \
    bash -c "
        echo '获取依赖...'
        flutter pub get
        
        echo '构建发布版APK...'
        flutter build apk --release
        
        echo '复制APK到输出目录...'
        cp build/app/outputs/flutter-apk/app-release.apk /output/车辆定损AI-v1.0.0.apk
        
        echo '构建完成!'
    "

echo ""
echo "=========================================="
echo "构建完成!"
echo "=========================================="
echo ""
echo "APK文件位置:"
echo "  $PROJECT_DIR/build/车辆定损AI-v1.0.0.apk"
echo ""
echo "文件大小:"
ls -lh "$PROJECT_DIR/build/车辆定损AI-v1.0.0.apk" 2>/dev/null || echo "  (请检查build目录)"
echo ""
echo "安装命令:"
echo "  adb install '$PROJECT_DIR/build/车辆定损AI-v1.0.0.apk'"
echo ""

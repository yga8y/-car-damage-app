#!/bin/bash
# 车辆定损AI APP - APK构建脚本
# 使用Buildozer构建APK

echo "=========================================="
echo "车辆定损AI APP - APK构建"
echo "=========================================="
echo ""

# 检查是否在WSL或Linux环境
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "✓ 支持的环境: $OSTYPE"
else
    echo "⚠ 警告: 当前环境可能不支持直接构建"
    echo "建议使用WSL2或Docker"
fi

echo ""
echo "步骤1: 准备环境..."

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

echo ""
echo "步骤2: 安装依赖..."

# 安装必要工具
pip install --upgrade pip
pip install buildozer cython

echo ""
echo "步骤3: 准备项目文件..."

# 确保目录结构正确
cd "$(dirname "$0")"

# 复制数据库文件到app目录
cp ../database/parts_pricing.sql . 2>/dev/null || echo "数据库文件将在运行时创建"
cp ../database/damage_rules_complete_v2.sql . 2>/dev/null || echo "规则文件将在运行时创建"

echo ""
echo "步骤4: 构建APK..."
echo "（这可能需要10-30分钟，取决于网络速度）"
echo ""

# 使用buildozer构建
buildozer android debug

# 检查结果
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ 构建成功!"
    echo "=========================================="
    echo ""
    echo "APK文件位置:"
    ls -lh bin/*.apk 2>/dev/null || echo "  ./bin/目录下"
    echo ""
    echo "安装命令:"
    echo "  buildozer android deploy run"
    echo ""
    echo "或直接安装:"
    echo "  adb install bin/*.apk"
else
    echo ""
    echo "=========================================="
    echo "✗ 构建失败"
    echo "=========================================="
    echo ""
    echo "常见解决方案:"
    echo "1. 检查网络连接（需要下载Android SDK）"
    echo "2. 确保有足够的磁盘空间（需要5GB+）"
    echo "3. 检查buildozer.spec配置"
    echo ""
    echo "查看详细日志:"
    echo "  buildozer android debug 2>&1 | tee build.log"
fi

echo ""
echo "按Enter键退出..."
read

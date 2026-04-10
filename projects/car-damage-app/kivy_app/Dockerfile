# 使用Buildozer构建Kivy APK的Dockerfile
FROM ubuntu:22.04

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/root/.buildozer/android/platform/android-sdk
ENV PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    automake \
    gettext \
    build-essential \
    libgtk-3-dev \
    libgl1-mesa-dev \
    libgles2-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip3 install --upgrade pip setuptools
RUN pip3 install buildozer cython

# 创建工作目录
WORKDIR /app

# 复制项目文件
COPY . /app/

# 创建启动脚本
RUN echo '#!/bin/bash\n\
echo "========================================"\n\
echo "车辆定损AI APP - Docker构建环境"\n\
echo "========================================"\n\
echo ""\n\
echo "构建命令:"\n\
echo "  buildozer android debug"\n\
echo ""\n\
echo "清理构建:"\n\
echo "  buildozer android clean"\n\
echo ""\n\
echo "进入交互模式..."\n\
bash' > /start.sh && chmod +x /start.sh

# 默认启动交互模式
CMD ["/start.sh"]

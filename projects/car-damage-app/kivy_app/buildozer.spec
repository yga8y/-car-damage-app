[app]
# 应用标题
title = 车辆定损AI

# 包名
package.name = cardamageai
package.domain = com.example

# 源码目录
source.dir = .

# 包含的文件
source.include_exts = py,png,jpg,kv,atlas,db,sql

# 版本
version = 1.0.0

# 依赖项
requirements = python3,kivy,sqlite3

# 图标
# icon.filename = %(source.dir)s/assets/icon.png

# 权限
android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# API级别
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# 架构
android.archs = armeabi-v7a, arm64-v8a

# 屏幕方向
orientation = portrait

# 全屏
fullscreen = 0

# 应用名称
android.app_name = 车辆定损AI

# 禁用某些功能以减小APK大小
android.gradle_dependencies = 
android.add_aars = 
android.add_jars = 

# 启用日志
android.logcat_filters = *:S python:D

[buildozer]
# 构建目录
build_dir = ./.buildozer

# 二进制目录
bin_dir = ./bin

# 日志级别
log_level = 2

# 警告为错误
warn_on_root = 1

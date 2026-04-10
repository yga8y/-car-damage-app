# 车辆定损APP - APK构建指南

## 📱 APK生成说明

由于当前环境缺少Flutter SDK和Android构建工具，无法直接生成APK。
以下是完整的构建步骤和替代方案。

---

## 方案一：本地构建APK（推荐）

### 1. 环境准备

#### 安装Flutter SDK
```bash
# 下载Flutter SDK
# 官网: https://docs.flutter.dev/get-started/install

# Windows PowerShell
git clone https://github.com/flutter/flutter.git -b stable

# 添加环境变量
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\flutter\bin", "User")
```

#### 安装Android Studio
1. 下载Android Studio: https://developer.android.com/studio
2. 安装Android SDK
3. 配置Android模拟器

#### 验证环境
```bash
flutter doctor
```

### 2. 构建APK

```bash
# 进入项目目录
cd projects/car-damage-app/frontend

# 获取依赖
flutter pub get

# 构建发布版APK
flutter build apk --release

# APK输出位置
# build/app/outputs/flutter-apk/app-release.apk
```

### 3. 安装APK

```bash
# 连接手机（开启USB调试）
flutter install

# 或手动安装
adb install build/app/outputs/flutter-apk/app-release.apk
```

---

## 方案二：使用GitHub Actions自动构建

### 创建构建工作流

文件: `.github/workflows/build-apk.yml`

```yaml
name: Build APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'
    
    - name: Get dependencies
      run: |
        cd frontend
        flutter pub get
    
    - name: Build APK
      run: |
        cd frontend
        flutter build apk --release
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: car-damage-app-apk
        path: frontend/build/app/outputs/flutter-apk/app-release.apk
```

---

## 方案三：使用在线构建服务

### 推荐服务
1. **Codemagic**: https://codemagic.io
   - 免费构建Flutter应用
   - 自动发布到Google Play

2. **Bitrise**: https://bitrise.io
   - 支持Flutter构建
   - 每月200分钟免费构建时间

---

## 📦 项目文件结构

```
projects/car-damage-app/
├── frontend/                    # Flutter前端
│   ├── lib/
│   │   ├── main.dart           # 入口文件
│   │   └── screens/            # 页面
│   │       ├── home_screen.dart       # 首页
│   │       ├── camera_screen.dart     # 拍照页
│   │       ├── result_screen.dart     # 结果页
│   │       ├── quote_screen.dart      # 报价页
│   │       └── history_screen.dart    # 历史记录
│   ├── pubspec.yaml            # 依赖配置
│   └── android/                # Android配置
│       └── app/
│           └── build.gradle    # 构建配置
├── backend/                     # 后端API
│   └── app/
│       └── routers/
│           └── damage_evaluation.py   # 定损API ⭐
├── database/                    # 数据库
│   ├── parts_pricing.sql              # 配件价格
│   └── damage_rules_complete_v2.sql   # 定损规则
└── ai-models/                   # AI模型
    └── weights/
        └── tqvcd_damage/
            └── best.pt                  # 训练好的模型
```

---

## 🔧 关键配置

### 1. 后端API地址配置

文件: `frontend/lib/config/api_config.dart`

```dart
class ApiConfig {
  // 开发环境
  static const String baseUrl = 'http://localhost:8000';
  
  // 生产环境（部署后修改）
  // static const String baseUrl = 'http://your-server-ip:8000';
  
  // API端点
  static const String evaluateDamage = '/api/car/damage/evaluate';
  static const String getAccidentTypes = '/api/car/accident-types';
  static const String getPartPrice = '/api/car/parts/price';
}
```

### 2. Android配置

文件: `frontend/android/app/build.gradle`

```gradle
android {
    compileSdkVersion 34
    
    defaultConfig {
        applicationId "com.example.car_damage_app"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
    }
    
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}
```

### 3. 权限配置

文件: `frontend/android/app/src/main/AndroidManifest.xml`

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    
    <application
        android:label="车辆定损AI"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher">
        ...
    </application>
</manifest>
```

---

## 📱 APP功能说明

### 已实现功能
1. ✅ 拍照上传车损照片
2. ✅ AI识别损伤部位
3. ✅ 自动匹配定损规则
4. ✅ 查询配件价格（OE编号+原厂价）
5. ✅ 生成报价单
6. ✅ 查看历史记录

### API集成
- 定损评估接口: `POST /api/car/damage/evaluate`
- 支持事故类型: 追尾、侧撞、正面碰撞、剐蹭
- 自动判断: 更换/修复
- 费用计算: 配件费 + 工时费

---

## 🚀 快速开始

### 方式1：使用预构建APK（如果有）
```bash
# 下载APK到手机
# 开启"允许安装未知来源应用"
# 点击安装
```

### 方式2：本地运行调试
```bash
# 启动后端服务
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 启动前端（新终端）
cd frontend
flutter run
```

---

## 📞 技术支持

如需帮助生成APK，请提供：
1. Flutter环境已安装的电脑
2. 或GitHub仓库访问权限（使用GitHub Actions自动构建）

---

**生成时间**: 2026-04-09
**版本**: v1.0.0

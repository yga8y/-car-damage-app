# 车辆定损AI APP - 项目交付包

## 📦 交付内容

由于本地环境网络限制，无法直接下载Flutter SDK构建APK。
本交付包包含完整的项目源码和多种构建方案。

---

## 📁 项目结构

```
car-damage-app/
├── 📱 frontend/                    # Flutter前端APP
│   ├── lib/
│   │   ├── main.dart              # 入口文件
│   │   ├── screens/               # 页面
│   │   │   ├── home_screen.dart   # 首页
│   │   │   ├── camera_screen.dart # 拍照
│   │   │   ├── result_screen.dart # 结果
│   │   │   ├── quote_screen.dart  # 报价
│   │   │   └── history_screen.dart# 历史
│   │   └── services/
│   │       └── damage_api_service.dart  # API服务 ⭐
│   ├── pubspec.yaml               # 依赖配置
│   └── android/                   # Android配置
│
├── 🔧 backend/                     # Python后端API
│   └── app/
│       └── routers/
│           └── damage_evaluation.py     # 定损API ⭐
│
├── 🗄️ database/                    # 数据库
│   ├── parts_pricing.sql          # 配件价格 (151条)
│   └── damage_rules_complete_v2.sql    # 定损规则 (157条)
│
├── 🤖 ai-models/                   # AI模型
│   └── weights/
│       └── tqvcd_damage/
│           └── best.pt             # 训练好的模型
│
├── 🔨 .github/workflows/            # GitHub Actions
│   └── build-apk.yml               # 自动构建配置
│
├── 📖 文档/
│   ├── APK_BUILD_GUIDE.md          # APK构建指南
│   ├── COMPLETION_REPORT.md        # 完成报告
│   └── README.md                   # 项目说明
│
└── 🔧 build_apk.sh                 # Docker构建脚本
```

---

## 🚀 快速构建APK（三种方案）

### 方案一：GitHub Actions自动构建（推荐）

**步骤：**

1. **创建GitHub仓库**
   ```bash
   # 在GitHub创建新仓库
   # 例如: https://github.com/yourname/car-damage-app
   ```

2. **上传代码**
   ```bash
   cd car-damage-app
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourname/car-damage-app.git
   git push -u origin main
   ```

3. **触发构建**
   - 进入GitHub仓库
   - 点击 Actions 标签
   - 选择 "Build Flutter APK" 工作流
   - 点击 "Run workflow"

4. **下载APK**
   - 等待构建完成（约5-10分钟）
   - 在 Actions 页面下载 artifacts
   - 或在 Releases 页面下载

**优点：**
- 无需本地配置
- 自动构建
- 可下载历史版本

---

### 方案二：Docker本地构建

**要求：** 已安装Docker

**步骤：**

1. **打开PowerShell/CMD**

2. **进入项目目录**
   ```powershell
   cd C:\path\to\car-damage-app
   ```

3. **运行构建脚本**
   ```powershell
   # Windows (使用Git Bash或WSL)
   bash build_apk.sh
   
   # 或手动执行Docker命令
   docker run --rm `
     -v "${PWD}/frontend:/app" `
     -v "${PWD}/build:/output" `
     -w /app `
     cirrusci/flutter:stable `
     bash -c "flutter pub get && flutter build apk --release && cp build/app/outputs/flutter-apk/app-release.apk /output/车辆定损AI.apk"
   ```

4. **获取APK**
   - 输出位置: `build/车辆定损AI.apk`

---

### 方案三：本地Flutter环境构建

**要求：** 安装Flutter SDK + Android Studio

**步骤：**

1. **安装Flutter**
   - 下载: https://docs.flutter.dev/get-started/install
   - 解压到 `C:\flutter`
   - 添加环境变量

2. **安装Android Studio**
   - 下载: https://developer.android.com/studio
   - 安装Android SDK

3. **验证环境**
   ```powershell
   flutter doctor
   ```

4. **构建APK**
   ```powershell
   cd car-damage-app/frontend
   flutter pub get
   flutter build apk --release
   ```

5. **获取APK**
   - 输出位置: `frontend/build/app/outputs/flutter-apk/app-release.apk`

---

## 📱 APP功能

### 已实现功能

1. **📸 AI拍照识别**
   - 拍摄车损照片
   - AI自动识别损伤部位

2. **🔍 智能定损**
   - 选择事故类型（追尾/侧撞/正面碰撞/剐蹭）
   - 自动匹配定损规则
   - 判断更换/修复

3. **💰 精准报价**
   - 查询配件原厂价格（带OE编号）
   - 自动计算工时费
   - 生成总报价

4. **📋 定损报告**
   - 配件清单
   - 费用明细
   - 维修建议

5. **📚 历史记录**
   - 保存定损记录
   - 查看历史报价

### 数据来源

- **配件价格**: 151条原厂配件价格（10个主流品牌）
- **定损规则**: 157条专业规则（覆盖4种事故类型）
- **AI模型**: TQVCD数据集训练，准确率61.64%

---

## 🔧 后端服务部署

APP需要连接后端API才能正常工作。

### 本地部署（测试）

```powershell
# 1. 安装Python依赖
cd backend
pip install fastapi uvicorn sqlite3

# 2. 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 3. 修改APP配置
# 编辑 frontend/lib/services/damage_api_service.dart
# 修改 baseUrl 为: http://10.0.2.2:8000 (模拟器) 或您的IP
```

### 服务器部署（生产）

```bash
# 使用Docker部署
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/backend/cardamage.db:/app/cardamage.db \
  --name car-damage-api \
  python:3.11-slim \
  bash -c "pip install fastapi uvicorn && uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

---

## 📋 系统要求

### 运行APP
- Android 5.0+ (API 21+)
- 存储空间: 50MB+
- 网络连接（连接后端API）

### 开发环境
- Flutter 3.16+
- Dart 3.0+
- Android SDK 34
- Python 3.11+ (后端)

---

## 🆘 常见问题

### Q1: GitHub Actions构建失败？
**A:** 检查:
- 是否已推送代码到GitHub
- 是否启用了Actions权限
- 查看Actions日志获取详细错误

### Q2: APP无法连接后端？
**A:** 检查:
- 后端服务是否启动
- 手机与电脑是否在同一网络
- API地址配置是否正确

### Q3: 配件价格不准确？
**A:** 
- 配件价格仅供参考
- 实际价格以4S店报价为准
- 可定期更新database/parts_pricing.sql

---

## 📞 技术支持

如有问题，请检查:
1. `APK_BUILD_GUIDE.md` - 详细构建指南
2. `COMPLETION_REPORT.md` - 项目完成报告
3. GitHub Actions日志 - 构建错误信息

---

## ✅ 交付清单

- [x] Flutter前端源码
- [x] Python后端API
- [x] 配件价格数据库 (151条)
- [x] 定损规则库 (157条)
- [x] AI训练模型
- [x] GitHub Actions自动构建配置
- [x] Docker构建脚本
- [x] 完整文档

**项目状态**: 已完成，等待构建APK

---

**交付时间**: 2026-04-09
**版本**: v1.0.0
**作者**: 龙虾小明

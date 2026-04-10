# 车辆定损AI APP - Kivy版本交付包

## 📦 交付内容

由于本地环境网络限制，我为您准备了**Kivy版本的Python APP**，可以更容易地构建APK。

---

## 📁 文件结构

```
kivy_app/
├── main.py                    # Kivy APP主程序 ⭐
├── buildozer.spec             # Buildozer构建配置
├── Dockerfile                 # Docker构建配置
├── build_apk.sh              # Linux/Mac构建脚本
├── build_apk_windows.bat     # Windows构建脚本
├── docker_build.bat          # Docker构建脚本
└── README.md                 # 本文件
```

---

## 🚀 快速构建APK（三种方案）

### 方案一：Docker构建（推荐，最简单）

**要求：** 已安装Docker

**步骤：**

1. **打开PowerShell或CMD**

2. **进入项目目录**
   ```powershell
   cd C:\path\to\car-damage-app\kivy_app
   ```

3. **运行构建脚本**
   ```powershell
   .\build_apk_windows.bat
   ```

4. **等待构建完成**
   - 首次构建：30-60分钟（下载依赖）
   - 后续构建：5-10分钟

5. **获取APK**
   - 输出位置: `kivy_app/bin/车辆定损AI-v1.0.0.apk`

---

### 方案二：GitHub Actions自动构建

**步骤：**

1. **创建GitHub仓库**
   - 访问 https://github.com/new
   - 仓库名: `car-damage-app`

2. **上传代码**
   ```powershell
   cd C:\path\to\car-damage-app
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/您的用户名/car-damage-app.git
   git push -u origin main
   ```

3. **触发构建**
   - 进入GitHub仓库
   - 点击 Actions 标签
   - 选择工作流运行

4. **下载APK**
   - 在Actions页面下载

---

### 方案三：Linux/WSL本地构建

**要求：** WSL2或Linux系统

**步骤：**

```bash
# 1. 进入目录
cd car-damage-app/kivy_app

# 2. 安装依赖
sudo apt-get update
sudo apt-get install -y python3-pip
pip3 install buildozer cython

# 3. 构建APK
./build_apk.sh
```

---

## 📱 APP功能

### 已实现功能

1. **🚗 车型选择**
   - 支持10个主流品牌
   - 自定义车系和年款

2. **💥 事故类型**
   - 追尾
   - 侧撞
   - 正面碰撞
   - 剐蹭

3. **🔍 智能定损**
   - 输入损伤部位
   - 选择损伤类型
   - 自动判断更换/修复

4. **💰 费用计算**
   - 配件价格查询
   - 工时费计算
   - 总费用汇总

5. **📋 定损报告**
   - 显示OE编号
   - 维修建议
   - 判定原因

### 数据来源

- **配件价格**: 151条原厂配件数据
- **定损规则**: 157条专业规则
- **安全件识别**: 自动标记安全件

---

## 🔧 技术说明

### 技术栈
- **框架**: Kivy (Python)
- **数据库**: SQLite
- **构建工具**: Buildozer
- **目标平台**: Android

### 优势
- 单文件运行，无需后端
- 内置数据库，离线可用
- 体积小，安装快速
- 跨平台，易于维护

---

## 📋 系统要求

### 运行APP
- Android 5.0+ (API 21+)
- 存储空间: 20MB+
- 无需网络连接

### 构建APK
- Docker 或
- Python 3.8+ + Buildozer 或
- GitHub Actions

---

## 🆘 常见问题

### Q1: Docker构建失败？
**A:** 
- 检查Docker是否运行
- 检查网络连接
- 清理Docker空间: `docker system prune`
- 使用管理员权限运行

### Q2: APK安装失败？
**A:**
- 开启"允许安装未知来源应用"
- 检查APK是否完整下载
- 确保Android版本5.0+

### Q3: 数据不准确？
**A:**
- 配件价格仅供参考
- 实际价格以4S店为准
- 可修改`main.py`中的数据

---

## 📝 自定义数据

如需修改配件价格或规则，编辑 `main.py` 文件：

```python
# 配件价格数据（约第50行）
parts = [
    ('丰田', '卡罗拉', '后保险杠', '52159-02955', 1050, 0, '严重破损必换'),
    # 添加更多...
]

# 定损规则（约第70行）
rules = [
    ('追尾', '后保险杠', '破损', '裂纹/破损/穿孔：更换', 0),
    # 添加更多...
]
```

---

## 🎯 下一步

1. **构建APK**: 使用上述方案之一
2. **安装测试**: 安装到Android手机
3. **数据更新**: 根据实际需求更新配件价格
4. **功能扩展**: 添加更多车型和规则

---

## ✅ 交付清单

- [x] Kivy APP源码 (main.py)
- [x] Buildozer构建配置
- [x] Docker构建脚本
- [x] Windows批处理脚本
- [x] 完整构建文档
- [x] 内置配件数据库
- [x] 内置定损规则库

**项目状态**: 已完成，可构建APK

---

**交付时间**: 2026-04-09
**版本**: v1.0.0
**作者**: 龙虾小明

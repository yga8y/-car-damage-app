# 车辆定损AI APP - GitHub上传和APK获取指南

## 📦 文件说明

您有2个压缩包：
1. **车辆定损AI-APP源码.zip** (11KB) - 简化的Kivy版本，推荐此版本
2. **车辆定损AI-完整项目.zip** - 完整项目（包含Flutter、后端、数据库等）

**推荐使用：车辆定损AI-APP源码.zip**

---

## 🚀 三步获取APK

### 第1步：解压文件

1. **找到压缩包**
   ```
   C:\Users\ZhuanZ\.openclaw\workspace\projects\car-damage-app\车辆定损AI-APP源码.zip
   ```

2. **解压到桌面**
   - 右键点击 `车辆定损AI-APP源码.zip`
   - 选择"解压到当前文件夹"
   - 会得到一个 `kivy_app` 文件夹

---

### 第2步：上传到GitHub

#### 2.1 创建GitHub账号（如果没有）
1. 打开 https://github.com
2. 点击 "Sign up"
3. 输入邮箱、密码、用户名
4. 验证邮箱

#### 2.2 创建新仓库
1. 登录GitHub后，点击右上角 **+** 号
2. 选择 **"New repository"**
3. 填写信息：
   - **Repository name**: `car-damage-app`
   - **Description**: `车辆定损AI APP`
   - 选择 **"Public"**（公开）
   - 勾选 **"Add a README file"**
4. 点击 **"Create repository"**

#### 2.3 上传文件
**方法一：网页上传（最简单）**

1. 在新创建的仓库页面，点击 **"Add file"**
2. 选择 **"Upload files"**
3. 点击 **"choose your files"**
4. 选择解压后的 `kivy_app` 文件夹中的所有文件
   - 或者直接将整个文件夹拖入网页
5. 等待上传完成
6. 点击 **"Commit changes"**

**方法二：使用GitHub Desktop（推荐）**

1. 下载GitHub Desktop: https://desktop.github.com
2. 安装并登录
3. 点击 **"File" → "New repository"**
4. 选择解压后的 `kivy_app` 文件夹
5. 填写仓库名 `car-damage-app`
6. 点击 **"Create repository"**
7. 点击 **"Publish repository"**
8. 选择 **"GitHub.com"**
9. 点击 **"Publish"**

---

### 第3步：自动获取APK

#### 3.1 触发自动构建

上传完成后，GitHub会自动开始构建APK：

1. 在GitHub仓库页面，点击 **"Actions"** 标签
2. 会看到 **"Build Kivy APK"** 工作流正在运行（黄色图标）
3. 等待5-10分钟（首次构建）
4. 当图标变成绿色勾号 ✅，表示构建成功

#### 3.2 下载APK

**方法一：从Actions下载**

1. 点击完成的构建记录（绿色勾号）
2. 页面下方找到 **"Artifacts"** 区域
3. 点击 **"car-damage-app-apk"**
4. 下载ZIP文件
5. 解压ZIP，里面就是 `车辆定损AI.apk`

**方法二：从Releases下载（推荐）**

1. 在仓库页面，点击 **"Releases"**（右侧边栏）
2. 找到最新的发布版本（如 v1.0.1）
3. 点击展开
4. 在 **"Assets"** 区域下载APK文件

---

## 📱 安装APK到手机

### 方法一：直接安装
1. 将APK文件传输到手机（微信、QQ、数据线）
2. 在手机上点击APK文件
3. 如果提示"未知来源"，点击 **"设置" → "允许此来源"**
4. 点击 **"安装"**

### 方法二：使用ADB（电脑安装）
1. 手机开启开发者模式和USB调试
2. 连接手机到电脑
3. 打开CMD或PowerShell
4. 运行：
   ```
   adb install 车辆定损AI.apk
   ```

---

## ✅ 完成检查清单

- [ ] 解压了 `车辆定损AI-APP源码.zip`
- [ ] 创建了GitHub账号
- [ ] 创建了 `car-damage-app` 仓库
- [ ] 上传了所有文件
- [ ] Actions构建成功（绿色勾号）
- [ ] 下载了APK文件
- [ ] 安装到手机

---

## 🆘 常见问题

### Q1: 上传文件时卡住？
**A:** 
- 文件较多，请耐心等待
- 或者分批上传
- 推荐使用GitHub Desktop

### Q2: Actions没有自动运行？
**A:**
- 检查是否上传了 `.github/workflows/build-apk.yml` 文件
- 进入Actions标签，点击 "Enable Actions"
- 手动点击 "Run workflow"

### Q3: 构建失败（红色X）？
**A:**
- 点击构建记录查看错误日志
- 常见原因：文件缺失、配置错误
- 检查是否上传了所有文件

### Q4: 下载的APK无法安装？
**A:**
- 确保Android版本5.0+
- 开启"允许安装未知来源应用"
- 检查APK文件是否完整下载

---

## 📞 需要帮助？

如果在任何步骤遇到问题：
1. 截图错误信息
2. 查看GitHub Actions日志
3. 检查文件是否完整上传

---

## 🎉 恭喜！

完成以上步骤后，您就拥有了自己的车辆定损AI APP！

**APP功能：**
- 📸 智能定损评估
- 💰 配件价格查询
- 📋 自动生成报价
- 🔧 离线使用

**版本**: v1.0.0  
**作者**: 龙虾小明  
**日期**: 2026-04-09

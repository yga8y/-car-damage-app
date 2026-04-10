# 车辆定损AI APP

## 📱 项目说明

智能车辆定损评估APP，基于AI视觉识别和原厂配件数据库。

## 🚀 快速开始

### 获取APK（推荐）

1. **Fork本仓库** 或 **上传到自己的GitHub**
2. 等待GitHub Actions自动构建（约5-10分钟）
3. 在Actions或Releases页面下载APK

### 手动构建

```bash
# 安装依赖
pip install buildozer cython

# 构建APK
buildozer android debug
```

## 📦 功能特性

- 📸 智能定损评估
- 💰 配件价格查询（带OE编号）
- 📋 自动生成报价单
- 🔧 离线使用

## 🚗 支持车型

丰田、大众、本田、别克、日产、比亚迪、特斯拉、宝马、奔驰、奥迪

## 💥 事故类型

追尾、侧撞、正面碰撞、剐蹭

## 📄 文件说明

- `main.py` - APP主程序
- `buildozer.spec` - 构建配置
- `.github/workflows/build-apk.yml` - 自动构建配置

## 📞 技术支持

如有问题，请查看GitHub Actions日志或提交Issue。

## 📄 许可证

MIT License

---

**版本**: v1.0.0  
**作者**: 龙虾小明  
**日期**: 2026-04-09

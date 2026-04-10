# 抖音自动化系统 - 使用说明

## 🎯 功能概述

自动完成：获取抖音热点 → AI生成视频脚本 → 制作视频 → 发布到抖音

## 📁 项目结构

```
douyin-automation/
├── src/
│   ├── index.js      # 主程序入口
│   ├── hotspot.js    # 热点获取模块
│   ├── generate.js   # 视频生成模块
│   └── publish.js    # 发布模块
├── output/           # 输出目录
│   ├── hotspots.json # 热点数据
│   ├── scripts/      # 生成的脚本
│   └── videos/       # 生成的视频
├── config/           # 配置文件
└── package.json
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd workspace/douyin-automation
npm install
```

### 2. 运行系统

```bash
# 运行完整工作流
npm start

# 或分步运行
npm run hotspot    # 仅获取热点
npm run generate   # 生成视频脚本
npm run publish    # 发布视频
```

## 📋 当前状态

### ✅ 已完成
- [x] 项目框架搭建
- [x] 热点获取模块（模拟数据）
- [x] AI脚本生成模块
- [x] 发布模块框架
- [x] 主程序工作流整合

### 🚧 待完善
- [ ] 接入真实抖音热点API
- [ ] 接入AI服务（OpenAI等）生成内容
- [ ] 安装FFmpeg实现视频生成
- [ ] 实现抖音自动登录
- [ ] 实现视频自动上传

## ⚙️ 配置说明

### 环境变量（.env文件）

```
# OpenAI API（用于生成内容）
OPENAI_API_KEY=your_api_key

# 抖音账号（可选）
DOUYIN_USERNAME=
DOUYIN_PASSWORD=
```

## 📝 下一步计划

1. **接入真实热点源**
   - 申请抖音开放平台API
   - 或使用第三方数据服务

2. **接入AI生成**
   - 注册OpenAI API
   - 或使用国产AI服务（文心一言、通义千问等）

3. **视频生成**
   - 安装FFmpeg
   - 准备视频素材库
   - 实现自动剪辑

4. **自动发布**
   - 实现抖音扫码登录
   - 处理反爬虫机制

## ⚠️ 注意事项

- 自动发布需遵守抖音平台规则
- 频繁操作可能触发风控
- 建议使用测试账号先验证

---

**创建时间**: 2026-03-26  
**作者**: 龙虾小明 🦞

# 抖音自动化系统 (Python版)

自动完成：获取抖音热点 → AI生成视频脚本 → 制作视频 → 发布到抖音

## 🚀 快速开始

### 1. 运行系统

```bash
# 进入项目目录
cd workspace/douyin-auto-py

# 运行完整工作流
python main.py

# 或分步运行
python main.py hotspot      # 仅获取热点
python main.py generate     # 生成视频脚本
python main.py setup        # 初始化系统
```

### 2. 命令行参数

```bash
python main.py full --limit 3 --video     # 生成3个脚本并制作视频
python main.py full --limit 5 --publish   # 生成5个脚本并发布
```

## 📁 项目结构

```
douyin-auto-py/
├── main.py                  # 主程序入口
├── src/
│   ├── hotspot.py          # 热点获取模块
│   ├── script_generator.py # 脚本生成模块
│   ├── video_producer.py   # 视频制作模块
│   └── publisher.py        # 发布模块
├── output/                 # 输出目录
│   ├── hotspots.json       # 热点数据
│   ├── scripts/            # 生成的脚本
│   └── videos/             # 生成的视频
├── assets/                 # 素材库
│   ├── videos/             # 视频素材
│   ├── music/              # 音乐素材
│   └── fonts/              # 字体文件
└── config/                 # 配置文件
    ├── auth.json           # 抖音登录信息
    └── publish_history.json # 发布历史
```

## ✅ 当前功能

- [x] 热点获取（模拟数据）
- [x] AI脚本生成（模板）
- [x] 视频制作框架
- [x] 发布模块框架
- [x] 完整工作流整合

## 🚧 待完善

### 高优先级
- [ ] 接入真实抖音热点API
- [ ] 接入AI服务（OpenAI/文心一言/通义千问）
- [ ] 安装FFmpeg实现视频生成

### 中优先级
- [ ] 抖音扫码登录自动化
- [ ] 视频自动上传
- [ ] 定时任务调度

## ⚙️ 配置说明

### 环境变量 (.env)

```bash
# AI服务API密钥
OPENAI_API_KEY=your_key_here
BAIDU_API_KEY=your_key_here
ALIBABA_API_KEY=your_key_here

# 抖音账号（可选）
DOUYIN_USERNAME=
DOUYIN_PASSWORD=
```

## 📝 开发计划

1. **接入真实热点源**
   - 抖音开放平台API申请
   - 第三方数据服务接入

2. **AI内容生成**
   - 接入大语言模型
   - 优化脚本生成质量

3. **视频自动化**
   - FFmpeg视频合成
   - 素材库管理
   - 字幕和特效

4. **自动发布**
   - 抖音登录自动化
   - 视频上传API
   - 风控处理

## ⚠️ 注意事项

- 自动发布需遵守抖音平台规则
- 频繁操作可能触发风控
- 建议使用测试账号先验证

---

**创建时间**: 2026-03-26  
**作者**: 龙虾小明 🦞

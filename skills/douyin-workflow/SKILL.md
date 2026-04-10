# 抖音视频工作流 - Douyin Video Workflow

全自动抖音视频生成系统：热点追踪 → AI脚本 → 自动剪辑 → 批量生成

## 功能特性

- 🔥 **热点追踪** - 自动获取抖音/微博实时热点
- 🤖 **AI生成脚本** - 根据热点自动生成口播文案和分镜
- 🎬 **自动剪辑** - FFmpeg视频合成（需准备素材）
- ⚡ **批量生成** - 一次处理多个热点，效率翻倍

## 快速开始

### 1. 运行完整工作流

```bash
python skills/douyin-workflow/scripts/workflow.py
```

### 2. 指定参数运行

```bash
# 从微博获取热点
python skills/douyin-workflow/scripts/workflow.py --source weibo --count 3

# 指定主题生成
python skills/douyin-workflow/scripts/workflow.py --topic "人工智能发展趋势"

# 自定义风格和时长
python skills/douyin-workflow/scripts/workflow.py --style 科普 --duration 60
```

### 3. 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--source` | 热点来源: douyin/weibo | douyin |
| `--count` | 生成视频数量 | 5 |
| `--style` | 视频风格: 口播/科普/故事 | 口播 |
| `--duration` | 视频时长(秒) | 30 |
| `--topic` | 指定主题(跳过热点获取) | - |

## 输出文件

运行后会在 `output/` 目录生成：

```
output/
├── hotspots_YYYYMMDD_HHMMSS.json    # 热点原始数据
├── script_[主题]_YYYYMMDD_HHMMSS.json  # 脚本JSON
├── script_[主题]_YYYYMMDD_HHMMSS.md    # 脚本Markdown(可读)
└── batch_report_YYYYMMDD_HHMMSS.json   # 批量生成报告
```

## 脚本结构

每个生成的脚本包含：

```json
{
  "title": "#热点标题",
  "topic": "热点标题",
  "style": "口播",
  "duration": 30,
  "scenes": [
    {
      "scene_num": 1,
      "time": "0-10秒",
      "visual": "画面描述",
      "prompt": "AI绘画提示词",
      "voiceover": "配音文案",
      "subtitle": "字幕文字",
      "music": "背景音乐建议"
    }
  ],
  "full_voiceover": "完整配音文案"
}
```

## 工作流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  热点追踪    │ → │  AI生成脚本  │ → │  素材准备    │ → │  FFmpeg合成  │
│  (抖音/微博) │    │  (分镜+文案) │    │  (AI图+配音) │    │  (最终视频)  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## 下一步计划

- [ ] 集成AI图像生成 (Stable Diffusion/ComfyUI)
- [ ] TTS语音合成自动配音
- [ ] 自动字幕生成
- [ ] 视频模板系统
- [ ] 定时自动运行 (Cron)

## 依赖

- Python 3.7+
- requests
- FFmpeg (已配置: `C:\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe`)

## 配置

配置文件位置: `C:\Users\ZhuanZ\.openclaw\workspace\config.json`

```json
{
  "ffmpegPath": "C:\\ffmpeg-8.1-essentials_build\\bin\\ffmpeg.exe"
}
```

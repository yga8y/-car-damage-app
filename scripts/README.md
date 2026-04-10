# FFmpeg 自动剪辑方案 - 安装指南

## 1. 安装 FFmpeg

### Windows 安装方法

#### 方法 A: 使用 Chocolatey（推荐）
```powershell
# 以管理员身份运行 PowerShell
choco install ffmpeg
```

#### 方法 B: 手动安装
1. 下载 FFmpeg: https://ffmpeg.org/download.html#build-windows
2. 解压到 `C:/ffmpeg`
3. 添加环境变量:
   - 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
   - 在 Path 中添加 `C:/ffmpeg/bin`
4. 重启终端，验证安装:
   ```
   ffmpeg -version
   ```

### macOS 安装
```bash
brew install ffmpeg
```

### Linux 安装
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

---

## 2. 安装 Python 依赖

```bash
# 不需要额外依赖，使用标准库即可
# 如果需要更高级功能，可以安装:
pip install ffmpeg-python
```

---

## 3. 测试脚本

```bash
cd ~/.openclaw/workspace/scripts
python auto_clipper.py
```

如果看到 "✓ AutoClipper 初始化完成！" 说明配置成功。

---

## 4. 功能演示

### 示例 1: 剪辑视频片段
```python
from auto_clipper import AutoClipper

clipper = AutoClipper()

# 从第10秒剪辑到第30秒
clipper.cut_video("input.mp4", start=10, end=30, output_name="clip.mp4")
```

### 示例 2: 批量剪辑（结合 AI 脚本）
```python
# 假设 AI 生成了多个片段时间点
segments = [
    {"start": 0, "end": 5, "name": "intro"},
    {"start": 5, "end": 15, "name": "content"},
    {"start": 15, "end": 20, "name": "outro"},
]

for seg in segments:
    clipper.cut_video(
        "input.mp4", 
        start=seg["start"], 
        end=seg["end"],
        output_name=f"{seg['name']}.mp4"
    )
```

### 示例 3: 添加字幕
```python
subtitles = [
    {"start": 0, "end": 3, "text": "大家好！"},
    {"start": 3, "end": 6, "text": "今天分享一个技巧"},
    {"start": 6, "end": 10, "text": "记得点赞关注哦"},
]

clipper.add_subtitles("video.mp4", subtitles, "with_subs.mp4")
```

### 示例 4: 生成抖音/快手格式
```python
# 9:16 竖屏格式
clipper.resize_video("input.mp4", 1080, 1920, "douyin.mp4")

# 或者 3:4 格式
clipper.resize_video("input.mp4", 1080, 1440, "kuaishou.mp4")
```

### 示例 5: 合并多个片段
```python
clips = ["intro.mp4", "content.mp4", "outro.mp4"]
clipper.merge_videos(clips, "final_video.mp4")
```

---

## 5. 完整工作流程（结合 AI 视频脚本）

```python
from auto_clipper import AutoClipper
import json

# 1. 使用 AI 生成视频脚本（分镜+时间点）
script = {
    "title": "AI工具介绍",
    "segments": [
        {"start": 0, "end": 5, "text": "大家好，今天介绍AI工具", "type": "intro"},
        {"start": 5, "end": 20, "text": "这个工具可以自动剪辑视频", "type": "content"},
        {"start": 20, "end": 25, "text": "记得关注我，下期见！", "type": "outro"},
    ]
}

# 2. 自动剪辑
clipper = AutoClipper(output_dir="./output")

# 3. 按脚本剪辑所有片段
clips = []
for i, seg in enumerate(script["segments"]):
    clip_path = clipper.cut_video(
        "raw_video.mp4",
        start=seg["start"],
        end=seg["end"],
        output_name=f"segment_{i}.mp4"
    )
    clips.append(clip_path)

# 4. 合并所有片段
final = clipper.merge_videos(clips, "final.mp4")

# 5. 添加字幕
subtitles = [{"start": s["start"], "end": s["end"], "text": s["text"]} 
             for s in script["segments"]]
final_with_subs = clipper.add_subtitles(final, subtitles, "final_with_subs.mp4")

# 6. 调整尺寸为抖音格式
douyin_version = clipper.resize_video(final_with_subs, 1080, 1920, "douyin_final.mp4")

print(f"✓ 视频制作完成: {douyin_version}")
```

---

## 6. 进阶功能

### 批量处理多个视频
```python
import os
from auto_clipper import AutoClipper

clipper = AutoClipper()
input_dir = "./raw_videos"

for video_file in os.listdir(input_dir):
    if video_file.endswith(".mp4"):
        input_path = os.path.join(input_dir, video_file)
        # 统一处理：剪辑前30秒+调整尺寸
        clipped = clipper.cut_video(input_path, 0, 30, f"clip_{video_file}")
        clipper.resize_video(clipped, 1080, 1920, f"douyin_{video_file}")
```

### 提取视频帧做封面
```python
frames = clipper.extract_frames("video.mp4", interval=5)  # 每5秒一帧
print(f"提取了 {len(frames)} 帧，可以选择作为封面")
```

---

## 7. 常见问题

### Q: 中文路径报错？
A: 脚本已处理中文路径，如果还有问题，将视频放在英文路径下。

### Q: 剪辑后的视频画质下降？
A: 使用 `-c copy` 参数时不重新编码，画质无损。如果需要重新编码，可以调整码率:
```python
# 在 auto_clipper.py 的 cut_video 方法中
# 将 "-c", "copy" 替换为:
# "-c:v", "libx264", "-crf", "18", "-preset", "fast"
```

### Q: 合并视频失败？
A: 确保所有视频格式、分辨率、编码一致。不一致时先统一转码:
```python
# 先统一转码再合并
for video in videos:
    clipper.resize_video(video, 1920, 1080, f"standard_{video}")
```

---

## 8. 下一步

1. 安装 FFmpeg
2. 运行 `python auto_clipper.py` 测试
3. 根据你的具体需求修改脚本
4. 结合 `ai-video-script` 技能实现全自动视频制作

需要我帮你定制特定功能的脚本吗？

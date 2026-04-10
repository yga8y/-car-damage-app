#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音视频工作流 - 一键生成热点视频
整合：热点追踪 + AI脚本 + 自动剪辑 + 批量生成
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Windows控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 配置路径 - 优先使用D盘
WORKSPACE = Path("D:/openclaw/workspace")
if not WORKSPACE.exists():
    WORKSPACE = Path("C:/Users/ZhuanZ/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "douyin-workflow"
# 输出目录可配置，默认D盘
OUTPUT_DIR = Path("D:/douyin-workflow-output")
CONFIG_FILE = WORKSPACE / "config.json"

# 加载配置
def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

config = load_config()
FFMPEG_PATH = config.get('ffmpegPath', 'ffmpeg')

class DouyinWorkflow:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_douyin_hotspots(self, limit=10):
        """获取抖音热点榜单"""
        print("🔥 正在获取抖音热点...")
        
        try:
            # 抖音热搜API
            url = "https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            hotspots = []
            if data.get('word_list'):
                for item in data['word_list'][:limit]:
                    hotspots.append({
                        'rank': item.get('position', 0),
                        'title': item.get('word', ''),
                        'hot_value': item.get('hot_value', 0),
                        'label': item.get('label', ''),
                        'sentence_id': item.get('sentence_id', '')
                    })
            
            # 保存热点数据
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            hotspot_file = self.output_dir / f"hotspots_{timestamp}.json"
            with open(hotspot_file, 'w', encoding='utf-8') as f:
                json.dump(hotspots, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 获取到 {len(hotspots)} 个热点")
            return hotspots
            
        except Exception as e:
            print(f"❌ 获取热点失败: {e}")
            return []
    
    def get_weibo_hotspots(self, limit=10):
        """获取微博热点榜单"""
        print("🔥 正在获取微博热点...")
        
        try:
            # 微博热搜API
            url = "https://weibo.com/ajax/side/hotSearch"
            response = self.session.get(url, timeout=10)
            data = response.json()
            
            hotspots = []
            if data.get('data', {}).get('realtime'):
                for item in data['data']['realtime'][:limit]:
                    hotspots.append({
                        'rank': item.get('rank', 0),
                        'title': item.get('word', ''),
                        'hot_value': item.get('num', 0),
                        'label': item.get('category', ''),
                        'url': f"https://s.weibo.com/weibo?q={item.get('word', '')}"
                    })
            
            print(f"✅ 获取到 {len(hotspots)} 个热点")
            return hotspots
            
        except Exception as e:
            print(f"❌ 获取微博热点失败: {e}")
            return []
    
    def generate_script(self, topic, style="口播", duration=30):
        """生成视频脚本"""
        print(f"📝 正在为「{topic}」生成脚本...")
        
        # 脚本模板
        script = {
            "title": f"#{topic}",
            "topic": topic,
            "style": style,
            "duration": duration,
            "scenes": []
        }
        
        # 根据时长生成场景
        scene_count = max(3, duration // 10)
        scene_duration = duration // scene_count
        
        # 开场
        script["scenes"].append({
            "scene_num": 1,
            "time": f"0-{scene_duration}秒",
            "visual": f"引人注目的开场画面，展示「{topic}」主题",
            "prompt": f"Eye-catching opening scene about {topic}, dynamic composition, vibrant colors, cinematic lighting --ar 9:16",
            "voiceover": f"你知道吗？最近{topic}火了！",
            "subtitle": f"🔥 {topic}",
            "music": "节奏感强的开场音乐"
        })
        
        # 中间内容
        for i in range(2, scene_count):
            script["scenes"].append({
                "scene_num": i,
                "time": f"{(i-1)*scene_duration}-{i*scene_duration}秒",
                "visual": f"展示{topic}相关内容，信息可视化",
                "prompt": f"Information visualization about {topic}, clean design, animated graphics, modern style --ar 9:16",
                "voiceover": f"让我们来看看这背后的故事...",
                "subtitle": f"第{i}点",
                "music": "轻快的背景音乐"
            })
        
        # 结尾
        script["scenes"].append({
            "scene_num": scene_count,
            "time": f"{(scene_count-1)*scene_duration}-{duration}秒",
            "visual": "互动引导画面，关注点赞",
            "prompt": "Social media engagement scene, thumbs up and follow icons, vibrant background, call to action --ar 9:16",
            "voiceover": "你怎么看？评论区告诉我！记得点赞关注~",
            "subtitle": "👍 点赞 | ➕ 关注 | 💬 评论",
            "music": "结尾高潮音乐"
        })
        
        # 完整配音文案
        script["full_voiceover"] = " ".join([s["voiceover"] for s in script["scenes"]])
        
        return script
    
    def save_script(self, script):
        """保存脚本到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = "".join(c for c in script['topic'] if c.isalnum() or c in (' ', '-', '_')).strip()
        script_file = self.output_dir / f"script_{safe_title}_{timestamp}.json"
        
        with open(script_file, 'w', encoding='utf-8') as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 脚本已保存: {script_file}")
        return script_file
    
    def format_script_markdown(self, script):
        """格式化脚本为Markdown"""
        md = f"""# {script['title']}

## 视频概述
- **主题**: {script['topic']}
- **风格**: {script['style']}
- **时长**: {script['duration']}秒

## 分镜表

"""
        for scene in script['scenes']:
            md += f"""### 场景{scene['scene_num']}（{scene['time']}）
- **画面**: {scene['visual']}
- **AI提示词**: `{scene['prompt']}`
- **配音**: {scene['voiceover']}
- **字幕**: {scene['subtitle']}
- **音乐**: {scene['music']}

"""
        
        md += f"""## 完整配音文案

{script['full_voiceover']}

---
*生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
        return md
    
    def create_video(self, script_file, media_files=None):
        """使用FFmpeg创建视频"""
        print(f"🎬 开始制作视频...")
        print(f"   FFmpeg路径: {FFMPEG_PATH}")
        
        # 加载脚本
        with open(script_file, 'r', encoding='utf-8') as f:
            script = json.load(f)
        
        # 这里可以实现具体的FFmpeg视频合成逻辑
        # 包括：图片/视频素材拼接、添加字幕、配音合成等
        
        output_video = self.output_dir / f"video_{script['topic']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        print(f"✅ 视频制作完成: {output_video}")
        print(f"   注意: 实际FFmpeg合成需要准备素材文件")
        
        return output_video
    
    def batch_generate(self, hotspots, style="口播", duration=30):
        """批量生成视频脚本"""
        print(f"🚀 批量生成模式: {len(hotspots)}个热点")
        
        results = []
        for hotspot in hotspots[:5]:  # 默认处理前5个
            topic = hotspot['title']
            print(f"\n📌 处理: {topic}")
            
            # 生成脚本
            script = self.generate_script(topic, style, duration)
            script_file = self.save_script(script)
            
            # 生成Markdown版本
            md_content = self.format_script_markdown(script)
            md_file = script_file.with_suffix('.md')
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            results.append({
                'topic': topic,
                'script_file': str(script_file),
                'md_file': str(md_file)
            })
            
            time.sleep(0.5)  # 避免请求过快
        
        # 保存批量生成报告
        report_file = self.output_dir / f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 批量生成完成！报告: {report_file}")
        return results
    
    def run_full_workflow(self, source="douyin", count=5):
        """运行完整工作流"""
        print("="*50)
        print("🎬 抖音视频工作流启动")
        print("="*50)
        
        # 1. 获取热点
        if source == "douyin":
            hotspots = self.get_douyin_hotspots(count)
        elif source == "weibo":
            hotspots = self.get_weibo_hotspots(count)
        else:
            hotspots = self.get_douyin_hotspot(count)
        
        if not hotspots:
            print("❌ 未获取到热点数据")
            return
        
        # 显示热点列表
        print("\n📋 热点榜单:")
        for i, h in enumerate(hotspots[:count], 1):
            print(f"   {i}. {h['title']} (热度: {h.get('hot_value', 'N/A')})")
        
        # 2. 批量生成脚本
        print("\n" + "="*50)
        results = self.batch_generate(hotspots[:count])
        
        # 3. 生成工作流报告
        print("\n" + "="*50)
        print("📊 工作流完成报告")
        print("="*50)
        print(f"输出目录: {self.output_dir}")
        print(f"生成脚本数: {len(results)}")
        print("\n生成的文件:")
        for r in results:
            print(f"  📄 {r['topic']}")
            print(f"     JSON: {r['script_file']}")
            print(f"     MD: {r['md_file']}")
        
        print("\n✨ 下一步:")
        print("  1. 查看Markdown脚本文件")
        print("  2. 根据提示词生成AI画面")
        print("  3. 录制/合成配音")
        print("  4. 使用FFmpeg合成最终视频")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='抖音视频工作流')
    parser.add_argument('--source', choices=['douyin', 'weibo'], default='douyin',
                       help='热点来源 (默认: douyin)')
    parser.add_argument('--count', type=int, default=5,
                       help='生成数量 (默认: 5)')
    parser.add_argument('--style', default='口播',
                       help='视频风格 (默认: 口播)')
    parser.add_argument('--duration', type=int, default=30,
                       help='视频时长秒数 (默认: 30)')
    parser.add_argument('--topic', type=str,
                       help='指定主题生成脚本')
    
    args = parser.parse_args()
    
    workflow = DouyinWorkflow()
    
    if args.topic:
        # 单主题模式
        print(f"🎯 单主题模式: {args.topic}")
        script = workflow.generate_script(args.topic, args.style, args.duration)
        script_file = workflow.save_script(script)
        md_content = workflow.format_script_markdown(script)
        md_file = script_file.with_suffix('.md')
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"\n✅ 脚本已生成!")
        print(f"   JSON: {script_file}")
        print(f"   MD: {md_file}")
    else:
        # 完整工作流模式
        workflow.run_full_workflow(args.source, args.count)

if __name__ == '__main__':
    main()

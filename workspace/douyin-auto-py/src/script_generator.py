"""
AI视频脚本生成模块
根据热点自动生成视频脚本
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict

# Windows编码兼容
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from hotspot import Hotspot


class VideoScript:
    """视频脚本模型"""
    def __init__(self, title: str, hotspot: Hotspot, duration: int = 30):
        self.title = title
        self.hotspot = hotspot
        self.duration = duration
        self.scenes = []
        self.tags = hotspot.tags
        self.generated_at = datetime.now().isoformat()
        self.suggested_title = f"{title} - 看完你就懂了！"
        self.suggested_desc = f"{hotspot.description}\n\n"
    
    def add_scene(self, time: str, content: str, visual: str, audio: str):
        """添加场景"""
        self.scenes.append({
            'time': time,
            'content': content,
            'visual': visual,
            'audio': audio
        })
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'hotspot': self.hotspot.to_dict(),
            'duration': self.duration,
            'scenes': self.scenes,
            'tags': self.tags,
            'generated_at': self.generated_at,
            'suggested_title': self.suggested_title,
            'suggested_desc': self.suggested_desc + ' #' + ' #'.join(self.tags) + ' #抖音热点'
        }


class ScriptGenerator:
    """脚本生成器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.scripts_dir = os.path.join(output_dir, "scripts")
        os.makedirs(self.scripts_dir, exist_ok=True)
    
    def generate_script(self, hotspot: Hotspot) -> VideoScript:
        """根据热点生成视频脚本"""
        print(f"[生成] 脚本: {hotspot.title}")
        
        script = VideoScript(
            title=hotspot.title,
            hotspot=hotspot,
            duration=30
        )
        
        # 场景1: 开场钩子 (0-5s)
        script.add_scene(
            time="0-5s",
            content=f"开场钩子：{hotspot.title} - 你知道吗？",
            visual="文字动画 + 吸睛背景",
            audio="热门BGM + 音效"
        )
        
        # 场景2: 核心内容 (5-15s)
        script.add_scene(
            time="5-15s",
            content=f"核心内容：{hotspot.description}",
            visual="相关图片/视频素材 + 关键文字",
            audio="解说配音或文字说明"
        )
        
        # 场景3: 深入分析 (15-25s)
        script.add_scene(
            time="15-25s",
            content="深入分析：提供独特观点或实用建议",
            visual="信息图表或演示画面",
            audio="继续解说"
        )
        
        # 场景4: 互动结尾 (25-30s)
        script.add_scene(
            time="25-30s",
            content="互动引导：你怎么看？评论区告诉我！",
            visual="关注按钮 + 点赞动画",
            audio="结尾音乐 + 关注号召"
        )
        
        # 保存脚本
        self.save_script(script)
        
        return script
    
    def generate_scripts(self, hotspots: List[Hotspot], limit: int = 3) -> List[VideoScript]:
        """批量生成脚本"""
        print(f"\n[批量] 开始生成视频脚本（前{limit}个热点）...\n")
        
        scripts = []
        top_hotspots = hotspots[:limit]
        
        for i, hotspot in enumerate(top_hotspots, 1):
            print(f"\n[{i}/{len(top_hotspots)}]")
            script = self.generate_script(hotspot)
            scripts.append(script)
            
            print(f"   建议标题: {script.suggested_title}")
            print(f"   时长: {script.duration}秒 | 场景: {len(script.scenes)}个")
        
        print(f"\n[完成] 已生成 {len(scripts)} 个脚本\n")
        return scripts
    
    def save_script(self, script: VideoScript):
        """保存脚本到文件"""
        filename = f"{int(datetime.now().timestamp())}-{script.title[:15].replace(' ', '_')}.json"
        filepath = os.path.join(self.scripts_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(script.to_dict(), f, ensure_ascii=False, indent=2)
        
        print(f"   [保存] 已保存: {filepath}")
    
    def generate_with_ai(self, hotspot: Hotspot) -> VideoScript:
        """使用AI生成更优质的脚本（需要接入AI API）"""
        print(f"[AI] 生成脚本: {hotspot.title}")
        print("[!] 提示：需要配置AI API密钥（OpenAI/文心一言/通义千问）")
        
        # TODO: 接入AI服务生成更优质内容
        return self.generate_script(hotspot)


if __name__ == "__main__":
    # 测试
    from hotspot import HotspotFetcher
    
    fetcher = HotspotFetcher()
    hotspots = fetcher.fetch_hotspots("mock")
    
    generator = ScriptGenerator()
    scripts = generator.generate_scripts(hotspots, 2)
    
    print("\n[摘要] 生成的脚本:")
    for i, script in enumerate(scripts, 1):
        print(f"\n脚本 {i}:")
        print(f"  标题: {script.suggested_title}")
        print(f"  场景:")
        for scene in script.scenes:
            print(f"    {scene['time']}: {scene['content'][:30]}...")

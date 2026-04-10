# DouyinAuto - 抖音视频全自动工作流
# 功能: 热点追踪 → AI脚本 → 自动剪辑 → 批量生成

import sys
sys.path.insert(0, r'C:\Users\ZhuanZ\.openclaw\workspace\scripts')

import json
import random
from datetime import datetime
from auto_clipper import AutoClipper

class DouyinWorkflow:
    """抖音视频自动化工作流"""
    
    def __init__(self, output_dir="./douyin_output"):
        self.clipper = AutoClipper(output_dir=output_dir)
        self.output_dir = output_dir
        
    # ========== 1. 热点库 ==========
    HOT_TOPICS = {
        "科技": [
            "AI人工智能改变生活",
            "新能源汽车技术突破", 
            "5G网络新应用",
            "智能家居新趋势",
            "元宇宙最新进展"
        ],
        "生活": [
            "省钱小妙招",
            "健康饮食习惯",
            "居家收纳技巧",
            "上班族必备神器",
            "周末去哪儿玩"
        ],
        "娱乐": [
            "热门影视剧解析",
            "明星八卦新鲜事",
            "搞笑段子合集",
            "音乐推荐榜单",
            "游戏攻略分享"
        ],
        "财经": [
            "股市行情分析",
            "理财入门知识",
            "副业赚钱方法",
            "创业经验分享",
            "房产投资趋势"
        ]
    }
    
    # ========== 2. 口播模板 ==========
    SCRIPT_TEMPLATES = {
        "开场": [
            "大家好，今天给大家分享一个超实用的内容",
            "你知道吗？最近这个事情火了",
            "哈喽，我是你们的老朋友",
            "今天这个视频一定要看完",
            "紧急通知！这件事和你有关"
        ],
        "过渡": [
            "重点来了，注意听",
            "很多人不知道的是",
            "接下来我说的很关键",
            "这里有个小技巧",
            "大家最关心的问题"
        ],
        "结尾": [
            "记得点赞收藏，下期见",
            "关注我，了解更多",
            "有问题评论区见",
            "觉得有用就分享吧",
            "我们下期再见"
        ]
    }
    
    def get_hot_topic(self, category=None):
        """获取热点话题"""
        if category and category in self.HOT_TOPICS:
            return random.choice(self.HOT_TOPICS[category])
        # 随机选择一个分类
        all_topics = [t for topics in self.HOT_TOPICS.values() for t in topics]
        return random.choice(all_topics)
    
    def generate_script(self, topic, duration=30):
        """根据话题生成口播脚本"""
        # 计算需要的片段数（每段5-8秒）
        segments = []
        current_time = 0
        
        # 开场（5秒）
        segments.append({
            "type": "开场",
            "text": random.choice(self.SCRIPT_TEMPLATES["开场"]),
            "start": current_time,
            "end": current_time + 5,
            "duration": 5
        })
        current_time += 5
        
        # 主体内容（15-20秒）
        content_texts = [
            f"关于{topic}，我总结了3个要点",
            f"首先，{topic}的核心是什么",
            f"其次，我们要注意这些问题",
            f"最后，给大家一个实用建议"
        ]
        
        for text in content_texts:
            if current_time >= duration - 5:
                break
            seg_duration = random.randint(4, 6)
            segments.append({
                "type": "内容",
                "text": text,
                "start": current_time,
                "end": min(current_time + seg_duration, duration - 5),
                "duration": seg_duration
            })
            current_time += seg_duration
        
        # 结尾（5秒）
        segments.append({
            "type": "结尾",
            "text": random.choice(self.SCRIPT_TEMPLATES["结尾"]),
            "start": current_time,
            "end": duration,
            "duration": duration - current_time
        })
        
        return {
            "topic": topic,
            "total_duration": duration,
            "segments": segments
        }
    
    def create_video_plan(self, num_videos=3):
        """创建视频制作计划"""
        plans = []
        for i in range(num_videos):
            topic = self.get_hot_topic()
            script = self.generate_script(topic)
            plans.append({
                "id": i + 1,
                "topic": topic,
                "script": script,
                "output_name": f"video_{i+1:02d}_{topic[:10]}.mp4"
            })
        return plans
    
    def process_video(self, input_video, plan, add_subs=True):
        """
        处理单个视频
        
        Args:
            input_video: 原始视频素材
            plan: 视频计划（包含脚本）
            add_subs: 是否添加字幕
        """
        print(f"\n{'='*50}")
        print(f"制作视频 #{plan['id']}: {plan['topic']}")
        print(f"{'='*50}")
        
        # 1. 根据脚本时长剪辑
        duration = plan['script']['total_duration']
        print(f"[1/4] 剪辑 {duration}秒 片段...")
        clipped = self.clipper.cut_video(
            input_video, 
            start=0, 
            end=duration,
            output_name=f"temp_{plan['id']}.mp4"
        )
        
        # 2. 调整为抖音格式（9:16）
        print(f"[2/4] 调整为抖音格式...")
        resized = self.clipper.resize_video(
            clipped,
            width=1080,
            height=1920,
            output_name=f"temp_{plan['id']}_9x16.mp4"
        )
        
        # 3. 添加字幕（可选）
        final_video = resized
        if add_subs:
            print(f"[3/4] 添加字幕...")
            subtitles = [
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"]
                }
                for seg in plan['script']['segments']
            ]
            try:
                final_video = self.clipper.add_subtitles(
                    resized,
                    subtitles,
                    output_name=plan['output_name']
                )
            except Exception as e:
                print(f"    字幕添加失败，使用无字幕版本: {e}")
                final_video = resized
        
        # 4. 生成视频信息
        print(f"[4/4] 生成视频信息...")
        info = {
            "filename": plan['output_name'],
            "topic": plan['topic'],
            "duration": duration,
            "script": plan['script'],
            "created_at": datetime.now().isoformat()
        }
        
        # 保存脚本文件
        script_file = f"{self.output_dir}/video_{plan['id']}_script.json"
        with open(script_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] 视频制作完成: {final_video}")
        print(f"[OK] 脚本保存: {script_file}")
        
        return final_video, info
    
    def batch_process(self, input_video, num_videos=3):
        """
        批量制作视频
        
        Args:
            input_video: 原始视频素材路径
            num_videos: 要生成的视频数量
        """
        print("="*60)
        print("     抖音视频全自动工作流")
        print("="*60)
        print(f"\n输入素材: {input_video}")
        print(f"计划生成: {num_videos} 个视频")
        print(f"输出目录: {self.output_dir}")
        print()
        
        # 1. 创建制作计划
        print("[步骤1] 生成视频计划...")
        plans = self.create_video_plan(num_videos)
        for plan in plans:
            print(f"  #{plan['id']}: {plan['topic']}")
        
        # 2. 批量处理
        print("\n[步骤2] 开始批量制作...")
        results = []
        for plan in plans:
            try:
                video_path, info = self.process_video(input_video, plan)
                results.append({"success": True, "video": video_path, "info": info})
            except Exception as e:
                print(f"[ERROR] 视频 #{plan['id']} 制作失败: {e}")
                results.append({"success": False, "error": str(e)})
        
        # 3. 生成报告
        print("\n" + "="*60)
        print("     制作完成报告")
        print("="*60)
        success_count = sum(1 for r in results if r['success'])
        print(f"成功: {success_count}/{num_videos}")
        print()
        
        for i, result in enumerate(results):
            if result['success']:
                info = result['info']
                print(f"✓ 视频 {i+1}: {info['filename']}")
                print(f"  话题: {info['topic']}")
                print(f"  时长: {info['duration']}秒")
            else:
                print(f"✗ 视频 {i+1}: 失败 - {result['error']}")
        
        print("\n" + "="*60)
        print("所有视频制作完成！")
        print(f"输出目录: {self.output_dir}")
        print("="*60)
        
        return results


# ========== 使用示例 ==========

def demo():
    """演示完整工作流"""
    
    # 创建工作流实例
    workflow = DouyinWorkflow(output_dir="./douyin_videos")
    
    # 使用测试视频作为素材
    input_video = "test_video.mp4"
    
    # 批量制作3个视频
    workflow.batch_process(input_video, num_videos=3)
    
    print("\n提示: 将你自己的视频素材重命名为 'test_video.mp4' 或修改代码中的路径")


if __name__ == "__main__":
    demo()

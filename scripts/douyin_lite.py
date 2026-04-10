# DouyinWorkflowLite - 抖音视频工作流（简化版）
# 使用已测试成功的功能：剪辑 + 调整尺寸

import sys
sys.path.insert(0, r'C:\Users\ZhuanZ\.openclaw\workspace\scripts')

import random
from auto_clipper import AutoClipper

class DouyinWorkflowLite:
    """简化版抖音工作流"""
    
    def __init__(self, output_dir="./douyin_videos"):
        self.clipper = AutoClipper(output_dir=output_dir)
        
    # 热点话题库
    TOPICS = [
        "AI人工智能改变生活",
        "省钱小妙招",
        "健康饮食习惯", 
        "热门影视剧解析",
        "股市行情分析",
        "居家收纳技巧",
        "副业赚钱方法",
        "周末去哪儿玩"
    ]
    
    def generate_batch(self, input_video, num_videos=3):
        """批量生成抖音视频"""
        print("="*60)
        print("     抖音视频批量生成器")
        print("="*60)
        print(f"\n输入素材: {input_video}")
        print(f"生成数量: {num_videos} 个")
        print()
        
        results = []
        
        for i in range(num_videos):
            topic = random.choice(self.TOPICS)
            print(f"\n[{i+1}/{num_videos}] 制作: {topic}")
            print("-" * 40)
            
            try:
                # 1. 剪辑15-30秒片段
                duration = random.randint(15, 30)
                print(f"  [1/2] 剪辑 {duration}秒 片段...")
                
                clip_name = f"clip_{i+1:02d}.mp4"
                clip_path = self.clipper.cut_video(
                    input_video,
                    start=0,
                    end=duration,
                    output_name=clip_name
                )
                
                # 2. 调整为抖音9:16格式
                print(f"  [2/2] 调整为抖音格式...")
                
                final_name = f"douyin_{topic[:10]}_{i+1:02d}.mp4"
                final_path = self.clipper.resize_video(
                    clip_path,
                    width=1080,
                    height=1920,
                    output_name=final_name
                )
                
                results.append({
                    "success": True,
                    "topic": topic,
                    "file": final_path,
                    "duration": duration
                })
                print(f"  [OK] 完成: {final_name}")
                
            except Exception as e:
                print(f"  [ERROR] 失败: {e}")
                results.append({
                    "success": False,
                    "error": str(e)
                })
        
        # 生成报告
        print("\n" + "="*60)
        print("     生成完成报告")
        print("="*60)
        
        success = sum(1 for r in results if r['success'])
        print(f"成功: {success}/{num_videos}\n")
        
        for i, r in enumerate(results):
            if r['success']:
                print(f"  {i+1}. {r['topic']} ({r['duration']}秒)")
            else:
                print(f"  {i+1}. [失败] {r.get('error', '未知错误')}")
        
        print(f"\n输出目录: {self.clipper.output_dir}")
        print("="*60)
        
        return results


def demo():
    """演示"""
    workflow = DouyinWorkflowLite()
    
    # 使用测试视频
    workflow.generate_batch("test_video.mp4", num_videos=3)
    
    print("\n提示: 将你自己的视频重命名为 'test_video.mp4' 即可处理")


if __name__ == "__main__":
    demo()

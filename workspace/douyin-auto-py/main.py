"""
抖音自动化系统 - 主程序
整合热点获取、脚本生成、视频制作、自动发布
"""

import argparse
import sys
import os

# 设置UTF-8编码（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from hotspot import HotspotFetcher
from script_generator import ScriptGenerator
from video_producer import VideoProducer
from publisher import DouyinPublisher


class DouyinAutomation:
    """抖音自动化系统"""
    
    def __init__(self):
        self.fetcher = HotspotFetcher()
        self.generator = ScriptGenerator()
        self.producer = VideoProducer()
        self.publisher = DouyinPublisher()
    
    def run_full_workflow(self, hotspot_limit: int = 3, generate_limit: int = 2, 
                          create_video: bool = False, publish: bool = False):
        """运行完整工作流"""
        print("=" * 40)
        print("     抖音自动化系统 v1.0")
        print("=" * 40 + "\n")
        
        try:
            # 步骤1: 获取热点
            print("=== 步骤1: 获取抖音热点 ===\n")
            hotspots = self.fetcher.fetch_hotspots("mock")
            
            if not hotspots:
                print("[错误] 没有获取到热点，工作流终止")
                return
            
            # 分析热点
            analysis = self.fetcher.analyze_trends(hotspots)
            print("\n[分析] 热点统计:")
            print(f"   总热点数: {analysis['total']}")
            print(f"   分类分布: {analysis['categories']}")
            print(f"   最高热度: {analysis['top_heat']:,}")
            print(f"   平均热度: {analysis['avg_heat']:,}")
            
            # 步骤2: 生成脚本
            print("\n=== 步骤2: AI生成视频脚本 ===")
            scripts = self.generator.generate_scripts(hotspots, generate_limit)
            
            # 步骤3: 制作视频（可选）
            if create_video and scripts:
                print("\n=== 步骤3: 制作视频 ===")
                results = self.producer.batch_create(scripts)
            
            # 步骤4: 发布（可选）
            if publish:
                print("\n=== 步骤4: 发布视频 ===")
                print("[!] 发布功能需要配置抖音账号")
            
            # 完成
            print("\n" + "=" * 40)
            print("[完成] 工作流执行完毕！")
            print("=" * 40)
            print("\n[输出] 文件位置:")
            print("   - 热点数据: output/hotspots.json")
            print("   - 视频脚本: output/scripts/")
            if create_video:
                print("   - 视频文件: output/videos/")
            
            print("\n[提示] 下一步:")
            print("   1. 查看生成的脚本")
            print("   2. 接入真实热点API")
            print("   3. 接入AI服务优化内容")
            print("   4. 安装FFmpeg生成视频")
            print("   5. 配置抖音账号自动发布")
            
        except Exception as e:
            print(f"\n[错误] 工作流出错: {e}")
            import traceback
            traceback.print_exc()
    
    def fetch_hotspots_only(self):
        """仅获取热点"""
        self.fetcher.fetch_hotspots("mock")
    
    def generate_scripts_only(self, limit: int = 3):
        """仅从缓存生成脚本"""
        hotspots = self.fetcher.load_hotspots()
        if hotspots:
            self.generator.generate_scripts(hotspots, limit)
        else:
            print("[错误] 没有缓存的热点数据，请先运行获取热点")
    
    def setup(self):
        """初始化设置"""
        print("[设置] 初始化抖音自动化系统...\n")
        
        # 创建目录结构
        dirs = [
            "output/scripts",
            "output/videos",
            "config",
            "assets/videos/backgrounds",
            "assets/music/bgm",
            "assets/fonts"
        ]
        
        for d in dirs:
            os.makedirs(d, exist_ok=True)
        
        print("[完成] 目录结构已创建")
        
        # 准备素材
        self.producer.prepare_assets()
        
        print("\n[完成] 系统初始化完成！")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='抖音自动化系统')
    parser.add_argument('command', choices=['full', 'hotspot', 'generate', 'setup'],
                        default='full', nargs='?',
                        help='运行模式: full(完整工作流), hotspot(仅获取热点), generate(生成脚本), setup(初始化)')
    parser.add_argument('--limit', '-l', type=int, default=2,
                        help='生成脚本数量限制 (默认: 2)')
    parser.add_argument('--video', '-v', action='store_true',
                        help='同时生成视频')
    parser.add_argument('--publish', '-p', action='store_true',
                        help='自动发布到抖音')
    
    args = parser.parse_args()
    
    automation = DouyinAutomation()
    
    if args.command == 'full':
        automation.run_full_workflow(
            generate_limit=args.limit,
            create_video=args.video,
            publish=args.publish
        )
    elif args.command == 'hotspot':
        automation.fetch_hotspots_only()
    elif args.command == 'generate':
        automation.generate_scripts_only(args.limit)
    elif args.command == 'setup':
        automation.setup()


if __name__ == "__main__":
    main()

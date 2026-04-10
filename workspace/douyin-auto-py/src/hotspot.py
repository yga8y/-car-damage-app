"""
抖音热点获取模块
支持多种数据源：模拟数据、API接口、网页抓取
"""

import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

# Windows编码兼容
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class Hotspot:
    """热点数据模型"""
    def __init__(self, rank: int, title: str, heat: int, category: str, 
                 tags: List[str], description: str):
        self.rank = rank
        self.title = title
        self.heat = heat
        self.category = category
        self.tags = tags
        self.description = description
    
    def to_dict(self) -> Dict:
        return {
            'rank': self.rank,
            'title': self.title,
            'heat': self.heat,
            'category': self.category,
            'tags': self.tags,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Hotspot':
        return cls(**data)


class HotspotFetcher:
    """热点获取器"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self.cache_file = os.path.join(output_dir, "hotspots.json")
        os.makedirs(output_dir, exist_ok=True)
    
    def fetch_mock_data(self) -> List[Hotspot]:
        """获取模拟热点数据（用于测试）"""
        print("[数据] 获取抖音热点数据...\n")
        
        mock_data = [
            Hotspot(
                rank=1,
                title="AI机器人会取代人类工作吗",
                heat=12500000,
                category="科技",
                tags=["AI", "人工智能", "未来"],
                description="讨论AI技术对就业市场的影响"
            ),
            Hotspot(
                rank=2,
                title="春季养生食谱推荐",
                heat=9800000,
                category="美食",
                tags=["养生", "健康", "食谱"],
                description="春天吃什么最养生"
            ),
            Hotspot(
                rank=3,
                title="职场沟通技巧大全",
                heat=8500000,
                category="职场",
                tags=["职场", "沟通", "技巧"],
                description="如何在职场中更好地沟通"
            ),
            Hotspot(
                rank=4,
                title="30天健身挑战",
                heat=7200000,
                category="健身",
                tags=["健身", "挑战", "减肥"],
                description="30天练出好身材"
            ),
            Hotspot(
                rank=5,
                title="省钱小妙招",
                heat=6500000,
                category="生活",
                tags=["省钱", "生活", "技巧"],
                description="日常生活中的省钱技巧"
            )
        ]
        return mock_data
    
    def fetch_from_api(self) -> List[Hotspot]:
        """从API获取热点（需要接入真实数据源）"""
        print("[API] 尝试从API获取热点...")
        print("[!] 提示：需要配置API密钥")
        return self.fetch_mock_data()
    
    def fetch_hotspots(self, source: str = "mock") -> List[Hotspot]:
        """获取热点主函数"""
        if source == "mock":
            hotspots = self.fetch_mock_data()
        elif source == "api":
            hotspots = self.fetch_from_api()
        else:
            hotspots = self.fetch_mock_data()
        
        # 保存到文件
        self.save_hotspots(hotspots)
        
        # 打印热点列表
        print("[热点] 当前抖音热点 TOP 5:\n")
        for h in hotspots:
            print(f"  {h.rank}. {h.title}")
            print(f"     热度: {h.heat:,} | 分类: {h.category}")
            print(f"     标签: {' #'.join(h.tags)}")
            print()
        
        return hotspots
    
    def save_hotspots(self, hotspots: List[Hotspot]):
        """保存热点数据到文件"""
        data = {
            'source': 'mock-data',
            'timestamp': datetime.now().isoformat(),
            'hotspots': [h.to_dict() for h in hotspots]
        }
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"[保存] 热点数据已保存: {self.cache_file}\n")
    
    def load_hotspots(self) -> Optional[List[Hotspot]]:
        """从文件加载热点数据"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Hotspot.from_dict(h) for h in data['hotspots']]
        except FileNotFoundError:
            print("[!] 没有缓存数据，请先获取热点")
            return None
    
    def analyze_trends(self, hotspots: List[Hotspot]) -> Dict:
        """分析热点趋势"""
        categories = {}
        for h in hotspots:
            categories[h.category] = categories.get(h.category, 0) + 1
        
        return {
            'total': len(hotspots),
            'categories': categories,
            'top_heat': hotspots[0].heat if hotspots else 0,
            'avg_heat': sum(h.heat for h in hotspots) // len(hotspots) if hotspots else 0
        }


if __name__ == "__main__":
    fetcher = HotspotFetcher()
    hotspots = fetcher.fetch_hotspots("mock")
    
    print("\n[分析] 热点统计:")
    analysis = fetcher.analyze_trends(hotspots)
    print(f"  总热点数: {analysis['total']}")
    print(f"  分类分布: {analysis['categories']}")
    print(f"  最高热度: {analysis['top_heat']:,}")
    print(f"  平均热度: {analysis['avg_heat']:,}")

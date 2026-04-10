#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音热点监控器 - 简化版
使用模拟数据进行演示
"""

import json
import os
from datetime import datetime


def get_mock_hotspots():
    """获取模拟热点数据"""
    mock_data = [
        {"rank": 1, "title": "春节放假安排公布", "hot_value": 12500000, "label": "热"},
        {"rank": 2, "title": "新电影票房破纪录", "hot_value": 10800000, "label": "热"},
        {"rank": 3, "title": "科技新品发布会", "hot_value": 9500000, "label": "热"},
        {"rank": 4, "title": "明星婚礼现场曝光", "hot_value": 8200000, "label": "新"},
        {"rank": 5, "title": "美食探店推荐", "hot_value": 7800000, "label": "新"},
        {"rank": 6, "title": "旅游攻略分享", "hot_value": 6500000, "label": ""},
        {"rank": 7, "title": "搞笑视频合集", "hot_value": 6200000, "label": ""},
        {"rank": 8, "title": "萌宠日常记录", "hot_value": 5800000, "label": ""},
        {"rank": 9, "title": "化妆教程分享", "hot_value": 5400000, "label": "新"},
        {"rank": 10, "title": "健身打卡挑战", "hot_value": 5100000, "label": ""},
        {"rank": 11, "title": "读书推荐清单", "hot_value": 4800000, "label": ""},
        {"rank": 12, "title": "音乐翻唱热门", "hot_value": 4500000, "label": ""},
        {"rank": 13, "title": "手工DIY教程", "hot_value": 4200000, "label": ""},
        {"rank": 14, "title": "游戏直播精彩", "hot_value": 3900000, "label": ""},
        {"rank": 15, "title": "汽车评测视频", "hot_value": 3600000, "label": ""},
        {"rank": 16, "title": "家居装修分享", "hot_value": 3300000, "label": ""},
        {"rank": 17, "title": "育儿经验交流", "hot_value": 3000000, "label": ""},
        {"rank": 18, "title": "职场干货分享", "hot_value": 2800000, "label": "新"},
        {"rank": 19, "title": "摄影技巧教学", "hot_value": 2500000, "label": ""},
        {"rank": 20, "title": "穿搭灵感分享", "hot_value": 2200000, "label": ""},
    ]
    
    # 添加时间戳和URL
    for item in mock_data:
        item['timestamp'] = datetime.now().isoformat()
        item['url'] = f"https://www.douyin.com/search/{item['title']}"
    
    return mock_data


def save_data(hotspots, output_dir='output'):
    """保存数据到JSON文件"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_dir, f'hotspots_{timestamp}.json')
    
    data = {
        'fetch_time': datetime.now().isoformat(),
        'source': 'douyin_mock',
        'total_count': len(hotspots),
        'hotspots': hotspots
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 数据已保存: {filename}")
    return filename


def generate_simple_report(hotspots, output_dir='output'):
    """生成简单的文本报告"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
    filename = os.path.join(output_dir, 'hotspot_report.txt')
    
    report = []
    report.append("=" * 60)
    report.append("抖音热点监控报告")
    report.append("=" * 60)
    report.append(f"生成时间: {timestamp}")
    report.append(f"热点总数: {len(hotspots)}")
    report.append("-" * 60)
    
    for hotspot in hotspots:
        label = f"[{hotspot['label']}]" if hotspot['label'] else "   "
        hot_str = f"{hotspot['hot_value']/10000:.1f}万" if hotspot['hot_value'] >= 10000 else str(hotspot['hot_value'])
        report.append(f"{hotspot['rank']:2d}. {hotspot['title']:<20} {label} 🔥{hot_str}")
    
    report.append("-" * 60)
    report.append("数据来源: 模拟数据 (用于演示)")
    report.append("=" * 60)
    
    content = '\n'.join(report)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 报告已生成: {filename}")
    return filename


def main():
    """主函数"""
    print("=" * 60)
    print("抖音热点监控器 (简化版)")
    print("=" * 60)
    
    # 获取热点数据
    hotspots = get_mock_hotspots()
    
    # 保存数据
    json_file = save_data(hotspots)
    
    # 生成报告
    report_file = generate_simple_report(hotspots)
    
    print("\n" + "=" * 60)
    print("✅ 完成!")
    print(f"📄 JSON数据: {json_file}")
    print(f"📄 文本报告: {report_file}")
    print("=" * 60)
    
    # 显示TOP10
    print("\n🔥 当前TOP10热点:")
    for hotspot in hotspots[:10]:
        label = f"[{hotspot['label']}]" if hotspot['label'] else "   "
        hot_str = f"{hotspot['hot_value']/10000:.1f}万"
        print(f"  {hotspot['rank']:2d}. {hotspot['title']:<20} {label} 🔥{hot_str}")


if __name__ == '__main__':
    main()

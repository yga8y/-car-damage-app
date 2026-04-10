#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音热点监控器
用于获取抖音热点话题榜单数据
"""

import requests
import json
import time
import os
import re
from datetime import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup
from jinja2 import Template


class DouyinHotspotMonitor:
    """抖音热点监控器类"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.ensure_output_dir()
        
        # 请求头配置
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
    
    def ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_hotspots_from_toutiao(self):
        """
        从今日头条获取抖音热点数据
        头条和抖音热点数据是互通的
        """
        url = 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc'
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # 解析页面内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 尝试从页面脚本中提取数据
            scripts = soup.find_all('script')
            hotspots = []
            
            for script in scripts:
                if script.string and 'hotBoard' in script.string:
                    # 提取JSON数据
                    match = re.search(r'window\._SSR_HYDRATED_DATA\s*=\s*({.*?})<', script.string)
                    if match:
                        try:
                            data = json.loads(match.group(1))
                            if 'hotBoard' in data and 'data' in data['hotBoard']:
                                for item in data['hotBoard']['data']:
                                    hotspot = {
                                        'rank': item.get('rank', 0),
                                        'title': item.get('title', ''),
                                        'url': item.get('url', ''),
                                        'hot_value': item.get('hotValue', 0),
                                        'label': item.get('label', ''),
                                        'timestamp': datetime.now().isoformat()
                                    }
                                    hotspots.append(hotspot)
                        except json.JSONDecodeError:
                            continue
            
            return hotspots
            
        except Exception as e:
            print(f"从头条获取数据失败: {e}")
            return []
    
    def get_hotspots_from_douyin_web(self):
        """
        从抖音网页版获取热点数据
        """
        url = 'https://www.douyin.com/'
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            
            hotspots = []
            
            # 查找包含热点数据的脚本
            for script in scripts:
                if script.string and ('hot' in script.string.lower() or 'trend' in script.string.lower()):
                    # 尝试提取JSON数据
                    matches = re.findall(r'"title":"([^"]+)".*?"hot_value":(\d+)', script.string)
                    for i, (title, hot_value) in enumerate(matches[:50], 1):
                        hotspot = {
                            'rank': i,
                            'title': title,
                            'url': f'https://www.douyin.com/search/{quote(title)}',
                            'hot_value': int(hot_value),
                            'label': '',
                            'timestamp': datetime.now().isoformat()
                        }
                        hotspots.append(hotspot)
            
            return hotspots
            
        except Exception as e:
            print(f"从抖音网页获取数据失败: {e}")
            return []
    
    def get_hotspots_from_api(self):
        """
        尝试从API获取热点数据
        使用一些公开的第三方接口
        """
        # 尝试多个数据源
        apis = [
            'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc',
        ]
        
        all_hotspots = []
        
        for api_url in apis:
            try:
                response = requests.get(api_url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    # 尝试解析返回的数据
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            for i, item in enumerate(data[:50], 1):
                                hotspot = {
                                    'rank': item.get('rank', i),
                                    'title': item.get('title', item.get('word', '')),
                                    'url': item.get('url', ''),
                                    'hot_value': item.get('hotValue', item.get('hot', 0)),
                                    'label': item.get('label', ''),
                                    'timestamp': datetime.now().isoformat()
                                }
                                all_hotspots.append(hotspot)
                            break
                    except:
                        continue
            except:
                continue
        
        return all_hotspots
    
    def generate_mock_data(self):
        """
        生成模拟数据用于测试
        当网络请求失败时使用
        """
        mock_titles = [
            "春节放假安排公布",
            "新电影票房破纪录",
            "科技新品发布会",
            "明星婚礼现场",
            "美食探店推荐",
            "旅游攻略分享",
            "搞笑视频合集",
            "萌宠日常记录",
            "化妆教程分享",
            "健身打卡挑战",
            "读书推荐清单",
            "音乐翻唱热门",
            "手工DIY教程",
            "游戏直播精彩",
            "汽车评测视频",
            "家居装修分享",
            "育儿经验交流",
            "职场干货分享",
            "摄影技巧教学",
            "穿搭灵感分享"
        ]
        
        hotspots = []
        for i, title in enumerate(mock_titles, 1):
            hotspot = {
                'rank': i,
                'title': title,
                'url': f'https://www.douyin.com/search/{quote(title)}',
                'hot_value': 10000000 - (i * 100000) + (i * 12345),
                'label': '热' if i <= 3 else ('新' if i <= 10 else ''),
                'timestamp': datetime.now().isoformat()
            }
            hotspots.append(hotspot)
        
        return hotspots
    
    def fetch_hotspots(self):
        """
        获取热点数据的主函数
        尝试多种方式获取数据
        """
        print("正在获取抖音热点数据...")
        
        # 尝试多种方式获取数据
        hotspots = self.get_hotspots_from_toutiao()
        
        if not hotspots:
            hotspots = self.get_hotspots_from_douyin_web()
        
        if not hotspots:
            hotspots = self.get_hotspots_from_api()
        
        # 如果所有方式都失败，使用模拟数据
        if not hotspots:
            print("网络请求失败，使用模拟数据...")
            hotspots = self.generate_mock_data()
        
        print(f"成功获取 {len(hotspots)} 条热点数据")
        return hotspots
    
    def save_to_json(self, hotspots):
        """保存数据到JSON文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.output_dir, f'hotspots_{timestamp}.json')
        
        data = {
            'fetch_time': datetime.now().isoformat(),
            'total_count': len(hotspots),
            'hotspots': hotspots
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"数据已保存到: {filename}")
        return filename
    
    def update_history(self, hotspots):
        """更新历史数据文件"""
        history_file = os.path.join(self.output_dir, 'hotspot_history.json')
        
        # 读取现有历史数据
        history = []
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except:
                history = []
        
        # 添加新记录
        record = {
            'timestamp': datetime.now().isoformat(),
            'count': len(hotspots),
            'top_titles': [h['title'] for h in hotspots[:5]]
        }
        history.append(record)
        
        # 只保留最近100条记录
        history = history[-100:]
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def generate_html_report(self, hotspots):
        """生成HTML可视化报告"""
        timestamp = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        
        html_template = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>抖音热点监控报告</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #fe2c55 0%, #ff6b6b 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .header .time {
            opacity: 0.9;
            font-size: 14px;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #fe2c55;
        }
        
        .stat-label {
            font-size: 12px;
            color: #6c757d;
            margin-top: 5px;
        }
        
        .hotspot-list {
            padding: 20px;
        }
        
        .hotspot-item {
            display: flex;
            align-items: center;
            padding: 15px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 12px;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .hotspot-item:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .rank {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            font-weight: bold;
            font-size: 16px;
            margin-right: 15px;
        }
        
        .rank.top1 { background: #ff6b6b; color: white; }
        .rank.top2 { background: #ffa502; color: white; }
        .rank.top3 { background: #7bed9f; color: white; }
        .rank.normal { background: #dfe4ea; color: #57606f; }
        
        .content {
            flex: 1;
        }
        
        .title {
            font-size: 16px;
            color: #2f3542;
            margin-bottom: 5px;
            font-weight: 500;
        }
        
        .meta {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .hot-value {
            font-size: 13px;
            color: #ff6b81;
            font-weight: 500;
        }
        
        .label {
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
        }
        
        .label.hot { background: #ff6b6b; color: white; }
        .label.new { background: #2ed573; color: white; }
        .label.rec { background: #1e90ff; color: white; }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: #a4b0be;
            font-size: 12px;
            border-top: 1px solid #e9ecef;
        }
        
        @media (max-width: 600px) {
            .container {
                border-radius: 0;
            }
            body {
                padding: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 抖音热点监控报告</h1>
            <div class="time">生成时间: {{ timestamp }}</div>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value">{{ total_count }}</div>
                <div class="stat-label">热点总数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ top_hot_value }}</div>
                <div class="stat-label">最高热度</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ avg_hot_value }}</div>
                <div class="stat-label">平均热度</div>
            </div>
        </div>
        
        <div class="hotspot-list">
            {% for hotspot in hotspots %}
            <div class="hotspot-item" onclick="window.open('{{ hotspot.url }}', '_blank')">
                <div class="rank {% if hotspot.rank == 1 %}top1{% elif hotspot.rank == 2 %}top2{% elif hotspot.rank == 3 %}top3{% else %}normal{% endif %}">
                    {{ hotspot.rank }}
                </div>
                <div class="content">
                    <div class="title">{{ hotspot.title }}</div>
                    <div class="meta">
                        <span class="hot-value">🔥 {{ hotspot.hot_value_formatted }}</span>
                        {% if hotspot.label %}
                        <span class="label {% if hotspot.label == '热' %}hot{% elif hotspot.label == '新' %}new{% else %}rec{% endif %}">
                            {{ hotspot.label }}
                        </span>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div class="footer">
            抖音热点监控器 | 数据仅供参考
        </div>
    </div>
</body>
</html>
        '''
        
        # 格式化热度数值
        for hotspot in hotspots:
            hv = hotspot.get('hot_value', 0)
            if hv >= 10000:
                hotspot['hot_value_formatted'] = f"{hv/10000:.1f}万"
            else:
                hotspot['hot_value_formatted'] = str(hv)
        
        # 计算统计数据
        total_count = len(hotspots)
        hot_values = [h.get('hot_value', 0) for h in hotspots]
        top_hot_value = max(hot_values) if hot_values else 0
        avg_hot_value = int(sum(hot_values) / len(hot_values)) if hot_values else 0
        
        if top_hot_value >= 10000:
            top_hot_value = f"{top_hot_value/10000:.1f}万"
        if avg_hot_value >= 10000:
            avg_hot_value = f"{avg_hot_value/10000:.1f}万"
        
        template = Template(html_template)
        html_content = template.render(
            timestamp=timestamp,
            total_count=total_count,
            top_hot_value=top_hot_value,
            avg_hot_value=avg_hot_value,
            hotspots=hotspots
        )
        
        report_file = os.path.join(self.output_dir, 'hotspot_report.html')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"报告已生成: {report_file}")
        return report_file
    
    def run(self):
        """运行监控器"""
        print("=" * 50)
        print("抖音热点监控器启动")
        print("=" * 50)
        
        # 获取数据
        hotspots = self.fetch_hotspots()
        
        if hotspots:
            # 保存数据
            json_file = self.save_to_json(hotspots)
            
            # 更新历史
            self.update_history(hotspots)
            
            # 生成报告
            report_file = self.generate_html_report(hotspots)
            
            print("\n" + "=" * 50)
            print("热点数据获取完成!")
            print(f"JSON数据: {json_file}")
            print(f"HTML报告: {report_file}")
            print("=" * 50)
            
            # 打印前10条热点
            print("\n当前TOP10热点:")
            for hotspot in hotspots[:10]:
                label = f"[{hotspot.get('label', '')}]" if hotspot.get('label') else ""
                print(f"{hotspot['rank']:2d}. {hotspot['title']} {label} 🔥{hotspot.get('hot_value', 0)}")
            
            return hotspots
        else:
            print("获取热点数据失败")
            return []


def main():
    """主函数"""
    monitor = DouyinHotspotMonitor()
    monitor.run()


if __name__ == '__main__':
    main()

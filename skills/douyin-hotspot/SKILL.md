# Douyin Hotspot Monitor - 抖音热点监控器

## Description

监控抖音热点话题，获取实时热搜榜单数据，并生成可视化报告。

## Usage

```bash
# 获取当前热点数据
python skills/douyin-hotspot/douyin_hotspot.py

# 查看生成的报告
open skills/douyin-hotspot/output/hotspot_report.html
```

## Features

- 自动获取抖音热点榜单数据
- 保存数据到本地JSON文件
- 生成HTML可视化报告
- 支持历史数据对比

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- jinja2

## Installation

```bash
pip install -r skills/douyin-hotspot/requirements.txt
```

## Output Files

- `output/hotspots_YYYYMMDD_HHMMSS.json` - 原始数据
- `output/hotspot_report.html` - 可视化报告
- `output/hotspot_history.json` - 历史数据汇总

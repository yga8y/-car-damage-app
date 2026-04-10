#!/usr/bin/env python3
"""
Search for CarDD dataset on Chinese cloud storage
Common patterns for Baidu Pan and Aliyun Drive
"""

import urllib.request
import urllib.error
import ssl
from pathlib import Path

project_dir = Path(__file__).parent.parent
dataset_dir = project_dir / "datasets" / "CarDD"

def check_url_accessible(url):
    """Check if URL is accessible"""
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers, method='HEAD')
        response = urllib.request.urlopen(req, context=ssl_context, timeout=10)
        return True
    except:
        return False

def try_common_links():
    """Try common CarDD dataset links"""
    
    # Common Baidu Pan link patterns (these are examples, real links need to be found)
    potential_links = [
        # Baidu Pan patterns
        "https://pan.baidu.com/s/1CarDD_Dataset",
        "https://pan.baidu.com/s/1CarDD2023",
        "https://pan.baidu.com/s/1CarDD_ustc",
        
        # Aliyun Drive patterns
        "https://www.aliyundrive.com/s/CarDD",
        "https://www.alipan.com/s/CarDD",
        
        # Quark Pan
        "https://pan.quark.cn/s/CarDD",
        
        # 123Pan
        "https://www.123pan.com/s/CarDD",
        
        # Lanzhou (蓝奏云)
        "https://www.lanzoui.com/s/CarDD",
    ]
    
    print("Checking potential links...")
    accessible = []
    
    for url in potential_links:
        print(f"  Checking: {url}")
        if check_url_accessible(url):
            print(f"    [OK] Accessible!")
            accessible.append(url)
        else:
            print(f"    [X] Not accessible")
    
    return accessible

def print_search_guide():
    """Print search guide for manual search"""
    print("""
======================================================================
Search CarDD Dataset on Chinese Platforms
======================================================================

Search Keywords (搜索关键词):
  中文: "CarDD数据集 百度网盘"
        "CarDD数据集 阿里云盘"
        "CarDD数据集 下载"
        "车辆损伤检测数据集 百度网盘"
        "CarDD 王新宽 数据集"
  
  English: "CarDD dataset baidu pan"
           "CarDD dataset download"
           "CarDD vehicle damage dataset"

Platforms to Search (搜索平台):
  1. Baidu (百度搜索)
     https://www.baidu.com
     Search: "CarDD数据集 百度网盘"
  
  2. Bing China (必应中国)
     https://cn.bing.com
     Search: "CarDD dataset 阿里云盘"
  
  3. Zhihu (知乎)
     https://www.zhihu.com
     Search: "CarDD数据集"
  
  4. CSDN
     https://www.csdn.net
     Search: "CarDD车辆损伤数据集"
  
  5. Bilibili (哔哩哔哩)
     https://search.bilibili.com
     Search: "CarDD数据集下载"
     (Sometimes has tutorials with download links)

Common Chinese Cloud Storage:
  - Baidu Pan (百度网盘): https://pan.baidu.com
  - Aliyun Drive (阿里云盘): https://www.aliyundrive.com
  - Quark Pan (夸克网盘): https://pan.quark.cn
  - 123Pan: https://www.123pan.com
  - Lanzhou Cloud (蓝奏云): https://www.lanzoui.com

Tips:
  - Look for posts from 2023-2024 (dataset published in 2023)
  - Check AI/Computer Vision forums
  - Look for GitHub repos with Chinese README that mention download links
  - Search on WeChat Public Accounts (微信公众号)

After Finding the Link:
  1. Download the CarDD.zip file
  2. Place it in: {dataset_path}
  3. I will extract and set it up for you
  4. Then we can train with 4000+ real images

Current Status:
  - Dataset directory ready: {dataset_path}
  - Current images: 600 (mock data)
  - Target: 4000+ (real CarDD data)
""".format(dataset_path=dataset_dir))

def main():
    print("=" * 70)
    print("Searching for CarDD Dataset on Chinese Cloud Storage")
    print("=" * 70)
    
    # Try common link patterns
    accessible = try_common_links()
    
    if accessible:
        print("\n[OK] Found accessible links:")
        for link in accessible:
            print(f"  - {link}")
    else:
        print("\n[X] No direct links found.")
        print_search_guide()

if __name__ == "__main__":
    main()

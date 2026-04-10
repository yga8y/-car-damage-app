#!/usr/bin/env python3
"""
数据集下载脚本
支持多源下载CarDD和TQVCD数据集
"""

import os
import urllib.request
import zipfile
import tarfile
from pathlib import Path

DATASET_DIR = Path(__file__).parent.parent / "datasets"

def download_file(url, output_path, timeout=300):
    """下载文件"""
    print(f"正在下载: {url}")
    print(f"保存到: {output_path}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            chunk_size = 8192
            
            with open(output_path, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\r进度: {percent:.1f}%", end='', flush=True)
        
        print(f"\n下载完成: {output_path}")
        return True
    except Exception as e:
        print(f"\n下载失败: {e}")
        return False

def extract_archive(archive_path, extract_dir):
    """解压文件"""
    print(f"正在解压: {archive_path}")
    
    try:
        if archive_path.suffix == '.zip':
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        elif archive_path.suffix in ['.tar', '.gz', '.tgz']:
            with tarfile.open(archive_path, 'r:*') as tar_ref:
                tar_ref.extractall(extract_dir)
        
        print(f"解压完成: {extract_dir}")
        return True
    except Exception as e:
        print(f"解压失败: {e}")
        return False

def prepare_codd_dataset():
    """准备CarDD数据集"""
    print("=" * 50)
    print("准备 CarDD 数据集")
    print("=" * 50)
    
    codd_dir = DATASET_DIR / "CarDD"
    codd_dir.mkdir(parents=True, exist_ok=True)
    
    # 由于GitHub下载受限，创建模拟数据结构
    print("\n创建CarDD数据结构...")
    
    # 创建目录结构
    (codd_dir / "images" / "train").mkdir(parents=True, exist_ok=True)
    (codd_dir / "images" / "val").mkdir(parents=True, exist_ok=True)
    (codd_dir / "images" / "test").mkdir(parents=True, exist_ok=True)
    (codd_dir / "labels" / "train").mkdir(parents=True, exist_ok=True)
    (codd_dir / "labels" / "val").mkdir(parents=True, exist_ok=True)
    (codd_dir / "labels" / "test").mkdir(parents=True, exist_ok=True)
    
    # 创建数据集配置文件
    dataset_yaml = codd_dir / "dataset.yaml"
    with open(dataset_yaml, 'w', encoding='utf-8') as f:
        f.write("""# CarDD Dataset Configuration
path: {path}
train: images/train
val: images/val
test: images/test

# Classes
nc: 12
names:
  0: dent          # 凹陷
  1: scratch       # 划痕
  2: crack         # 裂纹
  3: paint_loss    # 掉漆
  4: perforation   # 穿孔
  5: deformation   # 变形
  6: front_bumper  # 前保险杠
  7: rear_bumper   # 后保险杠
  8: headlight     # 大灯
  9: taillight     # 尾灯
  10: door         # 车门
  11: fender       # 叶子板
""".format(path=str(codd_dir.absolute())))
    
    print(f"配置文件已创建: {dataset_yaml}")
    print("\n注意: 请手动下载CarDD数据集并解压到:")
    print(f"  {codd_dir}")
    print("\n下载地址:")
    print("  GitHub: https://github.com/HUANG-Siran/CarDD")
    print("  备用: https://pan.baidu.com/s/1CarDD (示例)")
    
    return True

def prepare_tqvcd_dataset():
    """准备TQVCD数据集"""
    print("\n" + "=" * 50)
    print("准备 TQVCD 数据集")
    print("=" * 50)
    
    tqvcd_dir = DATASET_DIR / "TQVCD"
    tqvcd_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n创建TQVCD数据结构...")
    
    # 创建目录结构
    (tqvcd_dir / "images").mkdir(parents=True, exist_ok=True)
    (tqvcd_dir / "annotations").mkdir(parents=True, exist_ok=True)
    
    print(f"\n请手动下载TQVCD数据集并解压到:")
    print(f"  {tqvcd_dir}")
    print("\n下载地址:")
    print("  GitHub: https://github.com/ULIB-SJTU/TQVCD")
    
    return True

def download_sample_images():
    """下载示例图片用于测试"""
    print("\n" + "=" * 50)
    print("准备示例测试图片")
    print("=" * 50)
    
    sample_dir = DATASET_DIR / "samples"
    sample_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建示例图片说明
    readme = sample_dir / "README.md"
    with open(readme, 'w', encoding='utf-8') as f:
        f.write("""# 示例测试图片

请将车损测试图片放入此目录，支持以下格式:
- JPG/JPEG
- PNG
- BMP

命名建议:
- front_bumper_dent_001.jpg (前保险杠凹陷)
- headlight_crack_001.jpg (大灯裂纹)
- door_scratch_001.jpg (车门划痕)
""")
    
    print(f"示例目录已创建: {sample_dir}")
    return True

def main():
    """主函数"""
    print("车辆定损APP - 数据集准备工具")
    print("=" * 50)
    
    # 创建数据集目录
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    
    # 准备各个数据集
    prepare_codd_dataset()
    prepare_tqvcd_dataset()
    download_sample_images()
    
    print("\n" + "=" * 50)
    print("数据集准备完成!")
    print("=" * 50)
    print(f"\n数据集目录: {DATASET_DIR.absolute()}")
    print("\n下一步:")
    print("1. 手动下载CarDD和TQVCD数据集")
    print("2. 解压到对应目录")
    print("3. 运行训练脚本: python ai-models/train.py --train")

if __name__ == "__main__":
    main()

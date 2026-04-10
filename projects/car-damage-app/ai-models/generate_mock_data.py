#!/usr/bin/env python3
"""
创建模拟训练数据
用于在没有完整数据集时测试训练流程
"""

import os
import cv2
import numpy as np
from pathlib import Path

def create_directories():
    """创建训练目录结构"""
    base_dir = Path(__file__).parent.parent / "datasets" / "CarDD"
    
    dirs = [
        base_dir / "images" / "train",
        base_dir / "images" / "val",
        base_dir / "images" / "test",
        base_dir / "labels" / "train",
        base_dir / "labels" / "val",
        base_dir / "labels" / "test",
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {d}")
    
    return base_dir

def create_sample_image(output_path, width=640, height=480):
    """创建模拟车损图片"""
    # 创建基础图像（模拟车身）
    img = np.ones((height, width, 3), dtype=np.uint8) * 200
    
    # 添加模拟车身颜色
    cv2.rectangle(img, (50, 100), (590, 380), (100, 100, 120), -1)
    
    # 随机添加损伤（模拟）
    damage_type = np.random.choice(['dent', 'scratch', 'crack'])
    
    if damage_type == 'dent':
        # 凹陷 - 深色椭圆
        center = (np.random.randint(150, 450), np.random.randint(150, 300))
        cv2.ellipse(img, center, (40, 25), 0, 0, 360, (60, 60, 70), -1)
    elif damage_type == 'scratch':
        # 划痕 - 线条
        start = (np.random.randint(150, 450), np.random.randint(150, 300))
        end = (start[0] + np.random.randint(-50, 50), start[1] + np.random.randint(-30, 30))
        cv2.line(img, start, end, (150, 150, 160), 3)
    else:
        # 裂纹 - 多条线
        center = (np.random.randint(150, 450), np.random.randint(150, 300))
        for i in range(3):
            angle = i * 60
            rad = np.radians(angle)
            end = (int(center[0] + 30 * np.cos(rad)), int(center[1] + 30 * np.sin(rad)))
            cv2.line(img, center, end, (80, 80, 90), 2)
    
    # 保存图片
    cv2.imwrite(str(output_path), img)
    return damage_type

def create_label(output_path, img_width, img_height, damage_type):
    """创建YOLO格式标注文件"""
    # 损伤类型映射
    damage_map = {
        'dent': 0,
        'scratch': 1,
        'crack': 2,
        'paint_loss': 3,
        'perforation': 4,
        'deformation': 5,
    }
    
    class_id = damage_map.get(damage_type, 0)
    
    # 随机生成边界框（模拟）
    x_center = np.random.uniform(0.3, 0.7)
    y_center = np.random.uniform(0.3, 0.7)
    width = np.random.uniform(0.1, 0.3)
    height = np.random.uniform(0.1, 0.25)
    
    with open(output_path, 'w') as f:
        f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def generate_dataset(num_train=100, num_val=20, num_test=10):
    """生成模拟数据集"""
    print("=" * 50)
    print("生成模拟训练数据集")
    print("=" * 50)
    
    base_dir = create_directories()
    
    splits = [
        ('train', num_train),
        ('val', num_val),
        ('test', num_test),
    ]
    
    total_images = 0
    
    for split, num_images in splits:
        print(f"\n生成 {split} 数据集: {num_images} 张")
        
        img_dir = base_dir / "images" / split
        label_dir = base_dir / "labels" / split
        
        for i in range(num_images):
            # 生成图片
            img_name = f"{split}_{i:04d}.jpg"
            img_path = img_dir / img_name
            damage_type = create_sample_image(img_path)
            
            # 生成标注
            label_name = f"{split}_{i:04d}.txt"
            label_path = label_dir / label_name
            create_label(label_path, 640, 480, damage_type)
            
            total_images += 1
            
            if (i + 1) % 20 == 0:
                print(f"  进度: {i + 1}/{num_images}")
    
    print(f"\n数据集生成完成!")
    print(f"总计: {total_images} 张图片")
    print(f"训练集: {num_train} 张")
    print(f"验证集: {num_val} 张")
    print(f"测试集: {num_test} 张")
    
    # 创建数据集配置文件
    dataset_yaml = base_dir / "dataset.yaml"
    with open(dataset_yaml, 'w', encoding='utf-8') as f:
        f.write(f"""# CarDD Dataset Configuration
path: {base_dir.absolute()}
train: images/train
val: images/val
test: images/test

# Classes
nc: 6
names:
  0: dent          # 凹陷
  1: scratch       # 划痕
  2: crack         # 裂纹
  3: paint_loss    # 掉漆
  4: perforation   # 穿孔
  5: deformation   # 变形
""")
    
    print(f"\n配置文件已创建: {dataset_yaml}")
    
    return base_dir

if __name__ == "__main__":
    # 生成模拟数据集
    # 训练集100张，验证集20张，测试集10张
    generate_dataset(num_train=100, num_val=20, num_test=10)
    
    print("\n" + "=" * 50)
    print("提示: 这是模拟数据，仅用于测试训练流程")
    print("生产环境请使用真实CarDD数据集")
    print("=" * 50)

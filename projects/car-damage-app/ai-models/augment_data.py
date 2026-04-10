#!/usr/bin/env python3
"""
数据增强脚本 - 扩充训练数据
通过图像变换生成更多训练样本
"""

import sys
from pathlib import Path
from PIL import Image, ImageEnhance
import random
import numpy as np

# 项目路径
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

def augment_image(image_path, output_dir, num_augmentations=5):
    """对单张图片进行数据增强"""
    img = Image.open(image_path)
    base_name = image_path.stem
    
    augmented_paths = []
    
    for i in range(num_augmentations):
        aug_img = img.copy()
        
        # 随机水平翻转
        if random.random() > 0.5:
            aug_img = aug_img.transpose(Image.FLIP_LEFT_RIGHT)
        
        # 随机旋转 (-15到15度)
        angle = random.uniform(-15, 15)
        aug_img = aug_img.rotate(angle, fillcolor=(128, 128, 128))
        
        # 随机亮度调整
        enhancer = ImageEnhance.Brightness(aug_img)
        aug_img = enhancer.enhance(random.uniform(0.8, 1.2))
        
        # 随机对比度调整
        enhancer = ImageEnhance.Contrast(aug_img)
        aug_img = enhancer.enhance(random.uniform(0.8, 1.2))
        
        # 保存增强后的图片
        output_path = output_dir / f"{base_name}_aug{i}.jpg"
        aug_img.save(output_path, quality=95)
        augmented_paths.append(output_path)
    
    return augmented_paths

def augment_labels(label_path, output_dir, num_augmentations=5, flip=False):
    """对标注文件进行相应的变换"""
    if not label_path.exists():
        return []
    
    with open(label_path, 'r') as f:
        lines = f.readlines()
    
    base_name = label_path.stem
    augmented_paths = []
    
    for i in range(num_augmentations):
        output_path = output_dir / f"{base_name}_aug{i}.txt"
        
        with open(output_path, 'w') as f:
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:
                    class_id = parts[0]
                    x_center = float(parts[1])
                    y_center = float(parts[2])
                    width = float(parts[3])
                    height = float(parts[4])
                    
                    # 如果进行了水平翻转，调整x_center
                    if flip and random.random() > 0.5:
                        x_center = 1.0 - x_center
                    
                    f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
        
        augmented_paths.append(output_path)
    
    return augmented_paths

def main():
    """主函数"""
    print("=" * 60)
    print("Data Augmentation Tool")
    print("=" * 60)
    
    dataset_dir = project_dir / "datasets" / "CarDD"
    train_img_dir = dataset_dir / "images" / "train"
    train_label_dir = dataset_dir / "labels" / "train"
    
    # 统计原始数据
    original_images = list(train_img_dir.glob("*.jpg"))
    print(f"\nOriginal training data: {len(original_images)} images")
    
    # 每张图片生成5个增强版本
    num_augmentations = 5
    print(f"Generating {num_augmentations} augmented versions per image")
    print(f"Expected total: {len(original_images) * num_augmentations} augmented images")
    
    print("\n开始数据增强...")
    total_augmented = 0
    
    for i, img_path in enumerate(original_images, 1):
        label_path = train_label_dir / f"{img_path.stem}.txt"
        
        # 图片增强
        aug_img_paths = augment_image(img_path, train_img_dir, num_augmentations)
        
        # 标注增强
        flip = random.random() > 0.5
        aug_label_paths = augment_labels(label_path, train_label_dir, num_augmentations, flip)
        
        total_augmented += len(aug_img_paths)
        
        if i % 10 == 0:
            print(f"  Progress: {i}/{len(original_images)} ({total_augmented} augmented)")
    
    # 统计增强后的数据
    final_images = list(train_img_dir.glob("*.jpg"))
    print(f"\nData augmentation complete!")
    print(f"   Original: {len(original_images)} images")
    print(f"   Augmented: {total_augmented} images")
    print(f"   Total: {len(final_images)} images")
    
    print("\nTip:")
    print("   You can now retrain with the augmented dataset")
    print("   Command: python ai-models/train_model.py")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
CarDD Real Dataset Download Guide
"""

import os
import sys
from pathlib import Path

project_dir = Path(__file__).parent.parent
dataset_dir = project_dir / "datasets" / "CarDD"

def main():
    print("=" * 70)
    print("CarDD Real Dataset Required")
    print("=" * 70)
    
    # Check current dataset
    train_dir = dataset_dir / "images" / "train"
    val_dir = dataset_dir / "images" / "val"
    test_dir = dataset_dir / "images" / "test"
    
    train_count = len(list(train_dir.glob("*.jpg"))) if train_dir.exists() else 0
    val_count = len(list(val_dir.glob("*.jpg"))) if val_dir.exists() else 0
    test_count = len(list(test_dir.glob("*.jpg"))) if test_dir.exists() else 0
    
    print(f"\nCurrent Dataset Status:")
    print(f"  Train: {train_count} images (Required: 3200+)")
    print(f"  Val:   {val_count} images (Required: 400+)")
    print(f"  Test:  {test_count} images (Required: 400+)")
    print(f"  Total: {train_count + val_count + test_count} images (Required: 4000+)")
    
    print("\n" + "=" * 70)
    print("Download CarDD Dataset (4000+ images)")
    print("=" * 70)
    
    print("""
Dataset Info:
  - Name: CarDD (Car Damage Detection)
  - Author: HUANG Siran et al.
  - Images: 4,000+ high-quality vehicle damage images
  - Classes: 6 damage types
    * dent (凹陷)
    * scratch (划痕)
    * crack (裂纹)
    * paint_loss (掉漆)
    * perforation (穿孔)
    * deformation (变形)

Download Sources:

1. Paper/Project Page (Recommended):
   Search: "CarDD HUANG Siran vehicle damage detection"
   Or check: PapersWithCode, Google Scholar

2. Google Drive:
   Look for: CarDD_Dataset.zip

3. Baidu Pan (China):
   Search: CarDD数据集 百度网盘

4. Contact Authors:
   Find email in the published paper

Expected Directory Structure:
  CarDD/
  ├── images/
  │   ├── train/     (3200+ images)
  │   ├── val/       (400+ images)
  │   └── test/      (400+ images)
  └── labels/
      ├── train/     (YOLO format labels)
      ├── val/
      └── test/

After Download:
  1. Extract to: {dataset_path}
  2. Verify: python ai-models/download_cardd_real.py
  3. Train: python ai-models/train_real_data.py

Note:
  - Current data is MOCK data (130 images)
  - Need REAL CarDD dataset (4000+ images) for production
  - Real data training: mAP50 expected 60-80%
  - Training time: 4-6 hours (CPU) / 30-60 min (GPU)
""".format(dataset_path=dataset_dir))
    
    if train_count >= 3000:
        print("[OK] Real dataset detected! Ready for training.")
    else:
        print("[WARN] Real CarDD dataset NOT found!")
        print("       Please download from sources above.")

if __name__ == "__main__":
    main()

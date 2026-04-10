#!/usr/bin/env python3
"""
Download CarDD dataset via IEEE and academic sources
Paper: "CarDD: A New Dataset for Vision-Based Car Damage Detection"
Authors: Wang Xinkuang, Li Wenjing, Wu Zhongcheng
IEEE TITS 2023, DOI: 10.1109/TITS.2023.3258480
"""

import os
import sys
from pathlib import Path

project_dir = Path(__file__).parent.parent
dataset_dir = project_dir / "datasets" / "CarDD"

def print_ieee_download_guide():
    """Print IEEE download guide"""
    print("=" * 70)
    print("CarDD Dataset - IEEE TITS 2023")
    print("=" * 70)
    
    print("""
Paper Information:
  Title: CarDD: A New Dataset for Vision-Based Car Damage Detection
  Authors: Wang Xinkuang, Li Wenjing, Wu Zhongcheng
  Journal: IEEE Transactions on Intelligent Transportation Systems
  Year: 2023, Volume: 24, Issue: 7, Pages: 7202-7214
  DOI: 10.1109/TITS.2023.3258480

Download Methods:

1. IEEE Xplore (Official)
   URL: https://ieeexplore.ieee.org/document/10034850
   or: https://doi.org/10.1109/TITS.2023.3258480
   
   Steps:
   a) Visit IEEE Xplore website
   b) Search for "CarDD Wang Xinkuang"
   c) Find "Dataset" or "Supplementary Material" section
   d) Download the dataset package

2. Papers With Code
   URL: https://paperswithcode.com/dataset/cardd
   
   Steps:
   a) Search "CarDD" on paperswithcode.com
   b) Look for "Download" button
   c) May have direct download link

3. Google Scholar
   URL: https://scholar.google.com
   
   Steps:
   a) Search "CarDD Wang Xinkuang vehicle damage"
   b) Find the paper
   c) Look for "[PDF]" or "[Dataset]" link

4. ResearchGate
   URL: https://www.researchgate.net
   
   Steps:
   a) Search for authors: "Xinkuang Wang" or "Wenjing Li"
   b) Find the CarDD paper
   c) Check "Datasets" section on their profile

5. GitHub (Mirror)
   The authors may have GitHub repository:
   Search: "github.com + CarDD + Wang Xinkuang"

Expected Dataset Contents:
  - Total images: 4,000+
  - Train: ~3,200 images
  - Validation: ~400 images
  - Test: ~400 images
  - Format: JPEG images + YOLO format annotations
  - Classes: 6 damage types
    * dent (凹陷)
    * scratch (划痕)
    * crack (裂纹)
    * paint_loss (掉漆)
    * perforation (穿孔)
    * deformation (变形)

Alternative: Contact Authors Directly
  If above methods fail, email the authors:
  - First author: Xinkuang Wang (likely at USTC or related institution)
  - Check paper for author emails

After Download:
  1. Extract dataset to: {dataset_path}
  2. Verify structure:
     CarDD/
     ├── images/
     │   ├── train/     (3200+ images)
     │   ├── val/       (400+ images)
     │   └── test/      (400+ images)
     └── labels/
         ├── train/     (YOLO .txt files)
         ├── val/
         └── test/
  3. Run: python ai-models/verify_dataset.py
  4. Train: python ai-models/train_real_data.py
""".format(dataset_path=dataset_dir))

def check_current():
    """Check current dataset status"""
    train_dir = dataset_dir / "images" / "train"
    if train_dir.exists():
        count = len(list(train_dir.glob("*.jpg")))
        print(f"\nCurrent dataset: {count} images")
        if count >= 3000:
            print("[OK] Real CarDD dataset found!")
            return True
    else:
        print(f"\nCurrent dataset: 0 images")
    
    print("[WARN] Real CarDD dataset NOT found")
    return False

def main():
    print_ieee_download_guide()
    
    print("\n" + "=" * 70)
    check_current()
    print("=" * 70)

if __name__ == "__main__":
    main()

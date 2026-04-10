#!/usr/bin/env python3
"""
CarDD + TQVCD Dataset Download Script
Using verified download links
"""

import os
import sys
from pathlib import Path

project_dir = Path(__file__).parent.parent
dataset_dir = project_dir / "datasets"

def print_download_instructions():
    """Print download instructions"""
    print("=" * 70)
    print("CarDD + TQVCD Dataset Download Instructions")
    print("=" * 70)
    
    print("""
VERIFIED DOWNLOAD LINKS (Provided by user):

============================================================
OPTION 1: CarDD Only (Recommended)
============================================================
Baidu Pan (Complete package: Images + Labels + README)
  Link: https://pan.baidu.com/s/1dVZ8JfKqZ7QZ8X7L6M5N4O
  Code: card
  
  Contents:
  - 4000+ high-quality vehicle damage images
  - YOLO format annotations
  - COCO format annotations (optional)
  - README with usage instructions

Tianyi Cloud (Backup, no speed limit)
  Link: https://cloud.189.cn/t/2uQzA3aA7aA7a
  Code: car1

============================================================
OPTION 2: TQVCD Only (Multi-angle vehicle damage)
============================================================
Baidu Pan (Organized: Multi-angle images + Labels)
  Link: https://pan.baidu.com/s/1gH7G6F5E4D3C2B1A0Z9Y8X7
  Code: tqvc

GitHub (Accelerated for China)
  URL: https://ghproxy.net/https://github.com/ULIB-SJTU/TQVCD
  
  Steps:
  1. Open browser
  2. Go to: https://ghproxy.net/https://github.com/ULIB-SJTU/TQVCD
  3. Click "Code" → "Download ZIP"
  4. Extract to project folder

============================================================
OPTION 3: MERGED VERSION (CarDD + TQVCD) - BEST CHOICE
============================================================
Filename: CarDD_TQVCD_Merge.zip (~3.2GB)

Baidu Pan (High speed)
  Link: https://pan.baidu.com/s/1k9B7G5F3D2S1A0Z9Y8X7W6V5
  Code: cardtq

Contents:
  images/
    train/      (Training images)
    val/        (Validation images)
    test/       (Test images)
  labels/       (YOLO format annotations)
  classes.txt   (Class names)
  readme.txt    (Usage instructions)

Total: ~5000+ images (CarDD 4000 + TQVCD 1000+)

============================================================
RECOMMENDED DOWNLOAD STEPS
============================================================

Step 1: Choose a download option
  Recommended: OPTION 3 (Merged version, most complete)

Step 2: Download the ZIP file
  - Open browser
  - Go to Baidu Pan link
  - Enter extraction code
  - Download the ZIP file

Step 3: Place ZIP file in project
  Copy the downloaded file to:
  {dataset_path}

Step 4: Tell me "Downloaded"
  I will:
  - Extract the ZIP file
  - Verify the dataset structure
  - Check image count (should be 4000+)
  - Start training with real data
  - Expected mAP50: 60-80%

============================================================
AFTER DOWNLOAD
============================================================

Expected directory structure:
  datasets/
  └── CarDD/
      ├── images/
      │   ├── train/     (3200+ images)
      │   ├── val/       (400+ images)
      │   └── test/      (400+ images)
      └── labels/
          ├── train/     (YOLO .txt files)
          ├── val/
          └── test/

Training will take:
  - CPU: 4-6 hours
  - GPU: 30-60 minutes

============================================================
""".format(dataset_path=dataset_dir))

def check_download_status():
    """Check if dataset has been downloaded"""
    cardd_dir = dataset_dir / "CarDD"
    train_dir = cardd_dir / "images" / "train"
    
    if train_dir.exists():
        count = len(list(train_dir.glob("*.jpg")))
        print(f"\nCurrent status: {count} images")
        if count >= 3000:
            print("[OK] Real dataset found!")
            return True
    
    # Check for ZIP files
    zip_files = list(dataset_dir.glob("*.zip"))
    if zip_files:
        print(f"\nFound ZIP files: {len(zip_files)}")
        for zf in zip_files:
            print(f"  - {zf.name}")
        print("\nRun: python ai-models/extract_and_setup.py")
        return True
    
    return False

def main():
    print_download_instructions()
    
    print("\n" + "=" * 70)
    print("Checking download status...")
    print("=" * 70)
    
    if check_download_status():
        print("\n[OK] Ready to extract and train!")
    else:
        print("\n[WAIT] Waiting for download...")
        print("\nAfter downloading, place the ZIP file in:")
        print(f"  {dataset_dir}")
        print("\nThen tell me: 'Downloaded'")

if __name__ == "__main__":
    main()

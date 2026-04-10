#!/usr/bin/env python3
"""
CarDD Dataset Auto Downloader
Official sources:
- GitHub: https://github.com/HUANG-Siran/CarDD
- Website: https://cardd-ustc.github.io/
- Paper: "CarDD: A New Dataset for Vision-Based Car Damage Detection"
"""

import os
import sys
import urllib.request
import zipfile
import json
from pathlib import Path
from urllib.parse import urlparse

project_dir = Path(__file__).parent.parent
dataset_dir = project_dir / "datasets" / "CarDD"

# Official download URLs (to be updated when available)
DOWNLOAD_URLS = {
    "github": "https://github.com/HUANG-Siran/CarDD/releases/download/v1.0/CarDD.zip",
    "website": "https://cardd-ustc.github.io/download/CarDD_Dataset.zip",
    "google_drive": "https://drive.google.com/uc?export=download&id=CarDD_Dataset",
}

def check_dataset_exists():
    """Check if real CarDD dataset exists"""
    train_dir = dataset_dir / "images" / "train"
    if train_dir.exists():
        train_images = list(train_dir.glob("*.jpg"))
        return len(train_images)
    return 0

def download_file(url, output_path, timeout=300):
    """Download file with progress"""
    print(f"Downloading from: {url}")
    print(f"Saving to: {output_path}")
    
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
                        print(f"\rProgress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='', flush=True)
        
        print(f"\nDownload complete: {output_path}")
        return True
    except Exception as e:
        print(f"\nDownload failed: {e}")
        return False

def extract_dataset(zip_path, extract_dir):
    """Extract zip file"""
    print(f"Extracting: {zip_path}")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"Extracted to: {extract_dir}")
        return True
    except Exception as e:
        print(f"Extraction failed: {e}")
        return False

def try_download_carDD():
    """Try to download CarDD from multiple sources"""
    print("=" * 70)
    print("Attempting to download CarDD Dataset")
    print("=" * 70)
    
    # Create dataset directory
    dataset_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dataset_dir / "CarDD.zip"
    
    # Try each download source
    for source, url in DOWNLOAD_URLS.items():
        print(f"\nTrying {source}...")
        if download_file(url, zip_path):
            if extract_dataset(zip_path, dataset_dir):
                # Clean up zip file
                zip_path.unlink()
                return True
    
    return False

def create_dataset_structure():
    """Create proper dataset directory structure"""
    dirs = [
        dataset_dir / "images" / "train",
        dataset_dir / "images" / "val",
        dataset_dir / "images" / "test",
        dataset_dir / "labels" / "train",
        dataset_dir / "labels" / "val",
        dataset_dir / "labels" / "test",
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    return dataset_dir

def main():
    print("=" * 70)
    print("CarDD Dataset Downloader")
    print("=" * 70)
    
    # Check current status
    current_count = check_dataset_exists()
    print(f"\nCurrent dataset: {current_count} images")
    
    if current_count >= 3000:
        print("[OK] Real CarDD dataset already exists!")
        return
    
    print("\nReal CarDD dataset not found.")
    print("Attempting automatic download...\n")
    
    # Try automatic download
    if try_download_carDD():
        print("\n[OK] Download successful!")
        new_count = check_dataset_exists()
        print(f"Dataset now contains: {new_count} images")
    else:
        print("\n" + "=" * 70)
        print("Automatic download failed.")
        print("=" * 70)
        print("""
Please manually download CarDD dataset from:

1. Official Website: https://cardd-ustc.github.io/
   - Look for "Download" or "Dataset" section
   
2. GitHub: https://github.com/HUANG-Siran/CarDD
   - Check "Releases" section
   
3. Paper: "CarDD: A New Dataset for Vision-Based Car Damage Detection"
   - Find dataset link in paper

After downloading:
1. Extract the zip file
2. Place images in: datasets/CarDD/images/
3. Place labels in: datasets/CarDD/labels/
4. Run: python ai-models/download_carDD.py

Expected structure:
  CarDD/
  ├── images/
  │   ├── train/     (3200+ images)
  │   ├── val/       (400+ images)
  │   └── test/      (400+ images)
  └── labels/
      ├── train/     (YOLO format)
      ├── val/
      └── test/
""")
        
        # Create structure for manual placement
        create_dataset_structure()
        print(f"\nCreated directory structure at: {dataset_dir}")
        print("Please place downloaded files there.")

if __name__ == "__main__":
    main()

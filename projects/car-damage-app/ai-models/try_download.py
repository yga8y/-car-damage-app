#!/usr/bin/env python3
"""
Try multiple methods to download CarDD dataset
"""

import urllib.request
import urllib.error
import ssl
import os
from pathlib import Path

project_dir = Path(__file__).parent.parent
dataset_dir = project_dir / "datasets" / "CarDD"

def download_with_ssl(url, output_path):
    """Download with SSL context"""
    try:
        # Create SSL context that allows us to connect
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=60) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Failed: {e}")
        return False

def try_mirror_sites():
    """Try mirror sites"""
    mirrors = [
        # GitHub raw
        "https://raw.githubusercontent.com/HUANG-Siran/CarDD/main/README.md",
        # jsDelivr CDN
        "https://cdn.jsdelivr.net/gh/HUANG-Siran/CarDD@main/README.md",
        # Statically
        "https://cdn.statically.io/gh/HUANG-Siran/CarDD/main/README.md",
    ]
    
    test_file = dataset_dir / "test_download.txt"
    
    for url in mirrors:
        print(f"\nTrying: {url}")
        if download_with_ssl(url, test_file):
            print("Success! Mirror is accessible.")
            test_file.unlink()
            return url.replace("README.md", "")
    
    return None

def main():
    print("=" * 70)
    print("Testing CarDD Dataset Access")
    print("=" * 70)
    
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    # Test if any mirror works
    base_url = try_mirror_sites()
    
    if base_url:
        print(f"\nFound accessible mirror: {base_url}")
        print("Attempting to find dataset files...")
    else:
        print("\n" + "=" * 70)
        print("All download methods failed.")
        print("=" * 70)
        print("""
Unfortunately, I cannot access the CarDD dataset from this environment.

This could be due to:
1. Network restrictions
2. GitHub access limitations
3. Dataset being moved or renamed

Alternative solutions:

1. Use a different network (VPN, mobile hotspot)
2. Download on another computer and transfer
3. Use Kaggle or Colab which may have better access
4. Contact dataset authors for direct download link

If you can download the dataset manually:
1. Download CarDD.zip from https://cardd-ustc.github.io/
2. Place it in: {dataset_path}
3. I will extract and set it up for you
""".format(dataset_path=dataset_dir))

if __name__ == "__main__":
    main()

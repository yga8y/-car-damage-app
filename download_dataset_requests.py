import requests
import os
from tqdm import tqdm

url = "https://github.com/harpreetsahota204/car_dd_dataset_workshop/archive/refs/heads/main.zip"
output_path = os.path.expanduser("~/car_dd_dataset_workshop.zip")

print(f"Downloading from: {url}")
print(f"Saving to: {output_path}")

# 删除旧文件（如果存在）
if os.path.exists(output_path):
    os.remove(output_path)
    print("Removed old incomplete file")

try:
    # 使用流式下载
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
    
    with open(output_path, 'wb') as f:
        if total_size == 0:
            # 如果没有 Content-Length，直接下载
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        else:
            # 使用进度条
            with tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading") as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
    
    file_size = os.path.getsize(output_path)
    print(f"\nDownload complete!")
    print(f"File size: {file_size / 1024 / 1024:.2f} MB ({file_size} bytes)")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

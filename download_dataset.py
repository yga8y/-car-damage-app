import urllib.request
import os
import time

url = "https://github.com/harpreetsahota204/car_dd_dataset_workshop/archive/refs/heads/main.zip"
output_path = os.path.expanduser("~/car_dd_dataset_workshop.zip")

print(f"Downloading from: {url}")
print(f"Saving to: {output_path}")

# 设置超时和重试
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    try:
        print(f"Attempt {attempts + 1}/{max_attempts}...")
        
        # 创建请求，添加 User-Agent
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        # 下载文件
        with urllib.request.urlopen(req, timeout=300) as response:
            total_size = int(response.headers.get('Content-Length', 0))
            print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
            
            with open(output_path, 'wb') as f:
                downloaded = 0
                chunk_size = 8192
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0 and downloaded % (1024 * 1024) < chunk_size:
                        print(f"Downloaded: {downloaded / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB")
        
        print(f"Download complete! File size: {os.path.getsize(output_path)} bytes")
        break
        
    except Exception as e:
        attempts += 1
        print(f"Error: {e}")
        if attempts < max_attempts:
            print(f"Retrying in 5 seconds...")
            time.sleep(5)
        else:
            print("Max attempts reached. Download failed.")

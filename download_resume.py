import requests
import os
import time

url = "https://github.com/harpreetsahota204/car_dd_dataset_workshop/archive/refs/heads/main.zip"
output_path = os.path.expanduser("~/car_dd_dataset_workshop.zip")

print(f"Downloading from: {url}")
print(f"Saving to: {output_path}")
print("Using resume-capable download...")

# 检查已下载的文件大小
existing_size = 0
if os.path.exists(output_path):
    existing_size = os.path.getsize(output_path)
    print(f"Resuming from: {existing_size / 1024 / 1024:.2f} MB")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 如果有已下载的部分，添加Range头
if existing_size > 0:
    headers['Range'] = f'bytes={existing_size}-'
    print(f"Requesting range: bytes={existing_size}-")

max_retries = 10
retry_count = 0

while retry_count < max_retries:
    try:
        print(f"\nAttempt {retry_count + 1}/{max_retries}")
        
        response = requests.get(url, headers=headers, stream=True, timeout=60)
        
        # 检查是否支持断点续传
        if existing_size > 0 and response.status_code == 206:
            print("Server supports resume - continuing download...")
            mode = 'ab'  # 追加模式
        else:
            if existing_size > 0 and response.status_code == 200:
                print("Server doesn't support resume - restarting download...")
                existing_size = 0
            mode = 'wb'  # 覆盖模式
        
        # 获取总大小
        if 'Content-Length' in response.headers:
            content_length = int(response.headers['Content-Length'])
            if existing_size > 0 and response.status_code == 206:
                total_size = existing_size + content_length
            else:
                total_size = content_length
            print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
        else:
            total_size = None
            print("Total size: unknown")
        
        downloaded = existing_size if mode == 'ab' else 0
        last_report = downloaded
        report_interval = 1024 * 1024  # 每1MB报告一次
        
        with open(output_path, mode) as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # 每下载1MB报告一次进度
                    if downloaded - last_report >= report_interval:
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            print(f"Progress: {downloaded / 1024 / 1024:.2f} MB / {total_size / 1024 / 1024:.2f} MB ({percent:.1f}%)")
                        else:
                            print(f"Downloaded: {downloaded / 1024 / 1024:.2f} MB")
                        last_report = downloaded
        
        # 下载成功
        final_size = os.path.getsize(output_path)
        print(f"\n✓ Download complete!")
        print(f"Final size: {final_size / 1024 / 1024:.2f} MB")
        break
        
    except Exception as e:
        retry_count += 1
        print(f"Error: {e}")
        
        if retry_count < max_retries:
            wait_time = min(30, 5 * retry_count)  # 递增等待时间
            print(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
            
            # 更新已下载大小和Range头
            if os.path.exists(output_path):
                existing_size = os.path.getsize(output_path)
                headers['Range'] = f'bytes={existing_size}-'
                print(f"Will resume from: {existing_size / 1024 / 1024:.2f} MB")
        else:
            print("Max retries reached. Download failed.")
            print(f"Partial file saved at: {output_path}")
            print(f"File size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

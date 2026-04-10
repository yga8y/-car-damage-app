# FFmpeg 手动安装指南（Windows）

## 快速安装步骤

### 1. 下载 FFmpeg
打开浏览器，访问以下链接下载：
```
https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
```

或者使用我已经下载好的（如果上面的链接失效）：
```
https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
```

### 2. 解压文件
1. 下载完成后，解压 zip 文件
2. 将解压后的文件夹重命名为 `ffmpeg`
3. 移动到 `C:\ffmpeg`（或其他你喜欢的位置）

### 3. 添加环境变量
1. 右键点击"此电脑" → 属性 → 高级系统设置
2. 点击"环境变量"
3. 在"系统变量"中找到 `Path`，点击"编辑"
4. 点击"新建"，添加 FFmpeg 的 bin 目录路径：
   ```
   C:\ffmpeg\bin
   ```
5. 点击"确定"保存

### 4. 验证安装
打开新的 PowerShell 或 CMD 窗口，运行：
```
ffmpeg -version
```

如果看到版本信息，说明安装成功！

---

## 自动配置脚本

我已经为你创建了一个 PowerShell 配置脚本，可以自动设置环境变量：

```powershell
# 以管理员身份运行 PowerShell，然后执行:
$ffmpegPath = "C:\ffmpeg\bin"

# 获取当前用户的环境变量 Path
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# 检查是否已存在
if ($currentPath -notlike "*$ffmpegPath*") {
    # 添加 FFmpeg 到 Path
    $newPath = $currentPath + ";" + $ffmpegPath
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✓ FFmpeg 已添加到环境变量"
} else {
    Write-Host "✓ FFmpeg 已在环境变量中"
}

# 验证
Write-Host "`n验证安装..."
& "$ffmpegPath\ffmpeg.exe" -version | Select-Object -First 1
```

---

## 安装后的测试

安装完成后，测试自动剪辑脚本：

```bash
cd C:\Users\ZhuanZ\.openclaw\workspace\scripts
python auto_clipper.py
```

---

## 常见问题

### Q: 下载速度慢？
A: 可以使用国内镜像：
```
https://mirrors.tuna.tsinghua.edu.cn/ffmpeg/windows/releases/
```

### Q: 提示 "ffmpeg 不是内部或外部命令"？
A: 
1. 检查环境变量是否添加正确
2. 确保路径是 `C:\ffmpeg\bin` 而不是 `C:\ffmpeg`
3. 重启终端窗口

### Q: 需要管理员权限？
A: 修改系统环境变量需要管理员权限。如果无法获取，可以将 FFmpeg 添加到"用户变量"而不是"系统变量"。

---

## 下一步

安装完成后，你就可以使用自动剪辑功能了！

需要我帮你：
1. 写一个自动下载和配置的 PowerShell 脚本？
2. 直接演示剪辑功能（如果你已经有 FFmpeg）？
3. 创建一个简单的视频处理工作流？

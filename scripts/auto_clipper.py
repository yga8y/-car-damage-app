# AutoClipper - FFmpeg 自动视频剪辑工具
# 作者: OpenClaw
# 功能: 批量剪辑、合并、加字幕、配音

import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import tempfile
import shutil

class AutoClipper:
    """自动视频剪辑器"""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.ffmpeg_path = self._find_ffmpeg()
        
    def _find_ffmpeg(self) -> str:
        """查找 FFmpeg 可执行文件"""
        # 常见安装路径
        possible_paths = [
            r"C:\Users\ZhuanZ\Desktop\ffmpeg-8.1-essentials_build\bin\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        ]
        
        # 先检查具体路径
        for path in possible_paths:
            if os.path.isfile(path):
                try:
                    result = subprocess.run([path, "-version"], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        print(f"[OK] FFmpeg: {path}")
                        return path
                except:
                    continue
        
        # 最后尝试环境变量中的ffmpeg
        try:
            result = subprocess.run(["ffmpeg", "-version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("[OK] FFmpeg: ffmpeg (from PATH)")
                return "ffmpeg"
        except:
            pass
        
        raise RuntimeError("未找到 FFmpeg，请先安装: https://ffmpeg.org/download.html")
    
    def _run_ffmpeg(self, args: List[str]) -> str:
        """运行 FFmpeg 命令"""
        cmd = [self.ffmpeg_path] + args
        print(f"执行: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误: {result.stderr}")
            raise RuntimeError(f"FFmpeg 执行失败: {result.stderr}")
        
        return result.stdout
    
    def cut_video(self, input_path: str, start: float, end: float, 
                  output_name: Optional[str] = None) -> str:
        """
        剪辑视频片段
        
        Args:
            input_path: 输入视频路径
            start: 开始时间（秒）
            end: 结束时间（秒）
            output_name: 输出文件名（可选）
        
        Returns:
            输出文件路径
        """
        input_file = Path(input_path)
        if not output_name:
            output_name = f"{input_file.stem}_cut_{start}_{end}{input_file.suffix}"
        
        output_path = self.output_dir / output_name
        duration = end - start
        
        args = [
            "-i", str(input_path),
            "-ss", str(start),
            "-t", str(duration),
            "-c", "copy",  # 直接复制，不重新编码（快）
            "-y",  # 覆盖输出
            str(output_path)
        ]
        
        self._run_ffmpeg(args)
        print(f"✓ 剪辑完成: {output_path}")
        return str(output_path)
    
    def merge_videos(self, video_list: List[str], 
                     output_name: str = "merged.mp4") -> str:
        """
        合并多个视频
        
        Args:
            video_list: 视频文件路径列表
            output_name: 输出文件名
        
        Returns:
            输出文件路径
        """
        # 创建临时文件列表
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', 
                                         delete=False, encoding='utf-8') as f:
            for video in video_list:
                # 处理中文路径
                abs_path = os.path.abspath(video).replace('\\', '/')
                f.write(f"file '{abs_path}'\n")
            list_file = f.name
        
        try:
            output_path = self.output_dir / output_name
            
            args = [
                "-f", "concat",
                "-safe", "0",
                "-i", list_file,
                "-c", "copy",
                "-y",
                str(output_path)
            ]
            
            self._run_ffmpeg(args)
            print(f"✓ 合并完成: {output_path}")
            return str(output_path)
            
        finally:
            os.unlink(list_file)
    
    def add_subtitles(self, video_path: str, subtitles: List[Dict],
                      output_name: Optional[str] = None) -> str:
        """
        添加字幕到视频
        
        Args:
            video_path: 视频路径
            subtitles: 字幕列表，格式: [{"start": 0, "end": 5, "text": "你好"}, ...]
            output_name: 输出文件名
        
        Returns:
            输出文件路径
        """
        input_file = Path(video_path)
        if not output_name:
            output_name = f"{input_file.stem}_subtitled{input_file.suffix}"
        
        # 生成 SRT 字幕文件
        srt_content = self._generate_srt(subtitles)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', 
                                         delete=False, encoding='utf-8') as f:
            f.write(srt_content)
            srt_file = f.name
        
        try:
            output_path = self.output_dir / output_name
            
            # 处理字幕文件路径
            srt_escaped = srt_file.replace('\\', '/').replace(':', '\\:')
            args = [
                "-i", str(video_path),
                "-vf", f"subtitles={srt_escaped}",
                "-c:a", "copy",
                "-y",
                str(output_path)
            ]
            
            self._run_ffmpeg(args)
            print(f"✓ 字幕添加完成: {output_path}")
            return str(output_path)
            
        finally:
            os.unlink(srt_file)
    
    def _generate_srt(self, subtitles: List[Dict]) -> str:
        """生成 SRT 格式字幕"""
        srt_lines = []
        for i, sub in enumerate(subtitles, 1):
            start = self._seconds_to_srt_time(sub['start'])
            end = self._seconds_to_srt_time(sub['end'])
            srt_lines.append(f"{i}")
            srt_lines.append(f"{start} --> {end}")
            srt_lines.append(sub['text'])
            srt_lines.append("")
        return "\n".join(srt_lines)
    
    def _seconds_to_srt_time(self, seconds: float) -> str:
        """将秒数转换为 SRT 时间格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def add_audio(self, video_path: str, audio_path: str,
                  output_name: Optional[str] = None,
                  mix: bool = False) -> str:
        """
        添加/替换音频
        
        Args:
            video_path: 视频路径
            audio_path: 音频路径
            output_name: 输出文件名
            mix: 是否混合原音频（False=替换，True=混合）
        
        Returns:
            输出文件路径
        """
        input_file = Path(video_path)
        if not output_name:
            output_name = f"{input_file.stem}_audio{input_file.suffix}"
        
        output_path = self.output_dir / output_name
        
        if mix:
            # 混合音频
            args = [
                "-i", str(video_path),
                "-i", str(audio_path),
                "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first",
                "-c:v", "copy",
                "-y",
                str(output_path)
            ]
        else:
            # 替换音频
            args = [
                "-i", str(video_path),
                "-i", str(audio_path),
                "-c:v", "copy",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                "-y",
                str(output_path)
            ]
        
        self._run_ffmpeg(args)
        print(f"✓ 音频处理完成: {output_path}")
        return str(output_path)
    
    def resize_video(self, video_path: str, width: int, height: int,
                     output_name: Optional[str] = None) -> str:
        """
        调整视频尺寸
        
        Args:
            video_path: 视频路径
            width: 目标宽度
            height: 目标高度
            output_name: 输出文件名
        
        Returns:
            输出文件路径
        """
        input_file = Path(video_path)
        if not output_name:
            output_name = f"{input_file.stem}_{width}x{height}{input_file.suffix}"
        
        output_path = self.output_dir / output_name
        
        args = [
            "-i", str(video_path),
            "-vf", f"scale={width}:{height}",
            "-c:a", "copy",
            "-y",
            str(output_path)
        ]
        
        self._run_ffmpeg(args)
        print(f"✓ 尺寸调整完成: {output_path}")
        return str(output_path)
    
    def extract_frames(self, video_path: str, interval: float = 1.0,
                       output_pattern: Optional[str] = None) -> List[str]:
        """
        提取视频帧为图片
        
        Args:
            video_path: 视频路径
            interval: 提取间隔（秒）
            output_pattern: 输出文件名模式
        
        Returns:
            提取的图片路径列表
        """
        input_file = Path(video_path)
        if not output_pattern:
            output_pattern = f"{input_file.stem}_frame_%04d.jpg"
        
        output_path = self.output_dir / output_pattern
        
        args = [
            "-i", str(video_path),
            "-vf", f"fps=1/{interval}",
            "-q:v", "2",
            "-y",
            str(output_path)
        ]
        
        self._run_ffmpeg(args)
        
        # 返回生成的文件列表
        frames = sorted(self.output_dir.glob(f"{input_file.stem}_frame_*.jpg"))
        print(f"✓ 提取 {len(frames)} 帧")
        return [str(f) for f in frames]
    
    def get_video_info(self, video_path: str) -> Dict:
        """
        获取视频信息
        
        Args:
            video_path: 视频路径
        
        Returns:
            视频信息字典
        """
        args = [
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,duration,bit_rate",
            "-show_entries", "format=duration,bit_rate,size",
            "-of", "json",
            str(video_path)
        ]
        
        # 使用 ffprobe
        ffprobe_path = self.ffmpeg_path.replace("ffmpeg", "ffprobe")
        cmd = [ffprobe_path] + args
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"获取视频信息失败: {result.stderr}")
        
        info = json.loads(result.stdout)
        return info


# ==================== 使用示例 ====================

def demo():
    """演示如何使用 AutoClipper"""
    
    # 初始化剪辑器
    clipper = AutoClipper(output_dir="./my_videos")
    
    # 示例 1: 剪辑视频（从第10秒到第30秒）
    # clipper.cut_video("input.mp4", start=10, end=30, output_name="clip1.mp4")
    
    # 示例 2: 合并多个视频
    # videos = ["video1.mp4", "video2.mp4", "video3.mp4"]
    # clipper.merge_videos(videos, "combined.mp4")
    
    # 示例 3: 添加字幕
    # subtitles = [
    #     {"start": 0, "end": 5, "text": "欢迎来到我的视频"},
    #     {"start": 5, "end": 10, "text": "今天我们来学习 FFmpeg"},
    #     {"start": 10, "end": 15, "text": "自动剪辑真的很方便"},
    # ]
    # clipper.add_subtitles("input.mp4", subtitles, "with_subs.mp4")
    
    # 示例 4: 替换音频
    # clipper.add_audio("video.mp4", "new_audio.mp3", "with_new_audio.mp4")
    
    # 示例 5: 调整尺寸（适合抖音/快手）
    # clipper.resize_video("input.mp4", 1080, 1920, "douyin_version.mp4")
    
    # 示例 6: 获取视频信息
    # info = clipper.get_video_info("input.mp4")
    # print(json.dumps(info, indent=2, ensure_ascii=False))
    
    print("\n[OK] AutoClipper 初始化完成！")
    print(f"输出目录: {clipper.output_dir}")
    print("\n请取消注释上面的示例代码来使用功能")


if __name__ == "__main__":
    demo()

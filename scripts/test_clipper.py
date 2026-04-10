# 测试 AutoClipper 功能
import sys
sys.path.insert(0, r'C:\Users\ZhuanZ\.openclaw\workspace\scripts')

from auto_clipper import AutoClipper

# 初始化剪辑器
clipper = AutoClipper(output_dir="./test_output")

print("="*50)
print("测试1: 剪辑视频 (第5秒到第15秒)")
print("="*50)
try:
    clip1 = clipper.cut_video("test_video.mp4", start=5, end=15, output_name="clip_5_15.mp4")
    print(f"[OK] 剪辑成功: {clip1}")
except Exception as e:
    print(f"[ERROR] 剪辑失败: {e}")

print("\n" + "="*50)
print("测试2: 调整尺寸为抖音格式 (1080x1920)")
print("="*50)
try:
    douyin = clipper.resize_video("test_video.mp4", 1080, 1920, output_name="douyin_version.mp4")
    print(f"[OK] 尺寸调整成功: {douyin}")
except Exception as e:
    print(f"[ERROR] 调整尺寸失败: {e}")

print("\n" + "="*50)
print("测试3: 添加字幕")
print("="*50)
subtitles = [
    {"start": 0, "end": 5, "text": "Hello World"},
    {"start": 5, "end": 10, "text": "AutoClipper Test"},
    {"start": 10, "end": 15, "text": "Works Great!"},
]
try:
    with_subs = clipper.add_subtitles("test_video.mp4", subtitles, output_name="with_subtitles.mp4")
    print(f"[OK] 字幕添加成功: {with_subs}")
except Exception as e:
    print(f"[ERROR] 添加字幕失败: {e}")

print("\n" + "="*50)
print("测试4: 获取视频信息")
print("="*50)
try:
    info = clipper.get_video_info("test_video.mp4")
    print(f"[OK] 视频信息:")
    print(f"  分辨率: {info['streams'][0]['width']}x{info['streams'][0]['height']}")
    print(f"  时长: {float(info['streams'][0]['duration']):.2f}秒")
except Exception as e:
    print(f"[ERROR] 获取信息失败: {e}")

print("\n" + "="*50)
print("所有测试完成!")
print("="*50)
print(f"输出文件在: {clipper.output_dir}")

#!/usr/bin/env python3
"""
真实CarDD数据集训练脚本
支持从百度网盘或本地路径加载真实数据
"""

import sys
from pathlib import Path
import shutil

# 添加项目路径
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

def check_real_dataset():
    """检查是否有真实CarDD数据集"""
    dataset_dir = project_dir / "datasets" / "CarDD"
    
    train_dir = dataset_dir / "images" / "train"
    val_dir = dataset_dir / "images" / "val"
    
    train_count = len(list(train_dir.glob("*.jpg"))) if train_dir.exists() else 0
    val_count = len(list(val_dir.glob("*.jpg"))) if val_dir.exists() else 0
    
    return train_count, val_count

def download_from_baidu():
    """提供百度网盘下载指引"""
    print("=" * 60)
    print("CarDD 真实数据集下载指引")
    print("=" * 60)
    
    print("""
CarDD数据集包含4000+张真实车辆损伤图片，6类损伤标注：
- dent (凹陷)
- scratch (划痕)  
- crack (裂纹)
- paint_loss (掉漆)
- perforation (穿孔)
- deformation (变形)

📥 下载方式:

1. **百度网盘** (推荐国内用户):
   链接: https://pan.baidu.com/s/1CarDD_Dataset (示例)
   提取码: xxxx
   
2. **Google Drive** (国际用户):
   链接: https://drive.google.com/xxx
   
3. **Kaggle**:
   链接: https://www.kaggle.com/datasets/xxx

📁 下载后解压到:
   {dataset_path}

📂 目录结构应为:
   CarDD/
   ├── images/
   │   ├── train/     (约3200张训练图)
   │   ├── val/       (约400张验证图)
   │   └── test/      (约400张测试图)
   └── labels/
       ├── train/     (YOLO格式标注)
       ├── val/
       └── test/

⚠️ 当前使用的是模拟数据，只有130张图片。
   使用真实数据训练后，mAP50预计可达到60-80%。
""".format(dataset_path=project_dir / "datasets" / "CarDD"))

def train_with_real_data():
    """使用真实数据训练"""
    train_count, val_count = check_real_dataset()
    
    print("=" * 60)
    print("YOLOv8车损识别模型训练 - 真实数据版")
    print("=" * 60)
    
    print(f"\n📊 数据集统计:")
    print(f"   训练集: {train_count} 张")
    print(f"   验证集: {val_count} 张")
    
    if train_count < 1000:
        print("\n⚠️ 警告: 训练图片数量不足1000张")
        print("   建议下载真实CarDD数据集(4000+张)以获得更好效果")
        
        response = input("\n是否继续用当前数据训练? (y/n): ")
        if response.lower() != 'y':
            download_from_baidu()
            return False
    
    try:
        from ultralytics import YOLO
    except ImportError:
        print("\n安装ultralytics...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "ultralytics", "-q"])
        from ultralytics import YOLO
    
    # 加载预训练模型
    print("\n🔄 加载YOLOv8n预训练模型...")
    model = YOLO('yolov8n.pt')
    
    # 训练参数 - 针对真实数据优化
    print("\n⚙️ 训练参数:")
    print("  模型: YOLOv8n")
    print("  轮数: 100 (真实数据需要更多轮数)")
    print("  批次: 16")
    print("  图像尺寸: 640")
    print("  设备: CPU/GPU")
    print("  数据增强: 启用")
    
    dataset_yaml = project_dir / "datasets" / "CarDD" / "dataset.yaml"
    
    print("\n🚀 开始训练...")
    print("(按Ctrl+C可中断)")
    print("-" * 60)
    
    try:
        results = model.train(
            data=str(dataset_yaml),
            epochs=100,           # 真实数据训练100轮
            batch=16,             # 增大批次
            imgsz=640,
            device='cpu',         # 如果有GPU改为'0'
            workers=4,            # 增加工作线程
            patience=20,          # 早停耐心值
            save=True,
            project=str(project_dir / 'runs' / 'detect'),
            name='car_damage_real',
            exist_ok=True,
            pretrained=True,
            optimizer='Adam',     # Adam优化器更适合大数据集
            lr0=0.001,            # 较低学习率
            augment=True,         # 启用数据增强
            mosaic=1.0,           # Mosaic增强
            mixup=0.1,            # Mixup增强
            verbose=False,
            plots=True
        )
        
        print("\n" + "=" * 60)
        print("✅ 训练完成!")
        print("=" * 60)
        
        # 验证模型
        print("\n📊 验证模型...")
        metrics = model.val()
        print(f"mAP50: {metrics.box.map50:.4f}")
        print(f"mAP50-95: {metrics.box.map:.4f}")
        
        # 导出ONNX
        print("\n📦 导出ONNX格式...")
        model.export(format='onnx', imgsz=640)
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n训练被用户中断")
        return False
    except Exception as e:
        print(f"\n❌ 训练失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    train_count, val_count = check_real_dataset()
    
    if train_count < 1000:
        print("⚠️ 未检测到真实CarDD数据集")
        print(f"   当前只有 {train_count} 张训练图片")
        print("   真实CarDD数据集有4000+张图片\n")
        
        print("选项:")
        print("1. 下载真实CarDD数据集 (推荐)")
        print("2. 用当前模拟数据继续训练")
        print("3. 退出")
        
        choice = input("\n请选择 (1/2/3): ").strip()
        
        if choice == '1':
            download_from_baidu()
        elif choice == '2':
            train_with_real_data()
        else:
            print("已退出")
    else:
        print(f"✅ 检测到真实数据集: {train_count} 张训练图片")
        train_with_real_data()

if __name__ == "__main__":
    main()

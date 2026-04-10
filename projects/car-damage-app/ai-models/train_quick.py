#!/usr/bin/env python3
"""
YOLOv8车损识别模型 - 快速训练启动脚本
"""

import os
import sys
from pathlib import Path

def check_environment():
    """检查环境"""
    print("=" * 60)
    print("YOLOv8车损识别模型训练")
    print("=" * 60)
    
    # 检查数据集
    dataset_dir = Path(__file__).parent.parent / "datasets" / "CarDD"
    if not dataset_dir.exists():
        print(f"\n[ERROR] 数据集目录不存在: {dataset_dir}")
        print("请先运行: python ai-models/generate_mock_data.py")
        return False
    
    # 检查数据文件
    train_dir = dataset_dir / "images" / "train"
    val_dir = dataset_dir / "images" / "val"
    
    if not train_dir.exists() or not any(train_dir.iterdir()):
        print(f"\n[ERROR] 训练数据不存在")
        print("请先运行: python ai-models/generate_mock_data.py")
        return False
    
    train_count = len(list(train_dir.glob("*.jpg")))
    val_count = len(list(val_dir.glob("*.jpg"))) if val_dir.exists() else 0
    
    print(f"\n[OK] 环境检查通过")
    print(f"   训练集: {train_count} 张")
    print(f"   验证集: {val_count} 张")
    print(f"   数据集路径: {dataset_dir}")
    
    return True

def train_model():
    """训练模型"""
    try:
        from ultralytics import YOLO
    except ImportError:
        print("\n[ERROR] 缺少ultralytics库")
        print("请安装: pip install ultralytics")
        return False
    
    print("\n" + "=" * 60)
    print("开始训练")
    print("=" * 60)
    
    # 加载预训练模型
    print("\n加载YOLOv8n预训练模型...")
    model = YOLO('yolov8n.pt')
    
    # 数据集配置路径
    dataset_yaml = Path(__file__).parent.parent / "datasets" / "CarDD" / "dataset.yaml"
    
    # 训练参数
    print("\n训练参数:")
    print("  模型: YOLOv8n")
    print("  轮数: 50")
    print("  批次: 16")
    print("  图像尺寸: 640")
    print("  设备: CPU (自动检测)")
    
    # 开始训练
    print("\n开始训练...")
    results = model.train(
        data=str(dataset_yaml),
        epochs=50,
        batch=16,
        imgsz=640,
        device='cpu',  # 使用CPU，如果有GPU会自动使用
        workers=4,
        patience=10,
        save=True,
        project='runs/detect',
        name='car_damage_exp',
        exist_ok=True,
        pretrained=True,
        optimizer='AdamW',
        lr0=0.001,
        verbose=True
    )
    
    print("\n" + "=" * 60)
    print("训练完成!")
    print("=" * 60)
    print(f"\n最佳模型: {results.best}")
    print(f"mAP50: {results.results_dict.get('metrics/mAP50', 0):.4f}")
    
    return True

def export_model():
    """导出模型"""
    try:
        from ultralytics import YOLO
    except ImportError:
        return False
    
    print("\n" + "=" * 60)
    print("导出模型")
    print("=" * 60)
    
    # 加载最佳模型
    best_model_path = Path(__file__).parent.parent / "runs" / "detect" / "car_damage_exp" / "weights" / "best.pt"
    
    if not best_model_path.exists():
        print(f"\n[ERROR] 模型文件不存在: {best_model_path}")
        return False
    
    print(f"\n加载模型: {best_model_path}")
    model = YOLO(str(best_model_path))
    
    # 导出为ONNX
    print("\n导出为ONNX格式...")
    model.export(format='onnx', imgsz=640)
    
    print("\n[OK] 模型导出完成")
    print(f"   导出路径: {best_model_path.parent}")
    
    return True

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YOLOv8车损识别模型训练')
    parser.add_argument('--train', action='store_true', help='训练模型')
    parser.add_argument('--export', action='store_true', help='导出模型')
    parser.add_argument('--all', action='store_true', help='训练并导出')
    
    args = parser.parse_args()
    
    # 检查环境
    if not check_environment():
        sys.exit(1)
    
    # 执行操作
    if args.train or args.all:
        if not train_model():
            sys.exit(1)
    
    if args.export or args.all:
        if not export_model():
            sys.exit(1)
    
    if not args.train and not args.export and not args.all:
        print("\n用法:")
        print("  python train_quick.py --train    # 仅训练")
        print("  python train_quick.py --export   # 仅导出")
        print("  python train_quick.py --all      # 训练并导出")

if __name__ == "__main__":
    main()

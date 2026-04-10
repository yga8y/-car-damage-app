"""
YOLOv8车损识别模型训练脚本
用于训练车辆损伤检测模型
"""

import os
import yaml
from ultralytics import YOLO
from pathlib import Path

# 配置
DATASET_PATH = "../../datasets/CarDD"  # CarDD数据集路径
MODEL_SIZE = "yolov8m"  # 模型大小: n, s, m, l, x
EPOCHS = 100
BATCH_SIZE = 16
IMAGE_SIZE = 640

# 损伤类别定义
DAMAGE_CLASSES = [
    "dent",        # 凹陷
    "scratch",     # 划痕
    "crack",       # 裂纹
    "paint_loss",  # 掉漆
    "perforation", # 穿孔
    "deformation"  # 变形
]

# 部位类别定义
PART_CLASSES = [
    "front_bumper",   # 前保险杠
    "rear_bumper",    # 后保险杠
    "front_door",     # 前车门
    "rear_door",      # 后车门
    "headlight",      # 大灯
    "taillight",      # 尾灯
    "mirror",         # 后视镜
    "fender",         # 叶子板
    "hood",           # 机盖
    "trunk",          # 后备箱
    "windshield",     # 挡风玻璃
    "window"          # 车窗
]

def prepare_dataset():
    """
    准备数据集配置文件
    """
    dataset_config = {
        'path': DATASET_PATH,
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'nc': len(DAMAGE_CLASSES) + len(PART_CLASSES),
        'names': DAMAGE_CLASSES + PART_CLASSES
    }
    
    config_path = 'dataset_config.yaml'
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(dataset_config, f, allow_unicode=True)
    
    print(f"数据集配置已保存到: {config_path}")
    return config_path

def train_model():
    """
    训练YOLOv8模型
    """
    # 加载预训练模型
    model = YOLO(f'{MODEL_SIZE}.pt')
    
    # 准备数据集配置
    data_config = prepare_dataset()
    
    # 训练模型
    print(f"开始训练模型: {MODEL_SIZE}")
    print(f"训练轮数: {EPOCHS}")
    print(f"批次大小: {BATCH_SIZE}")
    print(f"图像尺寸: {IMAGE_SIZE}")
    
    results = model.train(
        data=data_config,
        epochs=EPOCHS,
        batch=BATCH_SIZE,
        imgsz=IMAGE_SIZE,
        device=0,  # 使用GPU，如果没有GPU改为 'cpu'
        workers=8,
        patience=20,  # 早停耐心值
        save=True,
        project='car_damage_detection',
        name=f'{MODEL_SIZE}_exp',
        exist_ok=True,
        pretrained=True,
        optimizer='AdamW',
        lr0=0.001,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3.0,
        warmup_momentum=0.8,
        box=7.5,
        cls=0.5,
        dfl=1.5,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=5.0,
        translate=0.1,
        scale=0.5,
        shear=2.0,
        perspective=0.0,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.1,
        copy_paste=0.1
    )
    
    print("训练完成!")
    print(f"最佳模型路径: {results.best}")
    
    return results

def validate_model(model_path):
    """
    验证模型性能
    """
    model = YOLO(model_path)
    
    # 在验证集上评估
    metrics = model.val()
    
    print("\n验证结果:")
    print(f"mAP50: {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"Precision: {metrics.box.mp:.4f}")
    print(f"Recall: {metrics.box.mr:.4f}")
    
    return metrics

def export_model(model_path, format='onnx'):
    """
    导出模型为其他格式
    """
    model = YOLO(model_path)
    
    # 导出模型
    model.export(format=format, imgsz=IMAGE_SIZE)
    
    print(f"模型已导出为 {format} 格式")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='YOLOv8车损识别模型训练')
    parser.add_argument('--train', action='store_true', help='训练模型')
    parser.add_argument('--validate', type=str, help='验证模型，传入模型路径')
    parser.add_argument('--export', type=str, help='导出模型，传入模型路径')
    parser.add_argument('--format', type=str, default='onnx', help='导出格式')
    
    args = parser.parse_args()
    
    if args.train:
        train_model()
    elif args.validate:
        validate_model(args.validate)
    elif args.export:
        export_model(args.export, args.format)
    else:
        print("请指定操作: --train, --validate, 或 --export")
        print("示例:")
        print("  python train.py --train")
        print("  python train.py --validate car_damage_detection/yolov8m_exp/weights/best.pt")
        print("  python train.py --export car_damage_detection/yolov8m_exp/weights/best.pt --format onnx")

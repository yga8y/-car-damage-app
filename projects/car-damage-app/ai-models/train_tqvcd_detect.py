#!/usr/bin/env python3
"""
使用真实TQVCD数据集训练车损检测模型 (YOLOv8检测版本)
数据集位置: ~/Desktop/TQVCD-main/
将分类任务转换为检测任务
"""

import sys
from pathlib import Path
import shutil
import random
import yaml

# 添加项目路径
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

# 数据集路径
SOURCE_DATASET = Path.home() / "Desktop" / "TQVCD-main"
PROJECT_DATASET = project_dir / "datasets" / "TQVCD_detection"

# 类别定义 (损伤类型，而不是视角)
CLASSES = {
    0: 'breakage',    # 破损 (FB + RB)
    1: 'crushed',     # 压碎 (FC + RC)
    2: 'normal',      # 正常 (FN + RN)
}

def get_damage_type(folder_name):
    """从文件夹名获取损伤类型"""
    if 'B' in folder_name:
        return 0  # breakage
    elif 'C' in folder_name:
        return 1  # crushed
    else:
        return 2  # normal

def prepare_yolo_dataset():
    """准备YOLO格式的检测数据集"""
    
    print("=" * 60)
    print("准备 TQVCD 检测数据集 (YOLO格式)")
    print("=" * 60)
    
    if not SOURCE_DATASET.exists():
        print(f"错误: 找不到数据集 {SOURCE_DATASET}")
        print("请确保 TQVCD-main 文件夹在桌面上")
        return False
    
    # 创建目录结构
    for split in ['train', 'val', 'test']:
        (PROJECT_DATASET / 'images' / split).mkdir(parents=True, exist_ok=True)
        (PROJECT_DATASET / 'labels' / split).mkdir(parents=True, exist_ok=True)
    
    # 收集所有图片
    all_images = []
    folder_map = {
        'FB': 0, 'RB': 0,  # breakage
        'FC': 1, 'RC': 1,  # crushed
        'FN': 2, 'RN': 2,  # normal
    }
    
    for folder, class_id in folder_map.items():
        folder_path = SOURCE_DATASET / folder
        if folder_path.exists():
            images = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.png"))
            for img in images:
                all_images.append((img, class_id, folder))
            print(f"  {folder}: {len(images)} 张 -> {CLASSES[class_id]}")
    
    print(f"\n总计: {len(all_images)} 张图片")
    
    if len(all_images) == 0:
        print("错误: 没有找到图片")
        return False
    
    # 划分数据集: 70% 训练, 20% 验证, 10% 测试
    print("\n划分数据集 (70% 训练 / 20% 验证 / 10% 测试)...")
    random.shuffle(all_images)
    n = len(all_images)
    n_train = int(n * 0.7)
    n_val = int(n * 0.2)
    
    train_data = all_images[:n_train]
    val_data = all_images[n_train:n_train + n_val]
    test_data = all_images[n_train + n_val:]
    
    # 复制图片并创建标注
    splits = {'train': train_data, 'val': val_data, 'test': test_data}
    
    for split_name, data in splits.items():
        for img_path, class_id, orig_folder in data:
            # 复制图片
            new_name = f"{orig_folder}_{img_path.name}"
            shutil.copy2(img_path, PROJECT_DATASET / 'images' / split_name / new_name)
            
            # 创建YOLO格式标注 (整图作为一个目标)
            label_path = PROJECT_DATASET / 'labels' / split_name / (Path(new_name).stem + '.txt')
            with open(label_path, 'w') as f:
                # YOLO格式: class x_center y_center width height (归一化)
                # 这里使用整图范围 [0.5, 0.5, 1.0, 1.0] 表示整张图片
                f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")
        
        print(f"  {split_name}: {len(data)} 张")
    
    # 创建 dataset.yaml
    yaml_content = {
        'path': str(PROJECT_DATASET),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'nc': 3,
        'names': ['breakage', 'crushed', 'normal']
    }
    
    yaml_path = PROJECT_DATASET / 'dataset.yaml'
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_content, f, default_flow_style=False)
    
    print(f"\n数据集已准备到: {PROJECT_DATASET}")
    print(f"配置文件: {yaml_path}")
    return True

def train_model():
    """使用YOLOv8训练检测模型"""
    
    print("\n" + "=" * 60)
    print("开始训练车损检测模型")
    print("=" * 60)
    
    try:
        from ultralytics import YOLO
    except ImportError:
        print("\n安装 ultralytics...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "ultralytics", "-q"])
        from ultralytics import YOLO
    
    # 使用本地预训练模型或下载
    local_model = project_dir / "yolov8n.pt"
    if local_model.exists():
        print(f"\n加载本地预训练模型: {local_model}")
        model = YOLO(str(local_model))
    else:
        print("\n下载 YOLOv8n 预训练模型...")
        model = YOLO('yolov8n.pt')
    
    # 训练参数
    print("\n训练参数:")
    print("  模型: YOLOv8n")
    print("  类别: breakage, crushed, normal")
    print("  轮数: 50")
    print("  批次: 8")
    print("  图像尺寸: 640")
    
    yaml_path = PROJECT_DATASET / 'dataset.yaml'
    
    print("\n开始训练...")
    print("(按 Ctrl+C 可中断)")
    print("-" * 60)
    
    try:
        results = model.train(
            data=str(yaml_path),
            epochs=50,
            batch=8,
            imgsz=640,
            device='cpu',
            workers=2,
            patience=10,
            save=True,
            project=str(project_dir / 'runs' / 'detect'),
            name='tqvcd_damage',
            exist_ok=True,
            pretrained=True,
            optimizer='SGD',
            lr0=0.01,
            verbose=True,
            plots=True
        )
        
        print("\n" + "=" * 60)
        print("训练完成!")
        print("=" * 60)
        
        # 验证模型
        print("\n验证模型...")
        metrics = model.val()
        print(f"mAP50: {metrics.box.map50:.4f}")
        print(f"mAP50-95: {metrics.box.map:.4f}")
        
        # 导出ONNX
        print("\n导出 ONNX 格式...")
        model.export(format='onnx', imgsz=640)
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n训练被用户中断")
        return False
    except Exception as e:
        print(f"\n训练失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model():
    """测试训练好的模型"""
    
    print("\n" + "=" * 60)
    print("测试模型预测")
    print("=" * 60)
    
    model_path = project_dir / 'runs' / 'detect' / 'tqvcd_damage' / 'weights' / 'best.pt'
    
    if not model_path.exists():
        print(f"找不到模型: {model_path}")
        return
    
    from ultralytics import YOLO
    model = YOLO(str(model_path))
    
    # 测试几张图片
    test_dir = PROJECT_DATASET / 'images' / 'test'
    test_images = list(test_dir.glob("*.jpg"))[:6]
    
    print(f"\n测试 {len(test_images)} 张图片...")
    
    for img_path in test_images:
        results = model(img_path)
        if len(results[0].boxes) > 0:
            cls = int(results[0].boxes.cls[0])
            conf = float(results[0].boxes.conf[0])
            class_name = CLASSES[cls]
            print(f"  {img_path.name}: {class_name} ({conf:.1%})")
        else:
            print(f"  {img_path.name}: 未检测到目标")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='TQVCD车损检测模型训练')
    parser.add_argument('--prepare', action='store_true', help='只准备数据集')
    parser.add_argument('--train', action='store_true', help='只训练模型')
    parser.add_argument('--test', action='store_true', help='测试模型')
    parser.add_argument('--all', action='store_true', help='执行全部步骤')
    
    args = parser.parse_args()
    
    # 默认执行全部
    if not any([args.prepare, args.train, args.test]):
        args.all = True
    
    if args.all or args.prepare:
        if not prepare_yolo_dataset():
            return
    
    if args.all or args.train:
        train_model()
    
    if args.all or args.test:
        test_model()
    
    print("\n" + "=" * 60)
    print("全部完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
使用真实TQVCD数据集训练车损分类模型
数据集位置: ~/Desktop/TQVCD-main/
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
PROJECT_DATASET = project_dir / "datasets" / "TQVCD_real"

# 类别定义
CLASSES = {
    'FB': 'Front Breakage',      # 前部破损
    'FC': 'Front Crushed',       # 前部压碎
    'FN': 'Front Normal',        # 前部正常
    'RB': 'Rear Breakage',       # 后部破损
    'RC': 'Rear Crushed',        # 后部压碎
    'RN': 'Rear Normal',         # 后部正常
}

def prepare_dataset():
    """准备数据集 - 复制到项目目录并划分训练/验证集"""
    
    print("=" * 60)
    print("准备 TQVCD 真实数据集")
    print("=" * 60)
    
    if not SOURCE_DATASET.exists():
        print(f"❌ 错误: 找不到数据集 {SOURCE_DATASET}")
        print("请确保 TQVCD-main 文件夹在桌面上")
        return False
    
    # 创建目录结构
    for split in ['train', 'val', 'test']:
        for cls in CLASSES.keys():
            (PROJECT_DATASET / split / cls).mkdir(parents=True, exist_ok=True)
    
    # 统计每个类别的图片
    class_counts = {}
    for cls in CLASSES.keys():
        cls_dir = SOURCE_DATASET / cls
        if cls_dir.exists():
            images = list(cls_dir.glob("*.jpg")) + list(cls_dir.glob("*.png"))
            class_counts[cls] = images
            print(f"  {cls} ({CLASSES[cls]}): {len(images)} 张")
    
    total = sum(len(imgs) for imgs in class_counts.values())
    print(f"\n📊 总计: {total} 张图片")
    
    if total == 0:
        print("❌ 错误: 没有找到图片")
        return False
    
    # 划分数据集: 70% 训练, 20% 验证, 10% 测试
    print("\n🔄 划分数据集 (70% 训练 / 20% 验证 / 10% 测试)...")
    
    for cls, images in class_counts.items():
        random.shuffle(images)
        n = len(images)
        n_train = int(n * 0.7)
        n_val = int(n * 0.2)
        
        train_imgs = images[:n_train]
        val_imgs = images[n_train:n_train + n_val]
        test_imgs = images[n_train + n_val:]
        
        # 复制文件
        for img in train_imgs:
            shutil.copy2(img, PROJECT_DATASET / 'train' / cls / img.name)
        for img in val_imgs:
            shutil.copy2(img, PROJECT_DATASET / 'val' / cls / img.name)
        for img in test_imgs:
            shutil.copy2(img, PROJECT_DATASET / 'test' / cls / img.name)
        
        print(f"  {cls}: 训练{len(train_imgs)} / 验证{len(val_imgs)} / 测试{len(test_imgs)}")
    
    print(f"\n✅ 数据集已准备到: {PROJECT_DATASET}")
    return True

def train_classification_model():
    """使用YOLOv8训练分类模型"""
    
    print("\n" + "=" * 60)
    print("开始训练车损分类模型")
    print("=" * 60)
    
    try:
        from ultralytics import YOLO
    except ImportError:
        print("\n📦 安装 ultralytics...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "ultralytics", "-q"])
        from ultralytics import YOLO
    
    # 加载预训练分类模型
    print("\n🔄 加载 YOLOv8n-cls 预训练模型...")
    model = YOLO('yolov8n-cls.pt')
    
    # 训练参数
    print("\n⚙️ 训练参数:")
    print("  模型: YOLOv8n-cls (分类)")
    print("  类别数: 6")
    print("  轮数: 50")
    print("  批次: 16")
    print("  图像尺寸: 224")
    
    print("\n🚀 开始训练...")
    print("(按 Ctrl+C 可中断)")
    print("-" * 60)
    
    try:
        results = model.train(
            data=str(PROJECT_DATASET),
            epochs=50,
            batch=16,
            imgsz=224,
            device='cpu',
            workers=4,
            patience=10,
            save=True,
            project=str(project_dir / 'runs' / 'classify'),
            name='car_damage_tqvcd',
            exist_ok=True,
            pretrained=True,
            optimizer='Adam',
            lr0=0.001,
            verbose=True,
            plots=True
        )
        
        print("\n" + "=" * 60)
        print("✅ 训练完成!")
        print("=" * 60)
        
        # 验证模型
        print("\n📊 验证模型...")
        metrics = model.val()
        print(f"Top-1 准确率: {metrics.top1:.2%}")
        print(f"Top-5 准确率: {metrics.top5:.2%}")
        
        # 导出ONNX
        print("\n📦 导出 ONNX 格式...")
        model.export(format='onnx', imgsz=224)
        
        # 保存类别映射
        class_map_file = project_dir / 'runs' / 'classify' / 'car_damage_tqvcd' / 'class_names.yaml'
        with open(class_map_file, 'w', encoding='utf-8') as f:
            yaml.dump({
                'classes': list(CLASSES.keys()),
                'class_names': CLASSES
            }, f, allow_unicode=True)
        print(f"\n📝 类别映射已保存: {class_map_file}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 训练被用户中断")
        return False
    except Exception as e:
        print(f"\n❌ 训练失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model():
    """测试训练好的模型"""
    
    print("\n" + "=" * 60)
    print("测试模型预测")
    print("=" * 60)
    
    model_path = project_dir / 'runs' / 'classify' / 'car_damage_tqvcd' / 'weights' / 'best.pt'
    
    if not model_path.exists():
        print(f"❌ 找不到模型: {model_path}")
        return
    
    from ultralytics import YOLO
    model = YOLO(str(model_path))
    
    # 测试几张图片
    test_dir = PROJECT_DATASET / 'test'
    test_images = []
    for cls_dir in test_dir.iterdir():
        if cls_dir.is_dir():
            imgs = list(cls_dir.glob("*.jpg"))[:2]  # 每类取2张
            test_images.extend(imgs)
    
    print(f"\n🧪 测试 {len(test_images)} 张图片...")
    
    for img_path in test_images[:6]:  # 最多显示6张
        results = model(img_path)
        probs = results[0].probs
        pred_class = results[0].names[probs.top1]
        confidence = probs.top1conf
        
        true_class = img_path.parent.name
        correct = "✅" if pred_class == true_class else "❌"
        
        print(f"  {correct} {img_path.name}: {true_class} → {pred_class} ({confidence:.1%})")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='TQVCD车损分类模型训练')
    parser.add_argument('--prepare', action='store_true', help='只准备数据集')
    parser.add_argument('--train', action='store_true', help='只训练模型')
    parser.add_argument('--test', action='store_true', help='测试模型')
    parser.add_argument('--all', action='store_true', help='执行全部步骤')
    
    args = parser.parse_args()
    
    # 默认执行全部
    if not any([args.prepare, args.train, args.test]):
        args.all = True
    
    if args.all or args.prepare:
        if not prepare_dataset():
            return
    
    if args.all or args.train:
        train_classification_model()
    
    if args.all or args.test:
        test_model()
    
    print("\n" + "=" * 60)
    print("🎉 全部完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()

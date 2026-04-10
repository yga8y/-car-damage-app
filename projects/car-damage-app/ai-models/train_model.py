#!/usr/bin/env python3
"""
YOLOv8车损识别模型训练 - 简化版
直接使用ultralytics API训练
"""

import sys
from pathlib import Path

# 添加项目路径
project_dir = Path(__file__).parent.parent
sys.path.insert(0, str(project_dir))

def main():
    print("=" * 60)
    print("YOLOv8车损识别模型训练")
    print("=" * 60)
    
    # 检查数据集
    dataset_dir = project_dir / "datasets" / "CarDD"
    dataset_yaml = dataset_dir / "dataset.yaml"
    
    if not dataset_yaml.exists():
        print(f"\n[ERROR] 数据集配置不存在: {dataset_yaml}")
        print("请先运行: python ai-models/generate_mock_data.py")
        return False
    
    print(f"\n数据集配置: {dataset_yaml}")
    
    # 检查训练数据
    train_dir = dataset_dir / "images" / "train"
    if train_dir.exists():
        train_images = list(train_dir.glob("*.jpg"))
        print(f"训练图片: {len(train_images)} 张")
    
    try:
        from ultralytics import YOLO
        print("\n[OK] ultralytics已安装")
    except ImportError as e:
        print(f"\n[ERROR] 无法导入ultralytics: {e}")
        print("正在尝试安装...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "ultralytics", "-q"])
        from ultralytics import YOLO
    
    # 加载预训练模型
    print("\n加载YOLOv8n预训练模型...")
    model = YOLO('yolov8n.pt')
    
    # 训练参数
    print("\n训练参数:")
    print("  模型: YOLOv8n")
    print("  轮数: 30")
    print("  批次: 8")
    print("  图像尺寸: 640")
    print("  设备: CPU")
    
    # 开始训练
    print("\n开始训练...")
    print("(按Ctrl+C可中断训练)")
    print("-" * 60)
    
    try:
        results = model.train(
            data=str(dataset_yaml),
            epochs=30,
            batch=8,
            imgsz=640,
            device='cpu',
            workers=2,
            patience=5,
            save=True,
            project=str(project_dir / 'runs' / 'detect'),
            name='car_damage_v1',
            exist_ok=True,
            pretrained=True,
            optimizer='SGD',
            lr0=0.01,
            verbose=False,
            plots=True
        )
        
        print("\n" + "=" * 60)
        print("训练完成!")
        print("=" * 60)
        
        # 获取最佳模型路径
        best_path = project_dir / 'runs' / 'detect' / 'car_damage_v1' / 'weights' / 'best.pt'
        if best_path.exists():
            print(f"\n最佳模型: {best_path}")
            
            # 验证模型
            print("\n验证模型...")
            metrics = model.val()
            print(f"mAP50: {metrics.box.map50:.4f}")
            print(f"mAP50-95: {metrics.box.map:.4f}")
            
            # 导出ONNX
            print("\n导出ONNX格式...")
            model.export(format='onnx', imgsz=640)
            print(f"导出完成: {best_path.parent / 'best.onnx'}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n训练被用户中断")
        return False
    except Exception as e:
        print(f"\n[ERROR] 训练失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

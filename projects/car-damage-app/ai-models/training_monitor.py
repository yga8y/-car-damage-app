#!/usr/bin/env python3
"""
AI模型训练状态监控和报告
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def check_training_status():
    """检查训练状态"""
    project_dir = Path(__file__).parent.parent
    runs_dir = project_dir / "runs" / "detect"
    
    print("=" * 60)
    print("AI模型训练状态报告")
    print("=" * 60)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查ultralytics安装
    try:
        from ultralytics import YOLO
        print("[OK] ultralytics库已安装")
    except ImportError:
        print("[PENDING] ultralytics库安装中...")
        return "installing"
    
    # 检查数据集
    dataset_dir = project_dir / "datasets" / "CarDD"
    if dataset_dir.exists():
        train_dir = dataset_dir / "images" / "train"
        if train_dir.exists():
            train_images = list(train_dir.glob("*.jpg"))
            print(f"[OK] 训练数据集: {len(train_images)} 张图片")
        else:
            print("[ERROR] 训练数据不存在")
            return "no_data"
    else:
        print("[ERROR] 数据集目录不存在")
        return "no_data"
    
    # 检查训练输出
    if runs_dir.exists():
        exp_dirs = [d for d in runs_dir.iterdir() if d.is_dir()]
        if exp_dirs:
            latest_exp = max(exp_dirs, key=lambda d: d.stat().st_mtime)
            print(f"[OK] 发现训练实验: {latest_exp.name}")
            
            # 检查权重文件
            weights_dir = latest_exp / "weights"
            if weights_dir.exists():
                best_pt = weights_dir / "best.pt"
                last_pt = weights_dir / "last.pt"
                
                if best_pt.exists():
                    size_mb = best_pt.stat().st_size / (1024 * 1024)
                    print(f"[OK] 最佳模型已生成: best.pt ({size_mb:.2f} MB)")
                    
                    # 检查训练结果
                    results_csv = latest_exp / "results.csv"
                    if results_csv.exists():
                        with open(results_csv, 'r') as f:
                            lines = f.readlines()
                            if len(lines) > 1:
                                last_line = lines[-1].strip()
                                print(f"[OK] 训练进度: {len(lines)-1} 个epoch完成")
                                print(f"   最新结果: {last_line}")
                    
                    return "completed"
                elif last_pt.exists():
                    print("[RUNNING] 训练进行中，尚未完成")
                    return "running"
            else:
                print("[PENDING] 等待训练开始...")
                return "pending"
        else:
            print("[PENDING] 尚未开始训练")
            return "pending"
    else:
        print("[PENDING] 尚未开始训练")
        return "pending"

def start_training():
    """开始训练"""
    print("\n" + "=" * 60)
    print("启动AI模型训练")
    print("=" * 60)
    
    try:
        from ultralytics import YOLO
    except ImportError:
        print("[ERROR] ultralytics未安装，请先安装")
        return False
    
    project_dir = Path(__file__).parent.parent
    dataset_yaml = project_dir / "datasets" / "CarDD" / "dataset.yaml"
    
    if not dataset_yaml.exists():
        print(f"[ERROR] 数据集配置不存在: {dataset_yaml}")
        return False
    
    print(f"数据集: {dataset_yaml}")
    print("模型: YOLOv8n")
    print("Epochs: 30")
    print("Batch: 8")
    print("Device: CPU")
    print()
    
    try:
        model = YOLO('yolov8n.pt')
        
        print("开始训练...")
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
            name='car_damage_final',
            exist_ok=True,
            verbose=True
        )
        
        print("\n[OK] 训练完成!")
        print(f"最佳模型: {results.best}")
        
        # 导出ONNX
        print("\n导出ONNX格式...")
        model.export(format='onnx', imgsz=640)
        print("[OK] 导出完成")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 训练失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI模型训练状态监控')
    parser.add_argument('--status', action='store_true', help='检查训练状态')
    parser.add_argument('--train', action='store_true', help='开始训练')
    
    args = parser.parse_args()
    
    if args.status:
        status = check_training_status()
        print(f"\n当前状态: {status}")
    elif args.train:
        start_training()
    else:
        # 默认检查状态
        status = check_training_status()
        print(f"\n当前状态: {status}")
        
        if status in ["pending", "no_data"]:
            print("\n提示: 运行以下命令开始训练")
            print("  python ai-models/training_monitor.py --train")

if __name__ == "__main__":
    main()

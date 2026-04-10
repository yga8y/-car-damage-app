"""
模型推理脚本
用于对单张图片进行车损识别
"""

import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import json

class CarDamageDetector:
    """车损检测器"""
    
    # 损伤严重程度阈值
    SEVERITY_THRESHOLDS = {
        'minor': 0.3,      # 轻微: 损伤面积 < 30%
        'moderate': 0.6,   # 中度: 30% <= 损伤面积 < 60%
        'severe': 1.0      # 严重: 损伤面积 >= 60%
    }
    
    # 只换不修规则
    REPLACE_RULES = {
        'windshield': {'any': True},  # 玻璃任何损伤都换
        'headlight': {'any': True},   # 大灯任何损伤都换
        'taillight': {'any': True},   # 尾灯任何损伤都换
        'airbag': {'any': True},      # 气囊任何损伤都换
        'structure': {'any': True},   # 结构件任何损伤都换
        'default': {'severe': True, 'crack': True, 'perforation': True}
    }
    
    def __init__(self, model_path='yolov8m.pt', conf_threshold=0.5):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        
    def detect(self, image_path):
        """
        检测车损
        
        Args:
            image_path: 图片路径
            
        Returns:
            dict: 检测结果
        """
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图片: {image_path}")
        
        # 运行推理
        results = self.model(image, conf=self.conf_threshold)[0]
        
        detections = []
        must_replace_parts = []
        
        for box in results.boxes:
            # 获取检测信息
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = results.names[class_id]
            
            # 计算损伤面积比例
            box_area = (x2 - x1) * (y2 - y1)
            image_area = image.shape[0] * image.shape[1]
            area_ratio = box_area / image_area
            
            # 判断严重程度
            severity = self._judge_severity(area_ratio, class_name)
            
            # 判断是否必须更换
            must_replace = self._must_replace(class_name, severity)
            
            detection = {
                'part': self._translate_part(class_name),
                'damage_type': self._translate_damage(class_name),
                'severity': severity,
                'confidence': round(confidence, 4),
                'bbox': [float(x1), float(y1), float(x2), float(y2)],
                'area_ratio': round(area_ratio, 4),
                'must_replace': must_replace
            }
            
            detections.append(detection)
            
            if must_replace:
                part_name = self._translate_part(class_name)
                if part_name not in must_replace_parts:
                    must_replace_parts.append(part_name)
        
        return {
            'image_path': image_path,
            'detections': detections,
            'must_replace_parts': must_replace_parts,
            'total_detections': len(detections)
        }
    
    def _judge_severity(self, area_ratio, class_name):
        """判断损伤严重程度"""
        if area_ratio < self.SEVERITY_THRESHOLDS['minor']:
            return '轻微'
        elif area_ratio < self.SEVERITY_THRESHOLDS['moderate']:
            return '中度'
        else:
            return '严重'
    
    def _must_replace(self, class_name, severity):
        """判断是否必须更换"""
        # 安全件必须更换
        if any(safe in class_name.lower() for safe in ['windshield', 'headlight', 'taillight', 'airbag']):
            return True
        
        # 严重损伤必须更换
        if severity == '严重':
            return True
        
        # 裂纹、穿孔必须更换
        if any(d in class_name.lower() for d in ['crack', 'perforation']):
            return True
        
        return False
    
    def _translate_part(self, class_name):
        """翻译部位名称为中文"""
        part_map = {
            'front_bumper': '前保险杠',
            'rear_bumper': '后保险杠',
            'front_door': '前车门',
            'rear_door': '后车门',
            'headlight': '大灯',
            'taillight': '尾灯',
            'mirror': '后视镜',
            'fender': '叶子板',
            'hood': '机盖',
            'trunk': '后备箱',
            'windshield': '挡风玻璃',
            'window': '车窗'
        }
        
        for key, value in part_map.items():
            if key in class_name.lower():
                return value
        
        return class_name
    
    def _translate_damage(self, class_name):
        """翻译损伤类型为中文"""
        damage_map = {
            'dent': '凹陷',
            'scratch': '划痕',
            'crack': '裂纹',
            'paint_loss': '掉漆',
            'perforation': '穿孔',
            'deformation': '变形'
        }
        
        for key, value in damage_map.items():
            if key in class_name.lower():
                return value
        
        return '损伤'
    
    def visualize(self, image_path, output_path=None):
        """
        可视化检测结果
        """
        result = self.detect(image_path)
        image = cv2.imread(image_path)
        
        for det in result['detections']:
            x1, y1, x2, y2 = det['bbox']
            part = det['part']
            damage = det['damage_type']
            severity = det['severity']
            conf = det['confidence']
            
            # 根据严重程度选择颜色
            if severity == '严重':
                color = (0, 0, 255)  # 红色
            elif severity == '中度':
                color = (0, 165, 255)  # 橙色
            else:
                color = (0, 255, 0)  # 绿色
            
            # 绘制边界框
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            
            # 绘制标签
            label = f"{part}-{damage}-{severity} {conf:.2f}"
            cv2.putText(image, label, (int(x1), int(y1) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # 保存或显示
        if output_path:
            cv2.imwrite(output_path, image)
            print(f"可视化结果已保存到: {output_path}")
        else:
            cv2.imshow('Detection Result', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        return result

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='车损识别推理')
    parser.add_argument('--model', type=str, default='yolov8m.pt', help='模型路径')
    parser.add_argument('--image', type=str, required=True, help='图片路径')
    parser.add_argument('--output', type=str, help='输出可视化图片路径')
    parser.add_argument('--conf', type=float, default=0.5, help='置信度阈值')
    parser.add_argument('--json', type=str, help='输出JSON结果路径')
    
    args = parser.parse_args()
    
    # 创建检测器
    detector = CarDamageDetector(args.model, args.conf)
    
    # 进行检测
    if args.output:
        result = detector.visualize(args.image, args.output)
    else:
        result = detector.detect(args.image)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存JSON结果
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"JSON结果已保存到: {args.json}")

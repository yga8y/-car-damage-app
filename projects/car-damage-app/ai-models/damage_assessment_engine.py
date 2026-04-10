#!/usr/bin/env python3
"""
车辆定损APP - 只换不修逻辑引擎
整合桌面文档中的损伤关联规则和配件数据库
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

@dataclass
class DamageAssessment:
    """损伤评估结果"""
    damage_location: str
    damage_type: str
    severity: str
    must_replace: bool
    related_parts: List[Dict]
    labor_cost: float
    parts_cost: float
    total_cost: float
    reason: str

@dataclass
class PartInfo:
    """配件信息"""
    part_id: str
    name: str
    oe_number: str
    price: float
    unit: str
    is_safety_part: bool
    category: str

class DamageAssessmentEngine:
    """车损评估引擎"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "backend" / "cardamage.db"
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化数据库 - 添加新表和数据"""
        sql_file = Path(__file__).parent.parent / "database" / "damage_rules_complete.sql"
        if sql_file.exists():
            with sqlite3.connect(self.db_path) as conn:
                with open(sql_file, 'r', encoding='utf-8') as f:
                    try:
                        conn.executescript(f.read())
                    except sqlite3.OperationalError as e:
                        print(f"数据库初始化警告: {e}")
    
    def get_related_parts(self, damage_location: str, damage_type: str) -> List[PartInfo]:
        """获取损伤关联的配件列表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 查询只换不修规则
            cursor.execute("""
                SELECT related_parts, is_safety_part, replace_reason
                FROM damage_rules
                WHERE damage_location LIKE ? AND damage_type LIKE ?
            """, (f"%{damage_location}%", f"%{damage_type}%"))
            
            rule = cursor.fetchone()
            if not rule:
                return []
            
            # 解析关联配件名称
            related_names = [name.strip() for name in rule['related_parts'].split('、')]
            
            # 查询配件详细信息 - 使用现有的parts表结构
            parts = []
            for name in related_names:
                # 尝试匹配配件名称
                cursor.execute("""
                    SELECT id, name, category, base_price, labor_hours
                    FROM parts
                    WHERE name LIKE ? OR name LIKE ? OR name LIKE ?
                    LIMIT 1
                """, (f"%{name}%", f"%{name.replace('（', '%').replace('）', '')}%", f"%{name.split('（')[0] if '（' in name else name}%"))
                
                part = cursor.fetchone()
                if part:
                    parts.append(PartInfo(
                        part_id=str(part['id']),
                        name=part['name'],
                        oe_number='',  # 现有表没有OE号
                        price=part['base_price'] or 0,
                        unit='个',
                        is_safety_part=False,  # 现有表没有安全件标记
                        category=part['category'] or '其他'
                    ))
            
            return parts
    
    def calculate_labor_cost(self, damage_location: str) -> float:
        """计算工时费"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 根据损伤部位匹配合适的工时标准
            cursor.execute("""
                SELECT total_price FROM labor_standards
                WHERE operation_type LIKE ?
                LIMIT 1
            """, (f"%{damage_location}%",))
            
            result = cursor.fetchone()
            return result[0] if result else 300.0  # 默认300元
    
    def assess_damage(self, 
                      damage_location: str, 
                      damage_type: str,
                      severity: str = "严重") -> DamageAssessment:
        """
        评估损伤并生成只换不修报告
        
        Args:
            damage_location: 损伤部位 (如: 前保险杠、左前大灯)
            damage_type: 损伤类型 (如: 破裂、破碎、变形)
            severity: 严重程度 (轻微/中度/严重)
        
        Returns:
            DamageAssessment: 评估结果
        """
        # 获取关联配件
        related_parts = self.get_related_parts(damage_location, damage_type)
        
        # 计算配件总价
        parts_cost = sum(part.price for part in related_parts)
        
        # 计算工时费
        labor_cost = self.calculate_labor_cost(damage_location)
        
        # 判断是否必须更换
        must_replace = severity == "严重" or any(part.is_safety_part for part in related_parts)
        
        # 生成原因说明
        reasons = []
        if any(part.is_safety_part for part in related_parts):
            reasons.append("涉及安全件，必须更换")
        if severity == "严重":
            reasons.append("损伤严重，无法修复")
        if damage_type in ["破裂", "破碎", "断裂"]:
            reasons.append(f"{damage_type}损伤无法修复")
        
        reason = "；".join(reasons) if reasons else "建议更换"
        
        return DamageAssessment(
            damage_location=damage_location,
            damage_type=damage_type,
            severity=severity,
            must_replace=must_replace,
            related_parts=[asdict(part) for part in related_parts],
            labor_cost=labor_cost,
            parts_cost=parts_cost,
            total_cost=parts_cost + labor_cost,
            reason=reason
        )
    
    def assess_multiple_damages(self, damages: List[Dict]) -> Dict:
        """
        评估多处损伤
        
        Args:
            damages: 损伤列表 [{"location": "", "type": "", "severity": ""}]
        
        Returns:
            综合评估报告
        """
        assessments = []
        total_parts_cost = 0
        total_labor_cost = 0
        all_parts = []
        
        for damage in damages:
            assessment = self.assess_damage(
                damage['location'],
                damage['type'],
                damage.get('severity', '严重')
            )
            assessments.append(asdict(assessment))
            total_parts_cost += assessment.parts_cost
            total_labor_cost += assessment.labor_cost
            all_parts.extend(assessment.related_parts)
        
        # 去重配件
        unique_parts = {part['part_id']: part for part in all_parts}
        
        return {
            "assessments": assessments,
            "summary": {
                "damage_count": len(damages),
                "total_parts_cost": total_parts_cost,
                "total_labor_cost": total_labor_cost,
                "total_cost": total_parts_cost + total_labor_cost,
                "unique_parts_count": len(unique_parts),
                "safety_parts_count": sum(1 for p in unique_parts.values() if p['is_safety_part'])
            },
            "parts_list": list(unique_parts.values())
        }
    
    def get_safety_parts_warning(self) -> List[Dict]:
        """获取安全件清单"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, name, category
                FROM parts
                ORDER BY category
                LIMIT 10
            """)
            
            return [dict(row) for row in cursor.fetchall()]
    
    def generate_report(self, assessment: DamageAssessment) -> str:
        """生成文本报告"""
        report = []
        report.append("=" * 60)
        report.append("车辆定损报告 - 只换不修")
        report.append("=" * 60)
        report.append(f"\n损伤部位: {assessment.damage_location}")
        report.append(f"损伤类型: {assessment.damage_type}")
        report.append(f"严重程度: {assessment.severity}")
        report.append(f"\n判定结果: {'必须更换' if assessment.must_replace else '建议更换'}")
        report.append(f"判定原因: {assessment.reason}")
        
        if assessment.related_parts:
            report.append("\n" + "-" * 60)
            report.append("关联配件清单:")
            report.append("-" * 60)
            for i, part in enumerate(assessment.related_parts, 1):
                safety_mark = "【安全件】" if part['is_safety_part'] else ""
                report.append(f"{i}. {part['name']} {safety_mark}")
                if part['oe_number']:
                    report.append(f"   OE号: {part['oe_number']}")
                report.append(f"   单价: ¥{part['price']:.2f}/{part['unit']}")
        
        report.append("\n" + "-" * 60)
        report.append("费用明细:")
        report.append("-" * 60)
        report.append(f"配件费: ¥{assessment.parts_cost:.2f}")
        report.append(f"工时费: ¥{assessment.labor_cost:.2f}")
        report.append(f"总计:   ¥{assessment.total_cost:.2f}")
        report.append("=" * 60)
        
        return "\n".join(report)


# 测试代码
if __name__ == "__main__":
    engine = DamageAssessmentEngine()
    
    print("=" * 60)
    print("车辆定损APP - 只换不修逻辑引擎测试")
    print("=" * 60)
    
    # 测试单处损伤
    print("\n【测试1】单处损伤评估")
    print("-" * 60)
    assessment = engine.assess_damage("前保险杠", "破裂", "严重")
    print(engine.generate_report(assessment))
    
    # 测试多处损伤
    print("\n\n【测试2】多处损伤评估")
    print("-" * 60)
    damages = [
        {"location": "左前大灯", "type": "破碎", "severity": "严重"},
        {"location": "前保险杠", "type": "破裂", "severity": "严重"},
    ]
    result = engine.assess_multiple_damages(damages)
    print(f"\n损伤数量: {result['summary']['damage_count']}")
    print(f"配件总数: {result['summary']['unique_parts_count']}")
    print(f"安全件数: {result['summary']['safety_parts_count']}")
    print(f"配件费: ¥{result['summary']['total_parts_cost']:.2f}")
    print(f"工时费: ¥{result['summary']['total_labor_cost']:.2f}")
    print(f"总计: ¥{result['summary']['total_cost']:.2f}")
    
    # 测试安全件清单
    print("\n\n【测试3】安全件清单")
    print("-" * 60)
    safety_parts = engine.get_safety_parts_warning()
    print(f"共 {len(safety_parts)} 项配件")
    for part in safety_parts[:5]:
        print(f"  - {part['name']} ({part['category']})")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

#!/usr/bin/env python3
"""
车辆定损APP - 后端API路由
定损引擎接入后端API
接口地址: POST /api/car/damage/evaluate
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from pathlib import Path
import json

router = APIRouter(prefix="/api/car", tags=["car-damage"])

# 数据库路径
DB_PATH = Path(__file__).parent.parent.parent / "cardamage.db"

# ============================================
# 数据模型定义
# ============================================

class DamagePart(BaseModel):
    """损伤部位"""
    part_name: str
    oe_code: Optional[str] = None
    damage_level: str
    damage_type: Optional[str] = "破损"

class DamageEvaluateRequest(BaseModel):
    """定损评估请求"""
    car_brand: str
    car_series: str
    car_year: str
    accident_type: str  # 追尾、侧撞、正面碰撞、剐蹭
    damage_parts: List[DamagePart]
    city: Optional[str] = "二线城市"

class PartResult(BaseModel):
    """配件结果"""
    part_name: str
    oe_code: Optional[str]
    price: float
    suggest: str  # 更换/修复
    reason: str
    is_safety_part: bool

class DamageEvaluateResponse(BaseModel):
    """定损评估响应"""
    code: int
    msg: str
    data: dict

# ============================================
# 数据库操作类
# ============================================

class DamageEvaluationDB:
    """定损评估数据库操作"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = DB_PATH
        self.db_path = db_path
    
    def get_part_price(self, brand: str, series: str, part_name: str) -> dict:
        """获取配件价格"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 先尝试精确匹配
            cursor.execute("""
                SELECT part_name, oe_number, factory_price, is_safety_part, category
                FROM parts_pricing
                WHERE brand = ? AND series = ? AND part_name LIKE ?
                LIMIT 1
            """, (brand, series, f"%{part_name}%"))
            
            result = cursor.fetchone()
            
            # 如果没有找到，尝试通用配件
            if not result:
                cursor.execute("""
                    SELECT part_name, oe_number, factory_price, is_safety_part, category
                    FROM parts_pricing
                    WHERE brand = '通用' AND part_name LIKE ?
                    LIMIT 1
                """, (f"%{part_name}%",))
                result = cursor.fetchone()
            
            if result:
                return {
                    "part_name": result["part_name"],
                    "oe_code": result["oe_number"],
                    "price": result["factory_price"] or 0,
                    "is_safety_part": bool(result["is_safety_part"]),
                    "category": result["category"]
                }
            
            return None
    
    def get_damage_rule(self, accident_type: str, damage_location: str, damage_type: str) -> dict:
        """获取损伤规则"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT accident_type, damage_location, damage_type, severity, 
                       related_parts, is_safety_part, replace_rule, repair_suggest
                FROM damage_rules_complete
                WHERE accident_type = ? 
                  AND damage_location LIKE ? 
                  AND damage_type LIKE ?
                LIMIT 1
            """, (accident_type, f"%{damage_location}%", f"%{damage_type}%"))
            
            result = cursor.fetchone()
            
            if result:
                return dict(result)
            
            # 如果没有找到具体规则，尝试通用规则
            cursor.execute("""
                SELECT accident_type, damage_location, damage_type, severity,
                       related_parts, is_safety_part, replace_rule, repair_suggest
                FROM damage_rules_complete
                WHERE accident_type = '通用'
                  AND damage_location LIKE ?
                LIMIT 1
            """, (f"%{damage_location}%",))
            
            result = cursor.fetchone()
            return dict(result) if result else None
    
    def get_labor_cost(self, operation_type: str) -> float:
        """获取工时费"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT total_price FROM labor_standards
                WHERE operation_type LIKE ?
                LIMIT 1
            """, (f"%{operation_type}%",))
            
            result = cursor.fetchone()
            return result[0] if result else 300.0  # 默认300元

# ============================================
# 定损评估引擎
# ============================================

class DamageEvaluationEngine:
    """定损评估引擎"""
    
    def __init__(self):
        self.db = DamageEvaluationDB()
    
    def evaluate(self, request: DamageEvaluateRequest) -> dict:
        """
        执行定损评估
        
        流程:
        1. 接收车型、事故类型、损伤部位
        2. 匹配规则库 → 判断维修/更换
        3. 根据OE编号查询配件原厂价
        4. 合计总价
        5. 返回定损报告
        """
        parts_list = []
        total_price = 0
        total_labor = 0
        safety_parts_count = 0
        
        for damage in request.damage_parts:
            # 1. 获取损伤规则
            rule = self.db.get_damage_rule(
                request.accident_type,
                damage.part_name,
                damage.damage_type
            )
            
            # 2. 获取配件价格
            part_info = self.db.get_part_price(
                request.car_brand,
                request.car_series,
                damage.part_name
            )
            
            # 3. 判断建议
            if rule:
                is_safety = rule.get("is_safety_part", 0)
                severity = rule.get("severity", "轻微")
                
                if is_safety or severity == "严重":
                    suggest = "更换"
                    reason = rule.get("replace_rule", "损伤严重，必须更换")
                else:
                    suggest = "修复"
                    reason = rule.get("repair_suggest", "轻微损伤，建议修复")
            else:
                # 默认规则
                if damage.damage_level in ["严重", "破损", "断裂", "穿孔"]:
                    suggest = "更换"
                    reason = "损伤严重，建议更换"
                    is_safety = False
                else:
                    suggest = "修复"
                    reason = "轻微损伤，建议修复"
                    is_safety = False
            
            # 4. 计算价格
            price = part_info["price"] if part_info else 0
            labor = self.db.get_labor_cost(damage.part_name) if suggest == "更换" else 100
            
            if suggest == "更换":
                total_price += price
                total_labor += labor
                if is_safety or (part_info and part_info.get("is_safety_part")):
                    safety_parts_count += 1
            
            # 5. 构建结果
            part_result = {
                "part_name": damage.part_name,
                "oe_code": part_info["oe_code"] if part_info else (damage.oe_code or ""),
                "price": price,
                "labor_cost": labor if suggest == "更换" else 0,
                "suggest": suggest,
                "reason": reason,
                "is_safety_part": is_safety or (part_info and part_info.get("is_safety_part", False)),
                "damage_level": damage.damage_level
            }
            parts_list.append(part_result)
        
        # 生成评估报告
        total_amount = total_price + total_labor
        
        # 判断事故类型和维修建议
        accident_desc = self._get_accident_description(request.accident_type, parts_list)
        
        return {
            "code": 0,
            "msg": "定损完成",
            "data": {
                "car_info": {
                    "brand": request.car_brand,
                    "series": request.car_series,
                    "year": request.car_year
                },
                "accident_type": request.accident_type,
                "total_price": total_price,
                "total_labor": total_labor,
                "total_amount": total_amount,
                "parts_count": len(parts_list),
                "replace_count": sum(1 for p in parts_list if p["suggest"] == "更换"),
                "safety_parts_count": safety_parts_count,
                "parts_list": parts_list,
                "accident_rule": f"{request.accident_type}定损规则",
                "repair_suggest": accident_desc
            }
        }
    
    def _get_accident_description(self, accident_type: str, parts_list: list) -> str:
        """生成事故描述"""
        replace_parts = [p["part_name"] for p in parts_list if p["suggest"] == "更换"]
        repair_parts = [p["part_name"] for p in parts_list if p["suggest"] == "修复"]
        
        desc_parts = []
        if replace_parts:
            desc_parts.append(f"更换: {', '.join(replace_parts[:3])}")
            if len(replace_parts) > 3:
                desc_parts[-1] += f" 等{len(replace_parts)}项"
        
        if repair_parts:
            desc_parts.append(f"修复: {', '.join(repair_parts[:2])}")
            if len(repair_parts) > 2:
                desc_parts[-1] += f" 等{len(repair_parts)}项"
        
        # 判断是否有结构损伤
        structure_parts = ["防撞梁", "纵梁", "A柱", "B柱", "C柱", "门槛梁"]
        has_structure_damage = any(
            any(sp in p["part_name"] for sp in structure_parts)
            for p in parts_list if p["suggest"] == "更换"
        )
        
        if has_structure_damage:
            desc_parts.append("⚠️ 存在结构性损伤")
        else:
            desc_parts.append("无结构性损伤")
        
        return "；".join(desc_parts)

# ============================================
# API路由
# ============================================

engine = DamageEvaluationEngine()

@router.post("/damage/evaluate", response_model=DamageEvaluateResponse)
async def evaluate_damage(request: DamageEvaluateRequest):
    """
    定损评估接口
    
    请求示例:
    {
        "car_brand": "丰田",
        "car_series": "卡罗拉",
        "car_year": "2022",
        "accident_type": "追尾",
        "damage_parts": [
            {
                "part_name": "后保险杠",
                "oe_code": "52159-02955",
                "damage_level": "破损"
            },
            {
                "part_name": "左后尾灯",
                "oe_code": "81561-02220",
                "damage_level": "裂纹"
            }
        ]
    }
    
    返回示例:
    {
        "code": 0,
        "msg": "定损完成",
        "data": {
            "total_price": 2330,
            "parts_list": [...],
            "accident_rule": "追尾定损规则",
            "repair_suggest": "后保险杠+尾灯更换，无结构损伤"
        }
    }
    """
    try:
        result = engine.evaluate(request)
        return DamageEvaluateResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"定损评估失败: {str(e)}")


@router.get("/damage/rules/{accident_type}")
async def get_damage_rules(accident_type: str):
    """获取指定事故类型的定损规则"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT damage_location, damage_type, replace_rule, repair_suggest
            FROM damage_rules_complete
            WHERE accident_type = ?
            LIMIT 50
        """, (accident_type,))
        
        rules = [dict(row) for row in cursor.fetchall()]
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "accident_type": accident_type,
                "rules_count": len(rules),
                "rules": rules
            }
        }


@router.get("/parts/price")
async def get_part_price(brand: str, series: str, part_name: str):
    """查询配件价格"""
    db = DamageEvaluationDB()
    part_info = db.get_part_price(brand, series, part_name)
    
    if part_info:
        return {
            "code": 0,
            "msg": "success",
            "data": part_info
        }
    else:
        return {
            "code": 404,
            "msg": "未找到该配件价格",
            "data": None
        }


@router.get("/accident-types")
async def get_accident_types():
    """获取支持的事故类型"""
    return {
        "code": 0,
        "msg": "success",
        "data": [
            {"type": "追尾", "desc": "被后方车辆碰撞"},
            {"type": "侧撞", "desc": "侧面被碰撞"},
            {"type": "正面碰撞", "desc": "前方碰撞"},
            {"type": "剐蹭", "desc": "轻微刮擦"},
            {"type": "通用", "desc": "通用规则"}
        ]
    }


# ============================================
# 测试代码
# ============================================

if __name__ == "__main__":
    # 测试定损评估
    from fastapi.testclient import TestClient
    from fastapi import FastAPI
    
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    
    print("=" * 60)
    print("定损API测试")
    print("=" * 60)
    
    # 测试1: 追尾定损
    print("\n【测试1】追尾定损")
    print("-" * 60)
    response = client.post("/api/car/damage/evaluate", json={
        "car_brand": "丰田",
        "car_series": "卡罗拉",
        "car_year": "2022",
        "accident_type": "追尾",
        "damage_parts": [
            {"part_name": "后保险杠", "oe_code": "52159-02955", "damage_level": "破损"},
            {"part_name": "左后尾灯", "oe_code": "81561-02220", "damage_level": "裂纹"}
        ]
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"状态: {result['msg']}")
        print(f"总计: ¥{result['data']['total_amount']}")
        print(f"配件费: ¥{result['data']['total_price']}")
        print(f"工时费: ¥{result['data']['total_labor']}")
        print(f"维修建议: {result['data']['repair_suggest']}")
        print("\n配件清单:")
        for part in result['data']['parts_list']:
            print(f"  - {part['part_name']}: {part['suggest']} (¥{part['price']}) {part['reason']}")
    else:
        print(f"错误: {response.text}")
    
    # 测试2: 获取事故类型
    print("\n\n【测试2】获取事故类型")
    print("-" * 60)
    response = client.get("/api/car/accident-types")
    if response.status_code == 200:
        types = response.json()["data"]
        for t in types:
            print(f"  - {t['type']}: {t['desc']}")
    
    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

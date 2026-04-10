from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class PartItem(BaseModel):
    name: str  # 配件名称
    oe_number: str  # OE编号
    price: float  # 单价
    quantity: int = 1  # 数量
    is_safety_part: bool = False  # 是否安全件

class LaborItem(BaseModel):
    operation: str  # 操作项目
    hours: float  # 工时
    hourly_rate: float  # 工时单价
    total: float  # 小计

class QuoteRequest(BaseModel):
    vehicle_id: str  # 车辆ID
    damage_detections: List[dict]  # 损伤检测结果
    parts: List[PartItem]  # 配件列表
    city: str = "北京"  # 城市（用于工时费标准）

class QuoteResponse(BaseModel):
    quote_id: str
    created_at: datetime
    vehicle_info: dict
    parts_total: float  # 配件总价
    labor_total: float  # 工时总价
    total_amount: float  # 总计
    parts_list: List[PartItem]
    labor_list: List[LaborItem]
    notes: str  # 备注

@router.post("/generate", response_model=QuoteResponse)
async def generate_quote(request: QuoteRequest):
    """
    生成只换不修报价单
    """
    # TODO: 实现报价逻辑
    
    # 计算配件总价
    parts_total = sum(p.price * p.quantity for p in request.parts)
    
    # 计算工时费（简化版）
    labor_items = []
    for part in request.parts:
        hours = 2.0 if part.is_safety_part else 1.5
        rate = 150.0  # 北京工时单价
        labor_items.append(LaborItem(
            operation=f"更换{part.name}",
            hours=hours,
            hourly_rate=rate,
            total=hours * rate
        ))
    
    labor_total = sum(l.total for l in labor_items)
    
    return QuoteResponse(
        quote_id=f"Q{datetime.now().strftime('%Y%m%d%H%M%S')}",
        created_at=datetime.now(),
        vehicle_info={"brand": "大众", "series": "朗逸", "year": "2020"},
        parts_total=parts_total,
        labor_total=labor_total,
        total_amount=parts_total + labor_total,
        parts_list=request.parts,
        labor_list=labor_items,
        notes="本报价基于只换不修原则生成，仅供参考。实际维修请以4S店检测为准。"
    )

@router.get("/history/{quote_id}")
async def get_quote_history(quote_id: str):
    """
    获取历史报价单
    """
    return {"quote_id": quote_id, "status": "found"}

@router.post("/{quote_id}/export")
async def export_quote(quote_id: str, format: str = "pdf"):
    """
    导出报价单（PDF/Excel）
    """
    return {"quote_id": quote_id, "format": format, "download_url": f"/downloads/{quote_id}.{format}"}

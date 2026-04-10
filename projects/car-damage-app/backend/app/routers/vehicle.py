from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class VehicleInfo(BaseModel):
    brand: str  # 品牌
    series: str  # 车系
    year: str  # 年款
    displacement: str  # 排量
    vin: Optional[str] = None  # VIN码

class VehicleResponse(BaseModel):
    id: str
    brand: str
    series: str
    year: str
    displacement: str
    body_type: str

@router.post("/identify")
async def identify_vehicle(vin: str):
    """
    通过VIN码识别车辆信息
    """
    # TODO: 实现VIN解析逻辑
    # 模拟返回
    return {
        "vin": vin,
        "brand": "大众",
        "series": "朗逸",
        "year": "2018-2024",
        "displacement": "1.4T/1.5L",
        "body_type": "紧凑型车"
    }

@router.get("/brands")
async def get_brands():
    """
    获取所有品牌列表
    """
    return {
        "brands": [
            "大众", "丰田", "本田", "日产", "别克", "宝马", "奔驰", "奥迪",
            "比亚迪", "吉利", "长安", "哈弗", "特斯拉", "小鹏", "蔚来"
        ]
    }

@router.get("/series/{brand}")
async def get_series(brand: str):
    """
    获取指定品牌的车系列表
    """
    series_map = {
        "大众": ["朗逸", "速腾", "宝来", "迈腾", "帕萨特", "途观L"],
        "丰田": ["卡罗拉", "雷凌", "凯美瑞", "RAV4", "汉兰达"],
        "本田": ["思域", "雅阁", "CR-V", "XR-V"],
        "比亚迪": ["宋PLUS", "汉EV", "海豚", "元PLUS"]
    }
    return {"brand": brand, "series": series_map.get(brand, [])}

@router.get("/parts/{brand}/{series}/{year}")
async def get_vehicle_parts(brand: str, series: str, year: str):
    """
    获取指定车型的配件列表
    """
    # TODO: 查询数据库
    return {
        "vehicle": f"{brand} {series} {year}",
        "parts_count": 150,
        "categories": ["发动机", "变速箱", "底盘", "车身", "电器", "内饰"]
    }

from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
import uuid

router = APIRouter()

# 临时文件存储目录
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

class DamageDetection(BaseModel):
    part: str  # 部位
    damage_type: str  # 损伤类型
    severity: str  # 程度：轻微/中度/严重
    confidence: float  # 置信度
    bbox: List[float]  # 边界框 [x1, y1, x2, y2]

class DamageResponse(BaseModel):
    image_id: str
    detections: List[DamageDetection]
    must_replace_parts: List[str]  # 必须更换的配件

@router.post("/detect", response_model=DamageResponse)
async def detect_damage(file: UploadFile = File(...)):
    """
    上传车损图片，AI识别损伤部位和程度
    """
    # 验证文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件")
    
    # 生成唯一ID
    image_id = str(uuid.uuid4())
    file_path = os.path.join(TEMP_DIR, f"{image_id}.jpg")
    
    # 保存上传的文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # TODO: 调用YOLOv8模型进行识别
    # 模拟识别结果
    detections = [
        DamageDetection(
            part="前保险杠",
            damage_type="破裂",
            severity="严重",
            confidence=0.95,
            bbox=[100, 200, 400, 350]
        ),
        DamageDetection(
            part="左前大灯",
            damage_type="破碎",
            severity="严重",
            confidence=0.92,
            bbox=[350, 180, 480, 280]
        )
    ]
    
    # 根据只换不修规则判断必须更换的配件
    must_replace_parts = ["前保险杠总成", "前保险杠骨架", "左前大灯总成"]
    
    return DamageResponse(
        image_id=image_id,
        detections=detections,
        must_replace_parts=must_replace_parts
    )

@router.get("/parts/{damage_id}")
async def get_related_parts(damage_id: str):
    """
    根据损伤ID获取关联配件列表
    """
    # TODO: 查询数据库获取关联配件
    return {
        "damage_id": damage_id,
        "parts": [
            {"name": "前保险杠总成", "oe_number": "18D807217", "price": 1280},
            {"name": "前保险杠骨架", "oe_number": "18D807218", "price": 580},
            {"name": "左前大灯总成", "oe_number": "18D941005", "price": 2150}
        ]
    }

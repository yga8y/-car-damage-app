# 数据库模型定义
from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Vehicle(Base):
    """车型表"""
    __tablename__ = "vehicles"
    
    id = Column(String(50), primary_key=True)
    brand = Column(String(50), nullable=False)  # 品牌
    series = Column(String(50), nullable=False)  # 车系
    year_range = Column(String(50), nullable=False)  # 年款范围
    displacement = Column(String(50))  # 排量
    transmission = Column(String(50))  # 变速箱
    body_type = Column(String(50))  # 车身结构
    vin_prefix = Column(String(20))  # VIN前缀
    vehicle_class = Column(String(50))  # 车型级别
    created_at = Column(DateTime, default=datetime.now)

class Part(Base):
    """配件表"""
    __tablename__ = "parts"
    
    id = Column(String(50), primary_key=True)
    category = Column(String(50), nullable=False)  # 配件分类
    name = Column(String(100), nullable=False)  # 配件名称
    oe_number = Column(String(50), nullable=False)  # OE编号
    spec = Column(String(100))  # 规格
    applicable_brands = Column(String(200))  # 适用品牌
    price = Column(Float, default=0)  # 参考单价
    unit = Column(String(20))  # 单位
    notes = Column(Text)  # 备注
    is_safety_part = Column(Boolean, default=False)  # 是否安全件
    created_at = Column(DateTime, default=datetime.now)

class VehiclePart(Base):
    """车型-配件关联表"""
    __tablename__ = "vehicle_parts"
    
    id = Column(String(50), primary_key=True)
    vehicle_id = Column(String(50), nullable=False)  # 车型ID
    part_id = Column(String(50), nullable=False)  # 配件ID
    install_position = Column(String(100))  # 安装位置
    factory_price = Column(Float)  # 原厂指导价
    is_safety = Column(Boolean, default=False)  # 是否安全件
    replace_rule = Column(Text)  # 只换不修规则

class DamageRule(Base):
    """损伤关联规则表"""
    __tablename__ = "damage_rules"
    
    id = Column(String(50), primary_key=True)
    main_damage = Column(String(200), nullable=False)  # 主损伤
    damage_type = Column(String(50))  # 损伤类型
    related_parts = Column(JSON)  # 关联配件列表
    rule_description = Column(Text)  # 规则说明
    priority = Column(Integer, default=1)  # 优先级

class DamageRecord(Base):
    """损伤记录表"""
    __tablename__ = "damage_records"
    
    id = Column(String(50), primary_key=True)
    image_url = Column(String(500))  # 图片URL
    vehicle_id = Column(String(50))  # 车型ID
    detections = Column(JSON)  # AI识别结果
    must_replace_parts = Column(JSON)  # 必须更换配件
    status = Column(String(20), default="pending")  # 状态
    created_at = Column(DateTime, default=datetime.now)

class Quote(Base):
    """报价单表"""
    __tablename__ = "quotes"
    
    id = Column(String(50), primary_key=True)
    damage_record_id = Column(String(50))  # 损伤记录ID
    vehicle_id = Column(String(50))  # 车型ID
    parts_total = Column(Float)  # 配件总价
    labor_total = Column(Float)  # 工时总价
    total_amount = Column(Float)  # 总计
    parts_detail = Column(JSON)  # 配件明细
    labor_detail = Column(JSON)  # 工时明细
    city = Column(String(50))  # 城市
    notes = Column(Text)  # 备注
    status = Column(String(20), default="draft")  # 状态
    created_at = Column(DateTime, default=datetime.now)

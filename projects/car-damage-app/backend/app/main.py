from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.routers import damage, vehicle, quote, damage_evaluation

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时加载模型
    print("正在加载AI模型...")
    # TODO: 加载YOLOv8模型
    print("AI模型加载完成")
    yield
    # 关闭时清理资源
    print("正在关闭服务...")

app = FastAPI(
    title="车辆定损AI API",
    description="基于AI视觉识别的车辆定损系统",
    version="1.0.0",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(damage.router, prefix="/api/v1/damage", tags=["车损识别"])
app.include_router(vehicle.router, prefix="/api/v1/vehicle", tags=["车辆信息"])
app.include_router(quote.router, prefix="/api/v1/quote", tags=["报价单"])
app.include_router(damage_evaluation.router, tags=["定损评估"])

@app.get("/")
async def root():
    return {
        "message": "车辆定损AI API服务",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

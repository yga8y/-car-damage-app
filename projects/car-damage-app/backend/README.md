# 后端API框架

## 技术栈
- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- YOLOv8 (Ultralytics)

## 项目结构
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI入口
│   ├── config.py        # 配置
│   ├── models/          # 数据库模型
│   ├── routers/         # API路由
│   ├── services/        # 业务逻辑
│   └── utils/           # 工具函数
├── requirements.txt
└── Dockerfile
```

## 安装依赖
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary ultralytics pillow python-multipart
```

## 运行
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

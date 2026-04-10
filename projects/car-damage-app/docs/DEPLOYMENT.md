# 车辆定损APP - 部署指南

## 系统要求

### 后端服务器
- OS: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+
- CPU: 4核+
- RAM: 8GB+
- 磁盘: 50GB+
- Python: 3.10+
- PostgreSQL: 14+

### AI训练服务器（可选）
- GPU: NVIDIA RTX 3060+ / Tesla T4+
- CUDA: 11.8+
- VRAM: 8GB+

### APP构建环境
- Flutter: 3.16+
- Dart: 3.0+
- Android SDK: 33+
- Xcode: 15+ (iOS)

---

## 一、后端部署

### 1. 安装依赖

```bash
# 安装Python依赖
cd backend
pip install -r requirements.txt

# 安装PostgreSQL
# Ubuntu
sudo apt-get update
sudo apt-get install postgresql-14 postgresql-contrib

# CentOS
sudo dnf install postgresql14 postgresql14-server
sudo postgresql-14-setup initdb
sudo systemctl enable postgresql-14
sudo systemctl start postgresql-14
```

### 2. 配置数据库

```bash
# 创建数据库
sudo -u postgres psql -c "CREATE DATABASE car_damage_db;"
sudo -u postgres psql -c "CREATE USER car_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE car_damage_db TO car_user;"

# 导入数据
sudo -u postgres psql -d car_damage_db -f database/schema.sql
sudo -u postgres psql -d car_damage_db -f database/vehicles_full.sql
sudo -u postgres psql -d car_damage_db -f database/parts_full.sql
sudo -u postgres psql -d car_damage_db -f database/vehicle_parts.sql
sudo -u postgres psql -d car_damage_db -f database/damage_rules.sql
```

### 3. 配置环境变量

```bash
# 创建 .env 文件
cat > backend/.env << EOF
DATABASE_URL=postgresql://car_user:your_password@localhost:5432/car_damage_db
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*
MODEL_PATH=ai-models/runs/detect/car_damage_v1/weights/best.pt
EOF
```

### 4. 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Docker部署（推荐）

```bash
# 创建Dockerfile
cat > backend/Dockerfile << 'EOF'
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# 构建镜像
docker build -t car-damage-api .

# 运行容器
docker run -d \
  --name car-damage-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://car_user:password@host:5432/car_damage_db \
  car-damage-api
```

---

## 二、AI模型部署

### 1. 安装依赖

```bash
pip install ultralytics torch torchvision
```

### 2. 训练模型

```bash
cd ai-models

# 生成训练数据（如果没有真实数据）
python generate_mock_data.py

# 开始训练
python train_model.py

# 或使用快速训练
python train_quick.py --all
```

### 3. 模型优化

```python
from ultralytics import YOLO

# 加载训练好的模型
model = YOLO('runs/detect/car_damage_v1/weights/best.pt')

# 导出为不同格式
model.export(format='onnx', imgsz=640)  # ONNX
model.export(format='tflite', imgsz=640)  # TensorFlow Lite
model.export(format='coreml', imgsz=640)  # CoreML (iOS)
```

### 3. 模型服务化

```python
# ai-models/model_server.py
from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import cv2
import numpy as np

app = FastAPI()
model = YOLO('runs/detect/car_damage_v1/weights/best.pt')

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    results = model(img)
    detections = []
    
    for box in results[0].boxes:
        detections.append({
            'class': int(box.cls),
            'confidence': float(box.conf),
            'bbox': box.xyxy.tolist()
        })
    
    return {'detections': detections}
```

---

## 三、APP部署

### 1. 配置环境

```bash
# 安装Flutter
https://docs.flutter.dev/get-started/install

# 检查环境
flutter doctor

# 获取依赖
cd frontend
flutter pub get
```

### 2. 配置API地址

```dart
// lib/config/api_config.dart
class ApiConfig {
  static const String baseUrl = 'https://your-api-server.com';
  static const String apiVersion = 'v1';
}
```

### 3. 构建Android APK

```bash
cd frontend

# 开发版
flutter build apk --debug

# 发布版
flutter build apk --release

# 输出路径: build/app/outputs/flutter-apk/app-release.apk
```

### 4. 构建iOS应用

```bash
cd frontend

# 需要在macOS上运行
flutter build ios --release

# 然后使用Xcode打包
open ios/Runner.xcworkspace
```

### 5. 发布到应用商店

#### Android (Google Play)
1. 生成签名密钥
```bash
keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-alias
```

2. 配置签名
```gradle
// android/app/build.gradle
android {
    signingConfigs {
        release {
            keyAlias 'my-alias'
            keyPassword 'password'
            storeFile file('my-release-key.jks')
            storePassword 'password'
        }
    }
}
```

3. 构建AAB格式
```bash
flutter build appbundle --release
```

#### iOS (App Store)
1. 在Apple Developer注册账号
2. 配置证书和描述文件
3. 使用Xcode Archive并上传

---

## 四、云服务部署

### 阿里云部署

```bash
# 1. 创建ECS实例
# 2. 安装Docker
# 3. 部署应用

# 使用阿里云容器服务
docker login registry.cn-hangzhou.aliyuncs.com

# 推送镜像
docker tag car-damage-api registry.cn-hangzhou.aliyuncs.com/your-namespace/car-damage-api:latest
docker push registry.cn-hangzhou.aliyuncs.com/your-namespace/car-damage-api:latest

# 部署到K8s
kubectl apply -f k8s-deployment.yaml
```

### 腾讯云部署

```bash
# 使用腾讯云Serverless
# 1. 创建云函数
# 2. 配置API网关
# 3. 部署应用
```

---

## 五、监控与维护

### 1. 日志监控

```bash
# 使用ELK Stack
# Filebeat收集日志 -> Logstash处理 -> Elasticsearch存储 -> Kibana展示

# 或使用Prometheus + Grafana
```

### 2. 性能监控

```python
# 添加性能监控中间件
from fastapi import Request
import time

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 3. 数据库备份

```bash
# 自动备份脚本
#!/bin/bash
BACKUP_DIR="/backup/postgres"
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump -U postgres car_damage_db > $BACKUP_DIR/car_damage_db_$DATE.sql

# 保留最近7天备份
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
```

---

## 六、安全加固

### 1. HTTPS配置

```nginx
# nginx配置
server {
    listen 443 ssl;
    server_name api.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. 防火墙配置

```bash
# 开放必要端口
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw enable
```

### 3. 定期更新

```bash
# 自动更新脚本
#!/bin/bash
cd /path/to/project
git pull origin main
docker-compose down
docker-compose up -d --build
```

---

## 七、故障排查

### 常见问题

1. **数据库连接失败**
   - 检查PostgreSQL服务状态
   - 验证连接字符串
   - 检查防火墙设置

2. **模型加载失败**
   - 确认模型文件路径
   - 检查文件权限
   - 验证模型格式

3. **API响应慢**
   - 检查数据库索引
   - 优化SQL查询
   - 增加缓存层

4. **APP闪退**
   - 检查Flutter版本
   - 查看设备日志
   - 验证API地址

---

## 八、联系方式

如有部署问题，请联系技术支持。

---

*文档版本: 1.0*
*更新日期: 2026-04-05*

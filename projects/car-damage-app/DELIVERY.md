# 车辆定损APP - 项目交付总结

## 项目概述

基于AI视觉识别的车辆定损手机APP，采用"只换不修"原则，用户拍照后AI自动识别车损部位和程度，生成配件报价单。

---

## 已完成交付物

### 1. 项目文档
- ✅ README.md - 项目整体说明
- ✅ PROGRESS.md - 开发进度追踪

### 2. 后端API框架 (Python + FastAPI)
```
backend/
├── app/
│   ├── main.py              # FastAPI主入口
│   ├── models/models.py     # SQLAlchemy数据库模型
│   └── routers/
│       ├── damage.py        # 车损识别API
│       ├── vehicle.py       # 车辆信息API
│       └── quote.py         # 报价单API
└── requirements.txt         # Python依赖
```

**API功能：**
- `POST /api/v1/damage/detect` - 上传图片识别车损
- `GET /api/v1/vehicle/brands` - 获取品牌列表
- `GET /api/v1/vehicle/series/{brand}` - 获取车系列表
- `POST /api/v1/quote/generate` - 生成报价单

### 3. 数据库设计 (PostgreSQL)
```
database/
├── schema.sql              # 数据库表结构
├── damage_rules.sql        # 只换不修规则(20+条)
├── vehicles.sql            # 车型数据(20款)
└── parts.sql               # 配件数据(80+件)
```

**核心表：**
- vehicles - 车型库
- parts - 配件库
- damage_rules - 损伤关联规则
- damage_records - 损伤记录
- quotes - 报价单

### 4. AI模型模块 (YOLOv8)
```
ai-models/
├── train.py                # 模型训练脚本
└── inference.py            # 模型推理脚本
```

**功能特性：**
- 支持6类损伤识别：凹陷、划痕、裂纹、掉漆、穿孔、变形
- 支持12个部位识别：保险杠、车门、大灯、后视镜、叶子板等
- 自动判断严重程度（轻微/中度/严重）
- 只换不修规则自动判定

### 5. APP前端 (Flutter)
```
frontend/
├── lib/
│   ├── main.dart
│   └── screens/
│       ├── home_screen.dart     # 首页
│       ├── camera_screen.dart   # 拍照页面
│       ├── result_screen.dart   # 识别结果
│       ├── quote_screen.dart    # 报价单
│       └── history_screen.dart  # 历史记录
└── pubspec.yaml
```

**UI功能：**
- 拍照/相册选择
- 车损识别结果展示
- 只换不修配件列表
- 报价单生成与导出
- 历史记录管理

---

## 核心技术栈

| 模块 | 技术 | 版本 |
|------|------|------|
| 后端 | Python + FastAPI | 3.10+ |
| 数据库 | PostgreSQL | 14+ |
| AI模型 | YOLOv8 (Ultralytics) | 8.1+ |
| APP | Flutter | 3.16+ |
| 部署 | Docker | - |

---

## 只换不修规则示例

### 安全件（任何损伤必须更换）
- 前挡风玻璃
- 大灯（左/右）
- 尾灯
- 气囊
- 结构件

### 严重损伤（必须更换）
- 破裂、撕裂
- 穿孔
- 严重变形（面积>60%）

### 关联更换规则示例
```
前保险杠破裂 → 前保险杠总成 + 骨架 + 卡扣 + 内衬 + 雾灯 + 雷达探头
左前大灯破碎 → 左前大灯总成 + 支架 + 前保险杠(左侧) + 水箱上横梁
```

---

## 数据资源

### 开源数据集
- **CarDD**: 4000+张高清图，6类损伤标注
  - GitHub: https://github.com/HUANG-Siran/CarDD
- **TQVCD**: 多角度车损数据集
  - GitHub: https://github.com/ULIB-SJTU/TQVCD

### 已录入车型（20款）
大众(朗逸/速腾/迈腾)、丰田(卡罗拉/凯美瑞/RAV4)、本田(思域/雅阁/CR-V)、
日产(轩逸/天籁)、别克(英朗)、宝马(3系/5系)、奔驰(C级)、奥迪(A4L)、
比亚迪(宋PLUS/汉EV)、特斯拉(Model 3/Model Y)

### 已录入配件（80+件）
保险杠、大灯、玻璃、叶子板、车门、后视镜、机盖、后备箱、水箱框架等

---

## 下一步开发计划

### Phase 1: 环境搭建（1-2天）
1. 安装Python依赖: `pip install -r backend/requirements.txt`
2. 安装PostgreSQL并导入数据库: `psql -f database/schema.sql`
3. 下载CarDD数据集并放入 datasets/CarDD/
4. 配置Flutter开发环境

### Phase 2: 模型训练（3-5天）
1. 准备训练数据
2. 运行训练: `python ai-models/train.py --train`
3. 评估模型: `python ai-models/train.py --validate best.pt`
4. 导出模型: `python ai-models/train.py --export best.pt`

### Phase 3: API开发（5-7天）
1. 启动后端服务: `uvicorn app.main:app --reload`
2. 实现图像上传和AI推理集成
3. 完善配件匹配和报价计算逻辑
4. API测试

### Phase 4: APP开发（7-10天）
1. 运行Flutter项目: `flutter run`
2. 对接后端API
3. 完善UI和交互
4. 测试和优化

### Phase 5: 部署上线（3-5天）
1. 后端Docker化部署
2. 数据库部署
3. APP打包发布

---

## 预计开发周期

- **MVP版本**: 3-4周（基础识别+20款车型+核心规则）
- **完整版本**: 2-3个月（300+车型+全部规则+API对接）

---

## 项目路径

```
C:\Users\ZhuanZ\.openclaw\workspace\projects\car-damage-app\
```

---

## 联系方式

如有问题，请联系开发负责人。

---

*交付时间: 2026-04-05*
*版本: v0.1.0*

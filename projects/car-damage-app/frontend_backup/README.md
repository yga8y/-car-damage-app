# 车辆定损APP - Flutter前端

## 项目结构
```
lib/
├── main.dart              # 入口文件
├── app.dart               # App配置
├── config/
│   └── api_config.dart    # API配置
├── models/
│   ├── damage_model.dart  # 损伤模型
│   ├── vehicle_model.dart # 车辆模型
│   └── quote_model.dart   # 报价模型
├── screens/
│   ├── home_screen.dart   # 首页
│   ├── camera_screen.dart # 拍照页面
│   ├── result_screen.dart # 识别结果页
│   ├── quote_screen.dart  # 报价单页
│   └── history_screen.dart# 历史记录
├── services/
│   ├── api_service.dart   # API服务
│   └── camera_service.dart# 相机服务
├── widgets/
│   ├── damage_card.dart   # 损伤卡片
│   ├── part_list.dart     # 配件列表
│   └── price_summary.dart # 价格汇总
└── utils/
    └── helpers.dart       # 工具函数
```

## 依赖
```yaml
dependencies:
  flutter:
    sdk: flutter
  camera: ^0.10.5+9
  image_picker: ^1.0.7
  http: ^1.2.0
  provider: ^6.1.1
  shared_preferences: ^2.2.2
  path_provider: ^2.1.2
  permission_handler: ^11.2.0
  flutter_pdfview: ^1.3.2
  share_plus: ^7.2.2
```

import 'dart:convert';
import 'package:http/http.dart' as http;

/// API配置
class ApiConfig {
  // 开发环境（本地测试）
  static const String baseUrl = 'http://10.0.2.2:8000';  // Android模拟器访问本机
  
  // 生产环境（部署后修改为您的服务器地址）
  // static const String baseUrl = 'http://your-server-ip:8000';
  
  // API端点
  static const String evaluateDamage = '/api/car/damage/evaluate';
  static const String getAccidentTypes = '/api/car/accident-types';
  static const String getPartPrice = '/api/car/parts/price';
  static const String getDamageRules = '/api/car/damage/rules';
}

/// 损伤部位模型
class DamagePart {
  final String partName;
  final String? oeCode;
  final String damageLevel;
  final String damageType;

  DamagePart({
    required this.partName,
    this.oeCode,
    required this.damageLevel,
    this.damageType = '破损',
  });

  Map<String, dynamic> toJson() => {
    'part_name': partName,
    'oe_code': oeCode,
    'damage_level': damageLevel,
    'damage_type': damageType,
  };
}

/// 定损结果配件
class PartResult {
  final String partName;
  final String? oeCode;
  final double price;
  final double laborCost;
  final String suggest;
  final String reason;
  final bool isSafetyPart;
  final String damageLevel;

  PartResult({
    required this.partName,
    this.oeCode,
    required this.price,
    required this.laborCost,
    required this.suggest,
    required this.reason,
    required this.isSafetyPart,
    required this.damageLevel,
  });

  factory PartResult.fromJson(Map<String, dynamic> json) => PartResult(
    partName: json['part_name'] ?? '',
    oeCode: json['oe_code'],
    price: (json['price'] ?? 0).toDouble(),
    laborCost: (json['labor_cost'] ?? 0).toDouble(),
    suggest: json['suggest'] ?? '',
    reason: json['reason'] ?? '',
    isSafetyPart: json['is_safety_part'] ?? false,
    damageLevel: json['damage_level'] ?? '',
  );
}

/// 定损评估结果
class DamageEvaluationResult {
  final int code;
  final String msg;
  final Map<String, dynamic> carInfo;
  final String accidentType;
  final double totalPrice;
  final double totalLabor;
  final double totalAmount;
  final int partsCount;
  final int replaceCount;
  final int safetyPartsCount;
  final List<PartResult> partsList;
  final String accidentRule;
  final String repairSuggest;

  DamageEvaluationResult({
    required this.code,
    required this.msg,
    required this.carInfo,
    required this.accidentType,
    required this.totalPrice,
    required this.totalLabor,
    required this.totalAmount,
    required this.partsCount,
    required this.replaceCount,
    required this.safetyPartsCount,
    required this.partsList,
    required this.accidentRule,
    required this.repairSuggest,
  });

  factory DamageEvaluationResult.fromJson(Map<String, dynamic> json) {
    final data = json['data'] ?? {};
    return DamageEvaluationResult(
      code: json['code'] ?? -1,
      msg: json['msg'] ?? '',
      carInfo: data['car_info'] ?? {},
      accidentType: data['accident_type'] ?? '',
      totalPrice: (data['total_price'] ?? 0).toDouble(),
      totalLabor: (data['total_labor'] ?? 0).toDouble(),
      totalAmount: (data['total_amount'] ?? 0).toDouble(),
      partsCount: data['parts_count'] ?? 0,
      replaceCount: data['replace_count'] ?? 0,
      safetyPartsCount: data['safety_parts_count'] ?? 0,
      partsList: (data['parts_list'] as List? ?? [])
          .map((e) => PartResult.fromJson(e))
          .toList(),
      accidentRule: data['accident_rule'] ?? '',
      repairSuggest: data['repair_suggest'] ?? '',
    );
  }
}

/// 定损API服务
class DamageApiService {
  static final DamageApiService _instance = DamageApiService._internal();
  factory DamageApiService() => _instance;
  DamageApiService._internal();

  final http.Client _client = http.Client();

  /// 定损评估
  Future<DamageEvaluationResult> evaluateDamage({
    required String carBrand,
    required String carSeries,
    required String carYear,
    required String accidentType,
    required List<DamagePart> damageParts,
    String city = '二线城市',
  }) async {
    try {
      final response = await _client.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.evaluateDamage}'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'car_brand': carBrand,
          'car_series': carSeries,
          'car_year': carYear,
          'accident_type': accidentType,
          'damage_parts': damageParts.map((p) => p.toJson()).toList(),
          'city': city,
        }),
      );

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body);
        return DamageEvaluationResult.fromJson(json);
      } else {
        throw Exception('API错误: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('网络请求失败: $e');
    }
  }

  /// 获取事故类型列表
  Future<List<Map<String, String>>> getAccidentTypes() async {
    try {
      final response = await _client.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.getAccidentTypes}'),
      );

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body);
        final data = json['data'] as List? ?? [];
        return data.map((e) => {
          'type': e['type']?.toString() ?? '',
          'desc': e['desc']?.toString() ?? '',
        }).toList();
      } else {
        // 返回默认类型
        return [
          {'type': '追尾', 'desc': '被后方车辆碰撞'},
          {'type': '侧撞', 'desc': '侧面被碰撞'},
          {'type': '正面碰撞', 'desc': '前方碰撞'},
          {'type': '剐蹭', 'desc': '轻微刮擦'},
        ];
      }
    } catch (e) {
      // 返回默认类型
      return [
        {'type': '追尾', 'desc': '被后方车辆碰撞'},
        {'type': '侧撞', 'desc': '侧面被碰撞'},
        {'type': '正面碰撞', 'desc': '前方碰撞'},
        {'type': '剐蹭', 'desc': '轻微刮擦'},
      ];
    }
  }

  /// 查询配件价格
  Future<Map<String, dynamic>?> getPartPrice({
    required String brand,
    required String series,
    required String partName,
  }) async {
    try {
      final response = await _client.get(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.getPartPrice}')
            .replace(queryParameters: {
          'brand': brand,
          'series': series,
          'part_name': partName,
        }),
      );

      if (response.statusCode == 200) {
        final json = jsonDecode(response.body);
        return json['data'];
      }
      return null;
    } catch (e) {
      return null;
    }
  }
}

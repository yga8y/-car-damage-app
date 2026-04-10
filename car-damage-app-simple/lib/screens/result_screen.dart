import 'dart:io';
import 'package:flutter/material.dart';
import 'quote_screen.dart';

class ResultScreen extends StatelessWidget {
  final File imageFile;

  const ResultScreen({super.key, required this.imageFile});

  // 模拟识别结果
  final List<Map<String, dynamic>> detections = [
    {
      'part': '前保险杠',
      'damage_type': '破裂',
      'severity': '严重',
      'confidence': 0.95,
      'must_replace': true,
    },
    {
      'part': '左前大灯',
      'damage_type': '破碎',
      'severity': '严重',
      'confidence': 0.92,
      'must_replace': true,
    },
  ];

  final List<Map<String, dynamic>> mustReplaceParts = [
    {'name': '前保险杠总成', 'oe_number': '18D807217', 'price': 1280},
    {'name': '前保险杠骨架', 'oe_number': '18D807218', 'price': 580},
    {'name': '左前大灯总成', 'oe_number': '18D941005', 'price': 2150},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('识别结果'),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => QuoteScreen(parts: mustReplaceParts),
                ),
              );
            },
            child: const Text('生成报价'),
          ),
        ],
      ),
      body: Column(
        children: [
          // 图片预览
          SizedBox(
            height: 200,
            child: Image.file(
              imageFile,
              fit: BoxFit.cover,
              width: double.infinity,
            ),
          ),
          // 识别结果列表
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // 损伤检测卡片
                ...detections.map((det) => _buildDetectionCard(context, det)),
                const SizedBox(height: 24),
                // 必须更换配件
                _buildReplaceSection(context),
              ],
            ),
          ),
        ],
      ),
      bottomNavigationBar: _buildBottomBar(context),
    );
  }

  Widget _buildDetectionCard(BuildContext context, Map<String, dynamic> det) {
    Color severityColor;
    switch (det['severity']) {
      case '严重':
        severityColor = Colors.red;
        break;
      case '中度':
        severityColor = Colors.orange;
        break;
      default:
        severityColor = Colors.green;
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: severityColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    det['severity'],
                    style: TextStyle(
                      color: severityColor,
                      fontWeight: FontWeight.bold,
                      fontSize: 12,
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                if (det['must_replace'])
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.red.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(4),
                    ),
                    child: const Text(
                      '必须更换',
                      style: TextStyle(
                        color: Colors.red,
                        fontWeight: FontWeight.bold,
                        fontSize: 12,
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        det['part'],
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        '损伤类型: ${det['damage_type']}',
                        style: TextStyle(
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                ),
                Text(
                  '${(det['confidence'] * 100).toStringAsFixed(1)}%',
                  style: TextStyle(
                    color: Colors.grey[600],
                    fontSize: 14,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildReplaceSection(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          '必须更换配件（只换不修）',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 12),
        ...mustReplaceParts.map((part) => ListTile(
              contentPadding: EdgeInsets.zero,
              title: Text(part['name']),
              subtitle: Text('OE号: ${part['oe_number']}'),
              trailing: Text(
                '¥${part['price']}',
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Colors.red,
                ),
              ),
            )),
        const Divider(),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              '配件小计',
              style: TextStyle(fontSize: 16),
            ),
            Text(
              '¥${mustReplaceParts.fold<int>(0, (sum, p) => sum + (p['price'] as int))}',
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildBottomBar(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(0, -5),
          ),
        ],
      ),
      child: SafeArea(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => QuoteScreen(parts: mustReplaceParts),
              ),
            );
          },
          style: ElevatedButton.styleFrom(
            minimumSize: const Size(double.infinity, 50),
          ),
          child: const Text(
            '生成完整报价单',
            style: TextStyle(fontSize: 16),
          ),
        ),
      ),
    );
  }
}

# 抖音热点监控技术调研报告

## 1. 可行技术方案分析

### 方案一：抖音开放平台API (推荐但有限制)

**优点：**
- 官方接口，数据稳定可靠
- 有完整文档支持
- 数据格式规范

**缺点：**
- 需要企业资质申请
- 需要审核，周期长
- 有调用频率限制
- 可能需要付费

**申请流程：**
1. 访问 https://open.douyin.com/
2. 注册开发者账号
3. 创建应用并申请权限
4. 等待审核通过

**相关API：**
- 视频搜索API
- 热点话题API (需要特殊权限)

---

### 方案二：网页抓取 (当前实现方式)

**优点：**
- 无需申请，立即可用
- 免费
- 数据实时性强

**缺点：**
- 需要处理反爬机制
- 页面结构变化可能导致失效
- 法律风险需注意

**目标页面：**
- 抖音网页版: https://www.douyin.com/
- 今日头条热点: https://www.toutiao.com/hot-event/hot-board/
- 第三方聚合站点

**技术要点：**
1. 模拟浏览器请求头
2. 处理JavaScript渲染内容
3. 解析JSON数据或HTML DOM
4. 设置合理的请求频率

---

### 方案三：第三方数据服务

**优点：**
- 接口稳定
- 数据已清洗整理
- 技术支持

**缺点：**
- 需要付费
- 数据可能有延迟
- 依赖第三方服务稳定性

**可能的提供商：**
- 各种数据API平台
- 社交媒体监测工具
- 舆情分析服务

---

## 2. 当前实现方案

### 实现方式

采用**网页抓取 + 模拟数据**的混合方案：

1. **优先尝试**从今日头条获取热点数据（与抖音数据互通）
2. **备选方案**从抖音网页版解析数据
3. **兜底方案**使用模拟数据展示功能

### 技术栈

- **Python 3.7+** - 主要开发语言
- **requests** - HTTP请求库
- **BeautifulSoup4** - HTML解析
- **Jinja2** - HTML模板引擎
- **json** - 数据存储

### 数据字段

```json
{
  "rank": 1,              // 排名
  "title": "热点标题",     // 话题标题
  "url": "搜索链接",       // 抖音搜索链接
  "hot_value": 1000000,   // 热度值
  "label": "热",          // 标签 (热/新/荐)
  "timestamp": "..."      // 采集时间
}
```

---

## 3. 改进建议

### 短期改进

1. **添加代理池** - 避免IP被封
2. **增加重试机制** - 提高稳定性
3. **定时任务** - 使用cron定期采集
4. **数据库存储** - 使用SQLite或MySQL存储历史数据

### 长期改进

1. **申请官方API** - 获取稳定数据源
2. **数据分析** - 热点趋势分析、预测
3. **告警功能** - 特定话题监控告警
4. **多平台整合** - 微博、知乎等热点对比

---

## 4. 使用说明

### 安装依赖

```bash
cd skills/douyin-hotspot
pip install -r requirements.txt
```

### 运行监控器

```bash
# 完整版 (带网络请求)
python douyin_hotspot.py

# 简化版 (仅模拟数据)
python douyin_hotspot_simple.py
```

### 查看结果

- JSON数据: `output/hotspots_YYYYMMDD_HHMMSS.json`
- HTML报告: `output/hotspot_report.html`
- 文本报告: `output/hotspot_report.txt`

---

## 5. 注意事项

1. **遵守法律法规** - 不要用于非法用途
2. **尊重网站规则** - 控制请求频率
3. **数据仅供参考** - 模拟数据不代表真实热点
4. **隐私保护** - 不要采集用户隐私数据

---

## 6. 参考资源

- 抖音开放平台: https://open.douyin.com/
- 抖音网页版: https://www.douyin.com/
- requests文档: https://docs.python-requests.org/
- BeautifulSoup文档: https://www.crummy.com/software/BeautifulSoup/

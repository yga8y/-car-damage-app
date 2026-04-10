/**
 * 抖音热点获取模块（无外部依赖版）
 */

const fs = require('fs');
const path = require('path');

class HotspotFetcher {
  constructor() {
    this.outputDir = path.join(__dirname, '..', 'output');
    this.cacheFile = path.join(this.outputDir, 'hotspots.json');
    
    // 确保输出目录存在
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  /**
   * 获取模拟热点数据
   */
  async fetchMockData() {
    console.log('📊 获取抖音热点数据...\n');
    
    const mockData = {
      source: 'mock-data',
      timestamp: new Date().toISOString(),
      hotspots: [
        { 
          rank: 1, 
          title: 'AI机器人会取代人类工作吗', 
          heat: 12500000, 
          category: '科技',
          tags: ['AI', '人工智能', '未来'],
          description: '讨论AI技术对就业市场的影响'
        },
        { 
          rank: 2, 
          title: '春季养生食谱推荐', 
          heat: 9800000, 
          category: '美食',
          tags: ['养生', '健康', '食谱'],
          description: '春天吃什么最养生'
        },
        { 
          rank: 3, 
          title: '职场沟通技巧大全', 
          heat: 8500000, 
          category: '职场',
          tags: ['职场', '沟通', '技巧'],
          description: '如何在职场中更好地沟通'
        },
        { 
          rank: 4, 
          title: '30天健身挑战', 
          heat: 7200000, 
          category: '健身',
          tags: ['健身', '挑战', '减肥'],
          description: '30天练出好身材'
        },
        { 
          rank: 5, 
          title: '省钱小妙招', 
          heat: 6500000, 
          category: '生活',
          tags: ['省钱', '生活', '技巧'],
          description: '日常生活中的省钱技巧'
        }
      ]
    };
    
    return mockData;
  }

  /**
   * 获取热点主函数
   */
  async fetchHotspots() {
    const data = await this.fetchMockData();
    
    // 保存到文件
    this.saveHotspots(data);
    
    // 打印热点列表
    console.log('🔥 当前抖音热点 TOP 5:\n');
    data.hotspots.forEach(h => {
      console.log(`  ${h.rank}. ${h.title}`);
      console.log(`     热度: ${h.heat.toLocaleString()} | 分类: ${h.category}`);
      console.log(`     标签: #${h.tags.join(' #')}`);
      console.log('');
    });
    
    return data;
  }

  /**
   * 保存热点数据
   */
  saveHotspots(data) {
    try {
      fs.writeFileSync(this.cacheFile, JSON.stringify(data, null, 2), 'utf8');
      console.log(`💾 热点数据已保存: ${this.cacheFile}\n`);
    } catch (error) {
      console.error('❌ 保存失败:', error.message);
    }
  }

  /**
   * 读取缓存的热点数据
   */
  loadHotspots() {
    try {
      const data = fs.readFileSync(this.cacheFile, 'utf8');
      return JSON.parse(data);
    } catch (error) {
      console.log('⚠️  没有缓存数据，请先获取热点');
      return null;
    }
  }
}

// 如果直接运行此文件
if (require.main === module) {
  const fetcher = new HotspotFetcher();
  fetcher.fetchHotspots();
}

module.exports = HotspotFetcher;

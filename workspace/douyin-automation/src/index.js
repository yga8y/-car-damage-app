/**
 * 抖音自动化主程序（无外部依赖版）
 */

const HotspotFetcher = require('./hotspot');
const VideoGenerator = require('./generate');

class DouyinAutomation {
  constructor() {
    this.fetcher = new HotspotFetcher();
    this.generator = new VideoGenerator();
  }

  /**
   * 完整工作流
   */
  async runFullWorkflow(options = {}) {
    console.log('╔════════════════════════════════════╗');
    console.log('║     抖音自动化系统 v1.0 🦞          ║');
    console.log('╚════════════════════════════════════╝\n');
    
    try {
      // 步骤1: 获取热点
      console.log('═══ 步骤1: 获取抖音热点 ═══\n');
      const hotspots = await this.fetcher.fetchHotspots();
      
      if (!hotspots || hotspots.hotspots.length === 0) {
        console.log('❌ 没有获取到热点，工作流终止');
        return;
      }
      
      // 步骤2: 生成视频脚本
      console.log('═══ 步骤2: AI生成视频脚本 ═══');
      const scripts = await this.generator.generateScriptsFromHotspots(
        hotspots, 
        options.generateLimit || 2
      );
      
      console.log('═══ 工作流完成 ═══\n');
      console.log('📋 输出文件:');
      console.log(`   - 热点数据: output/hotspots.json`);
      console.log(`   - 视频脚本: output/scripts/`);
      console.log('\n下一步:');
      console.log('   1. 查看生成的脚本');
      console.log('   2. 接入AI服务优化内容');
      console.log('   3. 安装FFmpeg生成视频');
      console.log('   4. 配置抖音账号自动发布');
      
      return {
        hotspots: hotspots,
        scripts: scripts
      };
      
    } catch (error) {
      console.error('❌ 工作流出错:', error.message);
    }
  }

  /**
   * 仅获取热点
   */
  async fetchOnly() {
    return this.fetcher.fetchHotspots();
  }

  /**
   * 从已有热点生成脚本
   */
  async generateOnly(limit = 3) {
    const hotspots = this.fetcher.loadHotspots();
    if (!hotspots) {
      console.log('❌ 没有缓存的热点数据，请先运行获取热点');
      return;
    }
    return this.generator.generateScriptsFromHotspots(hotspots, limit);
  }
}

// 命令行运行
if (require.main === module) {
  const automation = new DouyinAutomation();
  
  // 解析命令行参数
  const args = process.argv.slice(2);
  const command = args[0] || 'full';
  
  switch(command) {
    case 'full':
      automation.runFullWorkflow({ generateLimit: 2 });
      break;
      
    case 'hotspot':
      automation.fetchOnly();
      break;
      
    case 'generate':
      automation.generateOnly(3);
      break;
      
    default:
      console.log('用法: node src/index.js [full|hotspot|generate]');
      console.log('  full     - 运行完整工作流');
      console.log('  hotspot  - 仅获取热点');
      console.log('  generate - 从缓存生成脚本');
  }
}

module.exports = DouyinAutomation;

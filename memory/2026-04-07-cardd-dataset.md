# CarDD Dataset 下载工作记录

## 日期
2026-04-07

## 任务
下载 CarDD (Car Damage Detection) 数据集相关资源

## 完成情况

### ✅ 已下载完成
- **GitHub 仓库**: https://github.com/harpreetsahota204/car_dd_dataset_workshop
- **ZIP 文件位置**: `C:\Users\ZhuanZ\car_dd_dataset_workshop.zip` (54.91 MB)
- **解压位置**: `C:\Users\ZhuanZ\car_dd_dataset_extracted\car_dd_dataset_workshop-main\`

### 📁 解压后的文件清单
| 文件 | 大小 | 说明 |
|------|------|------|
| README.md | 7.9 KB | 数据集详细介绍 |
| 00_setting_up_your_enviornment.md | 2.6 KB | 环境设置指南 |
| 01_loading_and_exploring_dataset.ipynb | 37 KB | 加载和探索数据集教程 |
| 02_using_embeddings.ipynb | 26 KB | 使用嵌入教程 |
| 03_model_evaluation.ipynb | 43 KB | 模型评估教程 |
| 04_using_plugins.ipynb | 22 KB | 使用插件教程 |
| 05_using_zoo_models.ipynb | 10 KB | 使用 Zoo 模型教程 |
| 06_using_3d_models.ipynb | 10 KB | 使用 3D 模型教程 |
| cardd-overview-lq.gif | 57.4 MB | 数据集概览动画 |
| CarDD_license.pdf | 181 KB | 许可证文件 |
| LICENSE | 11.7 KB | 开源许可证 |
| requirements.txt | 158 B | Python 依赖 |
| .gitignore | 3.5 KB | Git 忽略文件 |

## 关于 CarDD 数据集

### 基本信息
- **全称**: Car Damage Detection Dataset
- **图像数量**: 4,000 张高分辨率汽车损伤图像
- **标注实例**: 超过 9,000 个
- **损伤类别**: 6 种
  1. Dent (凹陷)
  2. Scratch (划痕)
  3. Crack (裂纹)
  4. Glass shatter (玻璃破碎)
  5. Lamp broken (车灯损坏)
  6. Tire flat (轮胎漏气)

### 支持任务
- 分类 (Classification)
- 目标检测 (Object Detection)
- 实例分割 (Instance Segmentation)
- 显著性目标检测 (SOD)

### 标注格式
- **目标检测/实例分割**: COCO 格式
- **SOD**: DUTS 格式 (像素级二值掩码)

### 数据集划分
- 训练集: 70.4%
- 验证集: 20.25%
- 测试集: 9.35%

## ⚠️ 重要说明

**当前下载的仓库仅包含教程代码和文档，不包含实际的图像数据集！**

实际的图像数据集需要从官网下载：
- **官网**: https://cardd-ustc.github.io
- **要求**: 需要同意 Flickr 和 Shutterstock 的使用条款
- **用途**: 仅限非商业研究和教育用途

## 下一步计划

等待用户指示下载实际图像数据集。

## 相关脚本

下载脚本保存在工作区：
- `download_resume.py` - 支持断点续传的下载脚本

## 引用信息

```bibtex
@ARTICLE{CarDD, 
  author={Wang, Xinkuang and Li, Wenjing and Wu, Zhongcheng}, 
  journal={IEEE Transactions on Intelligent Transportation Systems}, 
  title={CarDD: A New Dataset for Vision-Based Car Damage Detection}, 
  year={2023}, 
  volume={24}, 
  number={7}, 
  pages={7202-7214}, 
  doi={10.1109/TITS.2023.3258480}
}
```

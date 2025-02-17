# 黄曲霉素知识图谱生成器 (Aflatoxin Mind Map Generator)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[English](README_EN.md) | 简体中文

一个优雅的知识图谱生成工具，专注于黄曲霉素相关知识的可视化展示。基于 FastAPI 和 Graphviz 构建，支持生成高质量的 PNG 和 PDF 格式输出。

## ✨ 功能特点

- 🎨 优雅的视觉设计
  - 多层次配色方案
  - 自适应节点大小
  - 智能文本换行

- 📊 专业的知识结构
  - 完整的知识体系
  - 清晰的层级关系
  - 准确的专业信息

- 🛠 强大的技术特性
  - RESTful API 接口
  - 高分辨率输出
  - 多格式支持 (PNG/PDF)
  - 完善的错误处理

## 🔧 系统要求

- Python 3.8+
- Graphviz
- ImageMagick

## 📦 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/aflatoxin-mindmap.git
cd aflatoxin-mindmap
```

2. 安装 Python 依赖：
```bash
pip install -r requirements.txt
```

3. 安装系统依赖：

macOS：
```bash
brew install graphviz imagemagick
```

Ubuntu：
```bash
sudo apt-get install graphviz imagemagick
```

## 🚀 快速开始

1. 启动服务器：
```bash
python mindmap_server.py
```

2. 生成知识图谱：
```bash
curl -X POST http://127.0.0.1:8081/generate_mindmap
```

## 📝 API 文档

### 健康检查
```http
GET /
```
响应：服务器状态信息

### 生成知识图谱
```http
POST /generate_mindmap
```
响应：生成的文件路径信息

## 📊 知识结构

生成的知识图谱包含以下主要部分：

- 基本特征
  - 产生条件
  - 毒性特点

- 主要危害
  - 肝脏损害
  - 免疫抑制
  - 其他影响

- 易污染食物
  - 谷物类
  - 坚果类
  - 干果类

- 预防控制
  - 储存管理
  - 加工处理
  - 质量检测

## 🎨 可视化效果

- 根节点：深蓝色 (#2E86C1)
- 主要分类：中蓝色 (#3498DB)
- 子节点：浅蓝色 (#5DADE2)
- 连接线：最浅蓝色 (#85C1E9)

## 🔧 配置选项

可以在 `mindmap_server.py` 中自定义以下配置：

- 节点样式（颜色、大小、字体）
- 图形布局（方向、间距）
- 输出质量（分辨率、压缩率）

## 📁 项目结构

```
aflatoxin-mindmap/
├── mindmap_server.py     # 主服务器代码
├── requirements.txt      # Python 依赖
├── README.md            # 项目文档（中文）
├── README_EN.md         # 项目文档（英文）
├── .gitignore           # Git 忽略配置
└── output/              # 输出目录
    ├── mindmap.png      # PNG 输出
    └── mindmap.pdf      # PDF 输出
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 作者

- 作者名字

## 🙏 致谢

- FastAPI 团队
- Graphviz 项目
- ImageMagick 团队

# 优雅的知识图谱生成器 🎨 (Elegant Mind Map Generator)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

一个基于 Python 的知识可视化工具，用于生成优雅的知识图谱。支持任意主题的知识结构化展示，提供丰富的样式自定义选项。

## 功能特点 ✨

- 支持任意主题的知识图谱生成
- 多种输出格式（PNG、PDF）
- 丰富的样式自定义选项
  - 节点颜色和形状
  - 连接线样式
  - 字体和布局
  - 方向和排列
- 优雅的视觉效果
- 自动文本换行
- 多层次节点样式

## 安装说明 🚀

### 系统依赖

- Python 3.8+
- Graphviz
- ImageMagick

在 macOS 上安装系统依赖：

```bash
brew install graphviz imagemagick
```

### Python 依赖

```bash
pip install -r requirements.txt
```

## 使用方法 📖

1. 启动服务器

```bash
uvicorn mindmap_server:app --host 0.0.0.0 --port 8081
```

2. 调用 API 生成思维导图

## API 接口 🔌

### 生成思维导图

```http
POST /generate_mindmap
```

生成自定义主题的思维导图，支持灵活的样式配置。

#### 请求示例

```json
{
  "title": "我的知识图谱",
  "content": "核心概念",
  "nodes": [
    {
      "title": "主要分类",
      "content": "分类描述",
      "children": [
        {
          "title": "子分类1",
          "content": "详细说明",
          "children": []
        }
      ]
    }
  ],
  "style": {
    "root_color": "#2E86C1",
    "main_color": "#3498DB",
    "sub_color": "#5DADE2",
    "edge_color": "#85C1E9",
    "font_family": "SimHei",
    "direction": "TB",
    "node_shape": "rect",
    "line_style": "curved"
  },
  "output_format": "both"
}
```

#### 响应示例

```json
{
  "status": "success",
  "message": "Mind map generated successfully",
  "files": {
    "png": "output/mindmap_20250217_180402.png",
    "pdf": "output/mindmap_20250217_180402.pdf"
  }
}
```

## 项目结构 📁

```
.
├── mindmap_server.py  # 主服务器实现
├── requirements.txt   # 项目依赖
├── README.md         # 说明文档
├── README_EN.md      # 英文说明文档
└── output/           # 生成的思维导图文件
```

## 许可证 📜

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献 🤝

欢迎提交 Issue 和 Pull Request！

## 样式配置说明 🎯

### 节点样式

- `root_color`: 根节点颜色
- `main_color`: 主要分类节点颜色
- `sub_color`: 子节点颜色
- `edge_color`: 连接线颜色
- `font_family`: 字体
- `direction`: 布局方向
  - `TB`: 从上到下
  - `LR`: 从左到右
  - `RL`: 从右到左
  - `BT`: 从下到上
- `node_shape`: 节点形状
  - `rect`: 矩形
  - `ellipse`: 椭圆
  - `diamond`: 菱形
  - `box`: 方框
- `line_style`: 连接线样式
  - `curved`: 曲线
  - `spline`: 样条曲线
  - `ortho`: 直角线
  - `line`: 直线

### 自定义节点样式

每个节点都可以通过 `style` 字段自定义样式：

```json
{
  "title": "自定义节点",
  "content": "说明文本",
  "style": {
    "fillcolor": "#FF0000",
    "shape": "diamond",
    "fontsize": "16"
  }
}
```

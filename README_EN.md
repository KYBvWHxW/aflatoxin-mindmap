# Elegant Mind Map Generator 🎨

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Python-based knowledge visualization tool for generating elegant mind maps. Supports knowledge structure visualization for any topic with rich style customization options.

## Features ✨

- Generate mind maps for any topic
- Multiple output formats (PNG, PDF)
- Rich style customization options
  - Node colors and shapes
  - Connection line styles
  - Fonts and layouts
  - Direction and arrangement
- Elegant visual effects
- Automatic text wrapping
- Multi-level node styling

## Installation 🚀

### System Dependencies

- Python 3.8+
- Graphviz
- ImageMagick

Install system dependencies on macOS:

```bash
brew install graphviz imagemagick
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage 📖

1. Start the server

```bash
uvicorn mindmap_server:app --host 0.0.0.0 --port 8081
```

2. Call the API to generate mind maps

## API Interface 🔌

### Generate Mind Map

```http
POST /generate_mindmap
```

Generate custom themed mind maps with flexible style configuration.

#### Request Example

```json
{
  "title": "My Knowledge Map",
  "content": "Core Concepts",
  "nodes": [
    {
      "title": "Main Category",
      "content": "Category Description",
      "children": [
        {
          "title": "Subcategory 1",
          "content": "Detailed Description",
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

#### Response Example

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

## Project Structure 📁

```
.
├── mindmap_server.py  # Main server implementation
├── requirements.txt   # Project dependencies
├── README.md         # Documentation (Chinese)
├── README_EN.md      # Documentation (English)
└── output/           # Generated mind map files
```

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing 🤝

Issues and Pull Requests are welcome!

## Style Configuration Guide 🎯

### Node Styles

- `root_color`: Root node color
- `main_color`: Main category node color
- `sub_color`: Sub-node color
- `edge_color`: Connection line color
- `font_family`: Font family
- `direction`: Layout direction
  - `TB`: Top to bottom
  - `LR`: Left to right
  - `RL`: Right to left
  - `BT`: Bottom to top
- `node_shape`: Node shape
  - `rect`: Rectangle
  - `ellipse`: Ellipse
  - `diamond`: Diamond
  - `box`: Box
- `line_style`: Connection line style
  - `curved`: Curved lines
  - `spline`: Spline curves
  - `ortho`: Orthogonal lines
  - `line`: Straight lines

### Custom Node Styles

Each node can have custom styles via the `style` field:

```json
{
  "title": "Custom Node",
  "content": "Description text",
  "style": {
    "fillcolor": "#FF0000",
    "shape": "diamond",
    "fontsize": "16"
  }
}
```

# Aflatoxin Mind Map Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[English](README_EN.md) | [简体中文](README.md)

An elegant knowledge map generator focused on visualizing aflatoxin-related information. Built with FastAPI and Graphviz, supporting high-quality PNG and PDF output formats.

## ✨ Features

- 🎨 Elegant Visual Design
  - Multi-level color scheme
  - Adaptive node sizing
  - Smart text wrapping

- 📊 Professional Knowledge Structure
  - Complete knowledge system
  - Clear hierarchical relationships
  - Accurate professional information

- 🛠 Powerful Technical Features
  - RESTful API interface
  - High-resolution output
  - Multiple format support (PNG/PDF)
  - Comprehensive error handling

## 🔧 System Requirements

- Python 3.8+
- Graphviz
- ImageMagick

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aflatoxin-mindmap.git
cd aflatoxin-mindmap
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install system dependencies:

macOS:
```bash
brew install graphviz imagemagick
```

Ubuntu:
```bash
sudo apt-get install graphviz imagemagick
```

## 🚀 Quick Start

1. Start the server:
```bash
python mindmap_server.py
```

2. Generate mind map:
```bash
curl -X POST http://127.0.0.1:8081/generate_mindmap
```

## 📝 API Documentation

### Health Check
```http
GET /
```
Response: Server status information

### Generate Mind Map
```http
POST /generate_mindmap
```
Response: Generated file path information

## 📊 Knowledge Structure

The generated mind map includes the following main sections:

- Basic Characteristics
  - Production Conditions
  - Toxicity Features

- Main Hazards
  - Liver Damage
  - Immune Suppression
  - Other Effects

- Contaminated Foods
  - Cereals
  - Nuts
  - Dried Fruits

- Prevention & Control
  - Storage Management
  - Processing
  - Quality Testing

## 🎨 Visualization

- Root Node: Deep Blue (#2E86C1)
- Main Categories: Medium Blue (#3498DB)
- Sub Nodes: Light Blue (#5DADE2)
- Connections: Lightest Blue (#85C1E9)

## 🔧 Configuration Options

The following can be customized in `mindmap_server.py`:

- Node styles (colors, sizes, fonts)
- Graph layout (direction, spacing)
- Output quality (resolution, compression)

## 📁 Project Structure

```
aflatoxin-mindmap/
├── mindmap_server.py     # Main server code
├── requirements.txt      # Python dependencies
├── README.md            # Documentation (Chinese)
├── README_EN.md         # Documentation (English)
├── .gitignore           # Git ignore configuration
└── output/              # Output directory
    ├── mindmap.png      # PNG output
    └── mindmap.pdf      # PDF output
```

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## 👥 Authors

- Author Name

## 🙏 Acknowledgments

- FastAPI Team
- Graphviz Project
- ImageMagick Team

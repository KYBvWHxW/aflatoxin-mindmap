from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
import graphviz
import json
from pathlib import Path
import os
import logging
import sys
import subprocess

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Aflatoxin Mind Map Server")

@app.get("/")
async def root():
    return PlainTextResponse("Server is running")

class MindMapNode(BaseModel):
    title: str
    content: str
    children: list = []

def create_mindmap(data: dict) -> graphviz.Digraph:
    # Create a new graph with PNG settings
    dot = graphviz.Digraph(
        comment='Aflatoxin Mind Map',
        format='png',
        engine='dot',
        encoding='utf-8'
    )
    
    # Set graph attributes for better output
    dot.attr(layout='dot')
    dot.attr(overlap='scale')
    dot.attr(splines='curved')
    dot.attr(dpi='300')
    dot.attr(bgcolor='white')
    
    # Set graph attributes
    dot.attr(rankdir='TB')  # Top to bottom layout
    dot.attr(ranksep='0.8')  # Increase vertical spacing
    dot.attr(nodesep='0.5')  # Increase horizontal spacing
    dot.attr(size='11,11')
    
    # Color scheme
    colors = {
        'root': '#4B77BE',  # 深蓝色
        'main': '#5DADE2',   # 浅蓝色
        'sub': '#85C1E9'     # 最浅蓝色
    }
    
    # Set default node attributes
    dot.attr('node', 
        shape='box',
        style='rounded,filled',
        fontname='SimSun',     # 中文字体
        fontsize='14',
        height='0.6',
        margin='0.3,0.2',
        penwidth='2')
    
    def add_nodes(node: dict, parent_id=None, level=0):
        node_id = str(abs(hash(node['title'])))
        
        # Node styling based on level
        if level == 0:
            # Root node
            color = colors['root']
            fontsize = '16'
            width = '3.0'
            height = '0.8'
            margin = '0.5,0.4'
        elif level == 1:
            # Main category nodes
            color = colors['main']
            fontsize = '14'
            width = '2.5'
            height = '0.7'
            margin = '0.4,0.3'
        else:
            # Sub nodes
            color = colors['sub']
            fontsize = '13'
            width = '2.0'
            height = '0.6'
            margin = '0.3,0.2'
        
        # Format label
        title = node['title'].strip()
        content = node['content'].strip()
        if content:
            # Split content into lines if too long
            if len(content) > 15:
                words = content.split()
                lines = []
                current_line = []
                current_length = 0
                
                for word in words:
                    if current_length + len(word) > 15:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = len(word)
                    else:
                        current_line.append(word)
                        current_length += len(word) + 1
                
                if current_line:
                    lines.append(' '.join(current_line))
                content = '\n'.join(lines)
            label = f"{title}\n{content}"
        else:
            label = title
        
        # Create node
        dot.node(node_id, label,
            fillcolor=color,
            fontcolor='white',
            fontsize=fontsize,
            width=width,
            height=height,
            margin=margin)
        
        # Create edge
        if parent_id:
            dot.edge(parent_id, node_id,
                color=colors['sub'],
                penwidth='1.2',
                arrowsize='0.6',
                arrowhead='normal')
        
        # Process children
        for child in node.get('children', []):
            add_nodes(child, node_id, level + 1)
    
    add_nodes(data)
    return dot

def check_dependencies():
    """Check if required system dependencies are installed"""
    try:
        # Check Graphviz
        import shutil
        if not shutil.which('dot'):
            raise RuntimeError("Graphviz is not installed. Please install it first.")
        
        # Check ImageMagick
        if not shutil.which('convert'):
            raise RuntimeError("ImageMagick is not installed. Please install it first.")
            
        logger.info("All system dependencies are available")
        return True
    except Exception as e:
        logger.error(f"Dependency check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"System dependency check failed: {str(e)}"
        )

@app.post("/generate_mindmap")
async def generate_mindmap():
    logger.info("Received request to generate mind map")
    
    # Check dependencies first
    check_dependencies()
    
    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Define the mind map structure
    mindmap_data = {
        "title": "黄曲霉素",
        "content": "真菌毒素",
        "children": [
            {
                "title": "基本特征",
                "content": "由黄曲霉菌产生的致癌毒素",
                "children": [
                    {"title": "产生条件", "content": "潮湿高温环境", "children": []},
                    {"title": "毒性特点", "content": "强致癌性和蓄积性", "children": []}
                ]
            },
            {
                "title": "主要危害",
                "content": "多系统损害",
                "children": [
                    {"title": "肝脏损害", "content": "可致肝癌，肝硬化", "children": []},
                    {"title": "免疫抑制", "content": "降低机体抵抗力", "children": []},
                    {"title": "其他影响", "content": "神经系统和肾脏损害", "children": []}
                ]
            },
            {
                "title": "易污染食物",
                "content": "多种农产品",
                "children": [
                    {"title": "谷物类", "content": "玉米、大米、小麦", "children": []},
                    {"title": "坚果类", "content": "花生、核桃、杏仁", "children": []},
                    {"title": "干果类", "content": "葡萄干、枣干", "children": []}
                ]
            },
            {
                "title": "预防控制",
                "content": "全程防控",
                "children": [
                    {"title": "储存管理", "content": "控制温湿度，保持通风", "children": []},
                    {"title": "加工处理", "content": "筛选分级，及时晾晒", "children": []},
                    {"title": "质量检测", "content": "定期抽检，严格把关", "children": []}
                ]
            }
        ]
    }
    
    try:
        logger.info("Creating mind map...")
        dot = create_mindmap(mindmap_data)
        
        # Save PNG version
        output_path = output_dir / "mindmap"
        logger.info(f"Rendering PNG to {output_path}.png")
        try:
            dot.render(str(output_path), cleanup=True)
        except Exception as e:
            logger.error(f"Failed to generate PNG: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate PNG: {str(e)}"
            )
        
        # Convert PNG to PDF using ImageMagick
        png_path = output_path.with_suffix(".png")
        pdf_path = output_path.with_suffix(".pdf")
        
        if not png_path.exists():
            error_msg = "PNG file was not generated"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
        logger.info("Converting PNG to PDF using ImageMagick")
        try:
            result = subprocess.run(
                [
                    'convert',
                    '-density', '300',  # High resolution
                    '-quality', '100',  # Best quality
                    str(png_path),
                    '-compress', 'lzw',  # Better compression
                    str(pdf_path)
                ],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"ImageMagick conversion failed: {e.stderr}")
            raise HTTPException(
                status_code=500,
                detail=f"PDF conversion failed: {e.stderr}"
            )
        
        if not pdf_path.exists():
            error_msg = "PDF file was not generated"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        
        logger.info("Files generated successfully")
        return JSONResponse(content={
            "status": "success",
            "message": "Mind map generated successfully",
            "files": {
                "png": str(png_path),
                "pdf": str(pdf_path)
            }
        })
            
    except Exception as e:
        error_msg = f"Error generating mind map: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    # Configure CORS and other settings
    uvicorn.run(
        "mindmap_server:app",
        host="127.0.0.1",
        port=8081,
        reload=True,
        log_level="info",
        access_log=True
    )

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import graphviz
import json
from pathlib import Path
import os
import logging
import sys
import subprocess
from datetime import datetime

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Elegant Mind Map Generator")

class MindMapNode(BaseModel):
    title: str
    content: str = ""
    children: List["MindMapNode"] = []
    style: Optional[dict] = Field(default_factory=dict)

class MindMapStyle(BaseModel):
    root_color: str = "#2E86C1"  # 深蓝色
    main_color: str = "#3498DB"  # 中蓝色
    sub_color: str = "#5DADE2"   # 浅蓝色
    edge_color: str = "#85C1E9"  # 最浅蓝色
    font_family: str = "SimHei"  # 字体
    direction: str = "TB"        # 布局方向 (TB, LR, RL, BT)
    node_shape: str = "rect"     # 节点形状
    line_style: str = "curved"   # 线条样式

class MindMapRequest(BaseModel):
    title: str
    content: str = ""
    nodes: List[MindMapNode]
    style: Optional[MindMapStyle] = None
    output_format: str = "both"  # "png", "pdf", or "both"

def add_node(dot: graphviz.Digraph, node: MindMapNode, parent_id: str = None, level: int = 0, style: MindMapStyle = None) -> None:
    """Add a node and its children to the graph with custom styling"""
    # Create unique node ID
    node_id = f"node_{id(node)}"
    
    # Get node color based on level and custom style
    if level == 0:
        color = style.root_color
    elif level == 1:
        color = style.main_color
    else:
        color = style.sub_color
    
    # Create node label with title and content
    label = f"{node.title}"
    if node.content:
        label += f"\\n{node.content}"
    
    # Merge default styling with custom node style
    node_style = {
        'shape': style.node_shape,
        'style': 'filled,rounded',
        'fillcolor': color,
        'fontname': style.font_family,
        'fontsize': '14',
        'height': '0.6',
        'width': '2.0',
        'penwidth': '2.0',
        'color': color
    }
    
    # Override with custom node style if provided
    if node.style:
        node_style.update(node.style)
    
    # Add node with styling
    dot.node(
        node_id,
        label=label,
        **node_style
    )
    
    # Connect to parent if exists
    if parent_id:
        dot.edge(
            parent_id,
            node_id,
            color=style.edge_color,
            penwidth='2.0'
        )
    
    # Add children recursively
    for child in node.children:
        add_node(dot, child, node_id, level + 1, style)

def create_mindmap(request: MindMapRequest) -> graphviz.Digraph:
    """Create a mind map based on the request"""
    # Get style settings
    style = request.style or MindMapStyle()
    
    # Create a new graph
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dot = graphviz.Digraph(
        comment=f'Mind Map - {request.title}',
        format='png',
        engine='dot',
        encoding='utf-8'
    )
    
    # Set graph attributes
    dot.attr(
        layout='dot',
        overlap='scale',
        splines=style.line_style,
        dpi='300',
        bgcolor='white',
        rankdir=style.direction,
        ranksep='0.8',
        nodesep='0.5',
        size='11,11'
    )
    
    # Add root node
    root = MindMapNode(title=request.title, content=request.content)
    add_node(dot, root, style=style)
    
    # Add main nodes
    for node in request.nodes:
        add_node(dot, node, f"node_{id(root)}", level=1, style=style)
    
    return dot

def check_dependencies():
    """Check if required system dependencies are installed"""
    try:
        # Check Graphviz
        result = subprocess.run(['dot', '-V'], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("Graphviz is not installed")
        logger.info("Graphviz check passed")
        
        # Check ImageMagick
        result = subprocess.run(['convert', '-version'], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception("ImageMagick is not installed")
        logger.info("ImageMagick check passed")
        
    except FileNotFoundError as e:
        logger.error(f"Dependency check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"System dependency check failed: {str(e)}"
        )

# Add CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Mind Map Generator is running"}

@app.post("/generate_mindmap")
async def generate_mindmap(request: MindMapRequest):
    """Generate a mind map based on the request"""
    logger.info(f"Received request to generate mind map: {request.title}")
    
    # Check dependencies
    check_dependencies()
    
    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Create mind map
        logger.info("Creating mind map...")
        dot = create_mindmap(request)
        
        # Generate unique filenames with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"mindmap_{timestamp}"
        output_path = output_dir / base_filename
        
        # Generate PNG
        png_path = None
        if request.output_format in ["png", "both"]:
            logger.info(f"Rendering PNG to {output_path}.png")
            try:
                dot.render(str(output_path), cleanup=True)
                png_path = output_path.with_suffix(".png")
            except Exception as e:
                logger.error(f"Failed to generate PNG: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to generate PNG: {str(e)}"
                )
        
        # Generate PDF if requested
        pdf_path = None
        if request.output_format in ["pdf", "both"]:
            if not png_path or not png_path.exists():
                error_msg = "PNG file is required for PDF conversion"
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=error_msg)
            
            pdf_path = output_path.with_suffix(".pdf")
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
        
        # Prepare response
        response = {
            "status": "success",
            "message": "Mind map generated successfully",
            "files": {}
        }
        
        if png_path and png_path.exists():
            response["files"]["png"] = str(png_path)
        if pdf_path and pdf_path.exists():
            response["files"]["pdf"] = str(pdf_path)
        
        logger.info("Files generated successfully")
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate mind map: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "mindmap_server:app",
        host="0.0.0.0",
        port=8081,
        reload=True
    )

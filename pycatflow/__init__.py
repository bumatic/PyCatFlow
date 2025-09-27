"""
PyCatFlow: A Python package for visualizing categorical data over time.

PyCatFlow creates temporal flow diagrams that show how categorical data evolves,
appears, and disappears over time periods. The package provides a complete
toolkit for loading data, processing it, and generating publication-ready
visualizations with extensive customization options.

Key Components:
    - Data Loading: read_file() and read() functions for CSV and structured data
    - Visualization: visualize() function for creating flow diagrams
    - Export: SVG and PNG output capabilities with professional styling

Basic Usage:
    >>> import pycatflow as pcf
    >>> data = pcf.read_file("data.csv", columns="year", nodes="category")
    >>> viz = pcf.visualize(data, spacing=30, width=800)
    >>> viz.save_svg("output.svg")

Features:
    - Multiple connection styles (semi-curved, curved, straight)
    - Automatic and custom color schemes
    - Flexible data input formats
    - Professional labeling and legends
    - High-quality export options

Version: 0.2.0 (drawSVG 2.x compatible)
Authors: Marcus Burkhardt, Herbert Natta
License: MIT
"""

from .input import read_file, read, find_delimiter, detect_dtype, prepare_data
from .viz import visualize, nodify, genSVG, Node

__version__ = "0.2.0"
__author__ = "Marcus Burkhardt"
__email__ = "marcus.burkhardt@gmail.com"
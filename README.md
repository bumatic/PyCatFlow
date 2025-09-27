[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5531785.svg)](https://doi.org/10.5281/zenodo.5531785)

# PyCatFlow

A Python package for visualizing categorical data over time using temporal flow diagrams.

## Overview

PyCatFlow is a specialized visualization tool designed to represent temporal developments in categorical data. It creates flow diagrams that show how categories evolve, appear, and disappear over time periods, making it ideal for analyzing trends in datasets with temporal and categorical dimensions.

### Key Features

- **Temporal Flow Visualization**: Create dynamic flow diagrams showing category changes over time
- **Multiple Connection Types**: Choose from semi-curved, curved, or straight connection styles
- **Data Input**: Support for CSV files
- **Customizable Appearance**: Extensive options for colors, spacing, labels, and legends
- **Export Capabilities**: Generate high-quality SVG and PNG outputs
- **Professional Output**: Publication-ready visualizations with comprehensive styling options

## Installation

### PyPI Installation

```bash
pip install pycatflow
```

### Development Installation

```bash
git clone https://github.com/bumatic/PyCatFlow.git
cd PyCatFlow
pip install -r requirements-dev.txt
pip install -e .
```

**Alternative using extras:**
```bash
pip install -e ".[dev]"
```

### System Dependencies

PyCatFlow requires Cairo for PNG export functionality. Install Cairo using your system's package manager:

**macOS (using Homebrew):**
```bash
brew install cairo
```

**Ubuntu/Debian:**
```bash
sudo apt-get install libcairo2-dev
```

**Windows:**
Follow the instructions at [cairographics.org](https://www.cairographics.org/download/)

**Additional Python Dependencies:**
For PNG export functionality, install:
```bash
pip install cairosvg
```

## Quick Start

### Basic Usage

```python
import pycatflow as pcf

# Load and parse data
data = pcf.read_file(
    "data.csv",
    columns="time_period",
    nodes="category",
    categories="subcategory"
)

# Create visualization
viz = pcf.visualize(
    data,
    spacing=20,
    width=800,
    connection_type="semi-curved"
)

# Export results
viz.save_svg('output.svg')
viz.save_png('output.png')

# Display in Jupyter
viz
```

### Data Format Requirements

Your CSV data should contain at minimum:
- **Time periods**: Column indicating different time points
- **Categories**: Column with categorical data to track over time
- **Subcategories** (optional): Additional categorical dimension for color coding

Example data structure:
```csv
time_period,category,subcategory
2020,LibraryA,Core
2020,LibraryB,Optional
2021,LibraryA,Core
2021,LibraryC,New
```

## Advanced Configuration

### Visualization Parameters

```python
viz = pcf.visualize(
    data,
    # Layout
    spacing=50,              # Space between time periods
    width=1200,              # Canvas width (auto if None)
    height=800,              # Canvas height (auto if None)

    # Node appearance
    node_size=10,            # Base node size
    minValue=1,              # Minimum node size
    maxValue=20,             # Maximum node size
    node_scaling="linear",   # Scaling method

    # Connections
    connection_type="semi-curved",  # "semi-curved", "curved", "straight"
    line_opacity=0.5,        # Connection transparency

    # Colors
    color_categories=True,   # Color by subcategory
    color_startEnd=True,     # Highlight start/end nodes
    palette=("viridis", 10), # Matplotlib colormap

    # Labels
    show_labels=True,        # Display node labels
    label_text="item",       # "item", "item_count", "item_category"
    label_position="nodes",  # "nodes", "start_end"

    # Legend
    legend=True,             # Include legend

    # Sorting
    sort_by="frequency"      # "frequency", "alphabetical", "category"
)
```

### Data Loading Options

```python
# File loading with custom parameters
data = pcf.read_file(
    "data.csv",
    columns="time_col",      # Time period column
    nodes="category_col",    # Category column
    categories="subcat_col", # Subcategory column (optional)
    orientation="horizontal", # Data layout
    delimiter=",",           # Custom delimiter
    column_order="order_col" # Column for custom time ordering
)

# Direct string parsing
data = pcf.read(
    csv_string,
    columns="time_col",
    nodes="category_col"
)
```

## Examples

### Example 1: Software Dependencies Over Time

```python
import pycatflow as pcf

# Load dependency data
data = pcf.read_file(
    "dependencies.csv",
    columns="year",
    nodes="library",
    categories="type"
)

# Create professional visualization
viz = pcf.visualize(
    data,
    spacing=30,
    width=1000,
    connection_type="curved",
    color_categories=True,
    label_text="item_count",
    legend=True
)

viz.save_svg('dependencies_flow.svg')
```

### Example 2: Custom Styling

```python
# Create visualization with custom colors
viz = pcf.visualize(
    data,
    palette=("Set3", 12),
    nodes_color="#f0f0f0",
    start_node_color="#2e8b57",
    end_node_color="#dc143c",
    line_opacity=0.7,
    label_color="#333333"
)
```

## API Reference

### Core Functions

#### `read_file(filepath, **kwargs)`
Load and parse data from CSV file.

**Parameters:**
- `filepath` (str): Path to CSV file
- `columns` (str): Column name containing time periods
- `nodes` (str): Column name containing categories to track
- `categories` (str, optional): Column name for subcategories
- `orientation` (str): "horizontal" or "vertical" data layout
- `delimiter` (str, optional): CSV delimiter (auto-detected if None)

**Returns:**
- `dict`: Structured data ready for visualization

#### `visualize(data, **kwargs)`
Generate flow visualization from structured data.

**Parameters:**
- `data` (dict): Output from `read_file()` or `read()`
- `spacing` (int): Space between time periods (default: 50)
- `connection_type` (str): "semi-curved", "curved", or "straight"
- `color_categories` (bool): Enable category-based coloring
- `legend` (bool): Include legend in output

**Returns:**
- `drawsvg.Drawing`: SVG visualization object

### Visualization Methods

The returned visualization object supports:
- `save_svg(filename)`: Export as SVG
- `save_png(filename)`: Export as PNG (requires cairosvg)
- Display in Jupyter notebooks directly

## Data Format Specifications

### Horizontal Format (Recommended)
Time periods in one column, categories in another:
```csv
time_period,category,subcategory
2020,ItemA,TypeX
2020,ItemB,TypeY
2021,ItemA,TypeX
2021,ItemC,TypeZ
```

### Vertical Format
Time periods as column headers:
```csv
category,2020,2021,2022
ItemA,TypeX,TypeX,
ItemB,TypeY,,TypeY
ItemC,,TypeZ,TypeZ
```

## Changelog

### Version 0.2.0 (2024)
**Major Update: drawSVG 2.x Migration**

#### Breaking Changes
- **Updated drawSVG dependency**: Now requires `drawsvg>=2.0` (previously `drawSVG<2.0`)
- **API method names**: Updated to snake_case following drawSVG 2.x conventions
  - `viz.saveSvg()` → `viz.save_svg()`
  - `viz.savePng()` → `viz.save_png()`
- **Package name**: Import statement unchanged (`import drawsvg`), but package name is now lowercase

#### Migration Notes
Users upgrading from version 0.1.x should:
1. Update method calls: `save_svg()` and `save_png()` instead of camelCase versions
2. Install updated dependencies: `pip install drawsvg>=2.0 cairosvg`
3. Existing visualization outputs will be functionally identical with minor coordinate improvements

### Version 0.1.x (2021-2023)
- Initial release with drawSVG 1.x support
- Core visualization functionality
- Basic CSV data loading
- SVG and PNG export capabilities
- Multiple connection types and styling options

## Development and Contributing

### Setting Up Development Environment

```bash
git clone https://github.com/bumatic/PyCatFlow.git
cd PyCatFlow
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

### Running Tests

```bash
# Using pytest (recommended)
python -m pytest tests/ -v

# With coverage report
python -m pytest tests/ --cov=pycatflow --cov-report=html

```

### Code Style

The project follows Python best practices:
- PEP 8 style guidelines
- Comprehensive docstrings
- Type hints where appropriate
- Professional error handling

## Troubleshooting

### Common Issues

**PNG Export Not Working**
```bash
pip install cairosvg
```

**Import Errors**
Ensure all dependencies are installed:
```bash
pip install drawsvg>=2.0 matplotlib cairosvg
```

**Data Loading Issues**
- Verify CSV format matches expected structure
- Check column names match those specified in parameters
- Ensure file encoding is UTF-8

### Performance Considerations

- Large datasets (>1000 categories) may require increased spacing
- Complex connection types (curved) take longer to render
- PNG export is slower than SVG due to rasterization

## Related Resources

- **Tutorial Article**: [Medium article](https://medium.com/@bumatic/pycatflow-visualizing-categorical-data-over-time-b344102bcce2) with detailed explanation
- **Interactive Tutorial**: [Jupyter Notebook](https://mybinder.org/v2/gist/bumatic/83c3423595cde010da7ad059c6b8b2f5/HEAD) with widgets
- **Example Data**: Sample datasets available in the `example/` directory

## Citation

If you use PyCatFlow in your research, please cite:

Marcus Burkhardt, and Herbert Natta. 2021. "PyCatFlow: A Python Package for Visualizing Categorical Data over Time". Zenodo. https://doi.org/10.5281/zenodo.5531785.

## License

PyCatFlow is released under the MIT License. See LICENSE file for details.

## Credits

**Conceptualization**: Marcus Burkhardt
**Implementation**: Marcus Burkhardt and Herbert Natta ([@herbertmn](https://github.com/herbertmn))
**Inspiration**: Rankflow visualization tool by Bernhard Rieder

---

For questions, issues, or contributions, please visit the [GitHub repository](https://github.com/bumatic/PyCatFlow).
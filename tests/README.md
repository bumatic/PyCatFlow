# PyCatFlow Test Suite

This directory contains comprehensive unit and integration tests for PyCatFlow's drawSVG 2.x migration.

## Test Structure

### `test_visualization.py` - Core Visualization Tests
Tests for the main visualization functionality:

- **Basic visualization creation** - Tests that visualizations can be created with default parameters
- **drawSVG 2.x API compatibility** - Verifies `save_svg()` and `save_png()` methods work correctly
- **Connection types** - Tests all three connection types: `semi-curved`, `curved`, `straight`
- **Visual customization** - Tests color options, sizing, labels, legend functionality
- **Coordinate system consistency** - Verifies the coordinate system migration from drawSVG 1.x to 2.x
- **Header positioning** - Tests that column headers are properly centered above nodes
- **Node label positioning** - Tests node label alignment and positioning
- **SVG structure validity** - Verifies generated SVG has proper XML structure
- **Data processing** - Tests the `nodify()` function and `Node` class

### `test_integration.py` - End-to-End Integration Tests
Tests for complete workflows:

- **Full CSV-to-SVG workflow** - Tests complete data loading, visualization, and export pipeline
- **Connection types integration** - Tests all connection types with real data
- **Custom styling integration** - Tests complex styling combinations
- **Large dataset performance** - Tests performance with larger datasets (100+ items)
- **Special characters handling** - Tests Unicode and special character support
- **PNG export integration** - Tests PNG export functionality (requires CairoSVG)

## Running Tests

### Run All Tests
```bash
cd /path/to/PyCatFlow
python -m unittest discover tests -v
```

### Run Specific Test Files
```bash
# Core visualization tests
python -m unittest tests.test_visualization -v

# Integration tests
python -m unittest tests.test_integration -v
```

### Run Individual Test Methods
```bash
# Test a specific functionality
python -m unittest tests.test_visualization.TestVisualization.test_connection_types -v
```

## Test Coverage

The test suite covers:

✅ **Core Functionality**
- Basic visualization creation
- All connection types (semi-curved, curved, straight)
- Data loading and processing
- Node creation and positioning

✅ **drawSVG 2.x Migration**
- API method name changes (`save_svg()`, `save_png()`)
- Coordinate system transformation
- Y-axis positioning correctness
- Header centering with `text-anchor="middle"`

✅ **Visual Options**
- Color customization (`color_categories`, `color_startEnd`, custom colors)
- Sizing options (`minValue`, `maxValue`, `node_size`, `spacing`)
- Label options (`show_labels`, `label_position`, `label_text`, `label_color`)
- Legend functionality
- Sorting options (`frequency`, `alphabetical`, `category`)

✅ **Edge Cases**
- Minimal datasets (2 columns, few items)
- Large datasets (5+ columns, 20+ items each)
- Special characters and Unicode
- Performance with complex visualizations

✅ **File I/O**
- SVG export functionality
- PNG export (with CairoSVG dependency)
- CSV data loading
- Temporary file handling

## Dependencies

### Required
- Python 3.6+
- drawsvg >= 2.0
- CairoSVG ~=2.3
- matplotlib
- pycatflow


### Optional (for full test coverage)
- CairoSVG (for PNG export tests)
- pytest (alternative test runner)

## Test Data

Tests use both synthetic and realistic data:

- **Synthetic data**: Simple test cases for unit testing
- **CSV data**: Realistic package dependency data mimicking the ChatterBot requirements
- **Large datasets**: Generated data for performance testing
- **Special characters**: Unicode and symbol testing

## Known Test Warnings

- **MatplotlibDeprecationWarning**: The tests may show warnings about `cm.get_cmap()` being deprecated. This is a matplotlib deprecation and doesn't affect functionality.

## Expected Results

All tests should pass with:
```
Ran 19 tests in ~0.1s
OK
```

If any tests fail, check:
1. drawSVG version is 2.x (`pip show drawsvg`)
2. All dependencies are installed
3. Python version is 3.6+
4. File permissions for temporary file creation

## Adding New Tests

When adding new functionality to PyCatFlow:

1. **Add unit tests** in `test_visualization.py` for individual components
2. **Add integration tests** in `test_integration.py` for end-to-end workflows
3. **Test edge cases** - minimal data, large data, special characters
4. **Test visual output** - verify SVG contains expected elements
5. **Test coordinate consistency** - ensure positioning is correct

### Test Naming Convention
- `test_[functionality]` - for unit tests
- `test_[workflow]_integration` - for integration tests
- Use descriptive docstrings explaining what is being tested
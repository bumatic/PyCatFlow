import unittest
import os
import sys
import tempfile
import xml.etree.ElementTree as ET

# Add parent directory to path to import pycatflow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import pycatflow as pcf


class TestVisualization(unittest.TestCase):
    """Test suite for PyCatFlow visualization functionality with drawSVG 2.x"""

    def setUp(self):
        """Set up test data for all tests"""
        # Sample data mimicking the ChatterBot requirements structure
        self.sample_data = {
            '2015-09-08': {
                'pymongo': (10, 'A_Requirements'),
                'requests': (5, 'A_Requirements'),
                'nltk': (8, 'A_Requirements')
            },
            '2016-09-08': {
                'pymongo': (8, 'A_Requirements'),
                'requests': (4, 'A_Requirements'),
                'nltk': (9, 'A_Requirements'),
                'sqlalchemy': (7, 'A_Requirements')
            },
            '2017-09-08': {
                'pymongo': (6, 'A_Requirements'),
                'nltk': (10, 'A_Requirements'),
                'sqlalchemy': (8, 'A_Requirements'),
                'pytest': (5, 'B_Developers_Requirements')
            }
        }

        # Minimal data for edge case testing
        self.minimal_data = {
            '2020-01': {'item1': (5, 'cat1')},
            '2020-02': {'item1': (3, 'cat1'), 'item2': (2, 'cat2')}
        }

        # Large data for stress testing
        self.large_data = {}
        for i in range(5):
            col_name = f'2020-0{i+1}'
            self.large_data[col_name] = {}
            for j in range(15):
                item_name = f'item_{j:02d}'
                category = 'cat_A' if j % 2 == 0 else 'cat_B'
                self.large_data[col_name][item_name] = (20 - j, category)

    def test_basic_visualization_creation(self):
        """Test basic visualization creation with default parameters"""
        viz = pcf.visualize(self.sample_data)

        # Check that it returns a drawsvg Drawing object
        self.assertIsNotNone(viz)
        self.assertEqual(type(viz).__name__, 'Drawing')

        # Check basic attributes
        self.assertGreater(viz.width, 0)
        self.assertGreater(viz.height, 0)

    def test_drawsvg_2x_api_methods(self):
        """Test that drawSVG 2.x API methods work correctly"""
        viz = pcf.visualize(self.sample_data, spacing=20, width=400)

        # Test save_svg method (new snake_case API)
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            try:
                viz.save_svg(tmp.name)
                # Verify file was created and has content
                self.assertTrue(os.path.exists(tmp.name))
                self.assertGreater(os.path.getsize(tmp.name), 100)

                # Parse SVG and verify basic structure
                tree = ET.parse(tmp.name)
                root = tree.getroot()
                self.assertEqual(root.tag.split('}')[-1], 'svg')

            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

    def test_connection_types(self):
        """Test all three connection types: semi-curved, curved, straight"""
        connection_types = ['semi-curved', 'curved', 'straight']

        for conn_type in connection_types:
            with self.subTest(connection_type=conn_type):
                viz = pcf.visualize(
                    self.sample_data,
                    connection_type=conn_type,
                    spacing=20,
                    width=400
                )

                # Verify visualization was created
                self.assertIsNotNone(viz)
                self.assertGreater(viz.width, 0)
                self.assertGreater(viz.height, 0)

                # Save and verify SVG contains path elements
                with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
                    try:
                        viz.save_svg(tmp.name)
                        with open(tmp.name, 'r') as f:
                            svg_content = f.read()
                            # Should contain path elements for connections
                            self.assertIn('<path', svg_content)

                    finally:
                        if os.path.exists(tmp.name):
                            os.unlink(tmp.name)

    def test_visual_customization_options(self):
        """Test visual customization parameters"""
        # Test color options
        viz_colors = pcf.visualize(
            self.sample_data,
            color_startEnd=False,
            color_categories=False,
            nodes_color='blue',
            spacing=20,
            width=400
        )
        self.assertIsNotNone(viz_colors)

        # Test sizing options
        viz_sizing = pcf.visualize(
            self.sample_data,
            minValue=2,
            maxValue=15,
            node_size=8,
            spacing=30,
            width=500,
            height=300
        )
        self.assertIsNotNone(viz_sizing)
        self.assertEqual(viz_sizing.width, 500)
        self.assertEqual(viz_sizing.height, 300)

        # Test label options
        viz_labels = pcf.visualize(
            self.sample_data,
            show_labels=True,
            label_text='item_count',
            label_position='start_end',
            label_color='red',
            label_size=6,
            spacing=20,
            width=400
        )
        self.assertIsNotNone(viz_labels)

    def test_legend_functionality(self):
        """Test legend creation and positioning"""
        # Test with legend enabled
        viz_with_legend = pcf.visualize(
            self.sample_data,
            legend=True,
            spacing=20,
            width=400
        )

        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            try:
                viz_with_legend.save_svg(tmp.name)
                with open(tmp.name, 'r') as f:
                    svg_content = f.read()
                    # Should contain legend text
                    self.assertIn('Legend', svg_content)
                    self.assertIn('A_Requirements', svg_content)

            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

        # Test with legend disabled
        viz_no_legend = pcf.visualize(
            self.sample_data,
            legend=False,
            spacing=20,
            width=400
        )
        self.assertIsNotNone(viz_no_legend)

    def test_sorting_options(self):
        """Test different sorting options"""
        sort_options = ['frequency', 'alphabetical', 'category']

        for sort_by in sort_options:
            with self.subTest(sort_by=sort_by):
                viz = pcf.visualize(
                    self.sample_data,
                    sort_by=sort_by,
                    spacing=20,
                    width=400
                )
                self.assertIsNotNone(viz)
                self.assertGreater(viz.width, 0)

    def test_coordinate_system_consistency(self):
        """Test that coordinate system works correctly after drawSVG 2.x migration"""
        viz = pcf.visualize(self.sample_data, spacing=20, width=400)

        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            try:
                viz.save_svg(tmp.name)

                # Parse SVG and check coordinate consistency
                tree = ET.parse(tmp.name)
                root = tree.getroot()

                # Find rectangles (nodes) and verify Y coordinates increase downward
                rectangles = root.findall('.//{http://www.w3.org/2000/svg}rect')
                node_rects = [r for r in rectangles if r.get('fill') and r.get('fill') != 'white']

                if len(node_rects) >= 2:
                    y_coords = [float(r.get('y', 0)) for r in node_rects[:5]]  # Check first 5
                    # Y coordinates should generally increase for subsequent nodes
                    self.assertTrue(any(y_coords[i] <= y_coords[i+1] for i in range(len(y_coords)-1)))

                # Find text elements (headers) and verify they're positioned at top
                text_elements = root.findall('.//{http://www.w3.org/2000/svg}text')
                header_texts = [t for t in text_elements if '2015' in t.text or '2016' in t.text or '2017' in t.text]

                if header_texts:
                    header_y = float(header_texts[0].get('y', 0))
                    # Headers should be near the top (low Y value)
                    self.assertLess(header_y, 50)

            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Test with minimal data
        viz_minimal = pcf.visualize(self.minimal_data, spacing=20, width=200)
        self.assertIsNotNone(viz_minimal)

        # Test with large data
        viz_large = pcf.visualize(self.large_data, spacing=15, width=600)
        self.assertIsNotNone(viz_large)
        self.assertEqual(viz_large.width, 600)

        # Test with custom palette
        viz_palette = pcf.visualize(
            self.sample_data,
            palette=('viridis', 5),
            spacing=20,
            width=400
        )
        self.assertIsNotNone(viz_palette)

    def test_header_positioning(self):
        """Test that column headers are properly centered above nodes"""
        viz = pcf.visualize(self.sample_data, spacing=20, width=400)

        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            try:
                viz.save_svg(tmp.name)
                with open(tmp.name, 'r') as f:
                    svg_content = f.read()

                    # Should contain headers with text-anchor="middle"
                    self.assertIn('text-anchor="middle"', svg_content)
                    self.assertIn('2015-09-08', svg_content)
                    self.assertIn('2016-09-08', svg_content)
                    self.assertIn('2017-09-08', svg_content)

            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

    def test_node_label_positioning(self):
        """Test that node labels are properly positioned"""
        viz = pcf.visualize(
            self.sample_data,
            show_labels=True,
            label_position='nodes',
            spacing=20,
            width=400
        )

        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            try:
                viz.save_svg(tmp.name)

                # Parse and verify label elements exist
                tree = ET.parse(tmp.name)
                root = tree.getroot()
                text_elements = root.findall('.//{http://www.w3.org/2000/svg}text')

                # Should have labels for items
                label_texts = [t.text for t in text_elements if t.text and t.text not in ['Legend', 'A_Requirements']]
                self.assertIn('pymongo', label_texts)
                self.assertIn('nltk', label_texts)

            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

    def test_svg_structure_validity(self):
        """Test that generated SVG has proper structure"""
        viz = pcf.visualize(self.sample_data, spacing=20, width=400)

        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            try:
                viz.save_svg(tmp.name)

                # Parse as XML to verify structure
                tree = ET.parse(tmp.name)
                root = tree.getroot()

                # Should be valid SVG
                self.assertTrue(root.tag.endswith('svg'))
                self.assertIsNotNone(root.get('width'))
                self.assertIsNotNone(root.get('height'))

                # Should contain defs, rect, text, and path elements
                defs = root.find('.//{http://www.w3.org/2000/svg}defs')
                self.assertIsNotNone(defs)

                rects = root.findall('.//{http://www.w3.org/2000/svg}rect')
                self.assertGreater(len(rects), 0)

                texts = root.findall('.//{http://www.w3.org/2000/svg}text')
                self.assertGreater(len(texts), 0)

            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)


class TestDataProcessing(unittest.TestCase):
    """Test suite for data processing functions"""

    def setUp(self):
        self.test_data = {
            '2020-01': {
                'item_a': (10, 'cat1'),
                'item_b': (5, 'cat2'),
                'item_c': (8, 'cat1')
            },
            '2020-02': {
                'item_a': (12, 'cat1'),
                'item_b': (3, 'cat2'),
                'item_d': (6, 'cat3')
            }
        }

    def test_nodify_function(self):
        """Test the nodify function with different sorting options"""
        # Test frequency sorting
        result_freq = pcf.nodify(self.test_data, sort_by='frequency')
        self.assertEqual(len(result_freq), 3)  # [headers, nodes, sequence]
        self.assertIsInstance(result_freq[0], list)  # headers
        self.assertIsInstance(result_freq[1], list)  # nodes
        self.assertIsInstance(result_freq[2], dict)  # sequence

        # Test alphabetical sorting
        result_alpha = pcf.nodify(self.test_data, sort_by='alphabetical')
        self.assertEqual(len(result_alpha), 3)

        # Test category sorting
        result_cat = pcf.nodify(self.test_data, sort_by='category')
        self.assertEqual(len(result_cat), 3)

    def test_node_class(self):
        """Test the Node class creation"""
        from pycatflow.viz import Node

        node = Node(
            index=0,
            col_index=1,
            x=10,
            y=20,
            size=5,
            value=15,
            width=8,
            label='test_item',
            category='test_cat'
        )

        self.assertEqual(node.index, 0)
        self.assertEqual(node.col_index, 1)
        self.assertEqual(node.x, 10)
        self.assertEqual(node.y, 20)
        self.assertEqual(node.size, 5)
        self.assertEqual(node.value, 15)
        self.assertEqual(node.width, 8)
        self.assertEqual(node.label, 'test_item')
        self.assertEqual(node.category, 'test_cat')


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
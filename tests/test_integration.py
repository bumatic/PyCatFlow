import unittest
import os
import sys
import tempfile
import csv

# Add parent directory to path to import pycatflow
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import pycatflow as pcf


class TestIntegration(unittest.TestCase):
    """Integration tests for PyCatFlow end-to-end functionality"""

    def setUp(self):
        """Set up test CSV files and data"""
        # Create a temporary CSV file for testing
        self.temp_csv = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        csv_content = [
            ['column', 'items', 'category', 'column order'],
            ['2020-01', 'numpy', 'libraries', '1'],
            ['2020-01', 'pandas', 'libraries', '1'],
            ['2020-01', 'matplotlib', 'visualization', '1'],
            ['2020-02', 'numpy', 'libraries', '2'],
            ['2020-02', 'scipy', 'libraries', '2'],
            ['2020-02', 'matplotlib', 'visualization', '2'],
            ['2020-02', 'seaborn', 'visualization', '2'],
            ['2020-03', 'numpy', 'libraries', '3'],
            ['2020-03', 'scipy', 'libraries', '3'],
            ['2020-03', 'plotly', 'visualization', '3']
        ]

        writer = csv.writer(self.temp_csv)
        writer.writerows(csv_content)
        self.temp_csv.close()

    def tearDown(self):
        """Clean up temporary files"""
        if os.path.exists(self.temp_csv.name):
            os.unlink(self.temp_csv.name)

    def test_full_workflow_csv_to_svg(self):
        """Test complete workflow: CSV → data loading → visualization → SVG export"""
        # Step 1: Load data from CSV
        data = pcf.read_file(
            self.temp_csv.name,
            columns='column',
            nodes='items',
            categories='category',
            column_order='column order'
        )

        # Verify data was loaded correctly
        self.assertIsInstance(data, dict)
        self.assertIn('2020-01', data)
        self.assertIn('2020-02', data)
        self.assertIn('2020-03', data)

        # Step 2: Create visualization
        viz = pcf.visualize(
            data,
            spacing=20,
            width=600,
            connection_type='semi-curved',
            show_labels=True,
            legend=True
        )

        # Verify visualization object
        self.assertIsNotNone(viz)
        self.assertEqual(viz.width, 600)

        # Step 3: Export to SVG
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as output_svg:
            try:
                viz.save_svg(output_svg.name)

                # Verify SVG file was created and has content
                self.assertTrue(os.path.exists(output_svg.name))
                self.assertGreater(os.path.getsize(output_svg.name), 1000)

                # Verify SVG contains expected elements
                with open(output_svg.name, 'r') as f:
                    svg_content = f.read()
                    self.assertIn('<svg', svg_content)
                    self.assertIn('numpy', svg_content)
                    self.assertIn('pandas', svg_content)
                    self.assertIn('matplotlib', svg_content)
                    self.assertIn('Legend', svg_content)

            finally:
                if os.path.exists(output_svg.name):
                    os.unlink(output_svg.name)

    def test_different_connection_types_integration(self):
        """Test integration with all connection types"""
        data = pcf.read_file(
            self.temp_csv.name,
            columns='column',
            nodes='items',
            categories='category'
        )

        connection_types = ['semi-curved', 'curved', 'straight']

        for conn_type in connection_types:
            with self.subTest(connection_type=conn_type):
                viz = pcf.visualize(
                    data,
                    connection_type=conn_type,
                    spacing=15,
                    width=400,
                    show_labels=True
                )

                with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
                    try:
                        viz.save_svg(tmp.name)

                        # Verify file was created
                        self.assertTrue(os.path.exists(tmp.name))

                        # Verify it contains path elements (connections)
                        with open(tmp.name, 'r') as f:
                            content = f.read()
                            self.assertIn('<path', content)

                    finally:
                        if os.path.exists(tmp.name):
                            os.unlink(tmp.name)

    def test_custom_styling_integration(self):
        """Test integration with custom styling options"""
        data = pcf.read_file(
            self.temp_csv.name,
            columns='column',
            nodes='items',
            categories='category'
        )

        # Test with custom colors and styling
        viz = pcf.visualize(
            data,
            spacing=25,
            width=500,
            height=400,
            minValue=3,
            maxValue=12,
            connection_type='curved',
            color_startEnd=True,
            color_categories=True,
            nodes_color='navy',
            start_node_color='green',
            end_node_color='red',
            show_labels=True,
            label_color='darkblue',
            label_size=6,
            label_position='nodes',
            line_opacity=0.7,
            line_stroke_color='gray',
            legend=True,
            sort_by='alphabetical'
        )

        self.assertIsNotNone(viz)
        self.assertEqual(viz.width, 500)
        self.assertEqual(viz.height, 400)

        # Export and verify
        with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as tmp:
            try:
                viz.save_svg(tmp.name)
                self.assertTrue(os.path.exists(tmp.name))

                with open(tmp.name, 'r') as f:
                    content = f.read()
                    # Should contain expected styling
                    # Note: when color_categories=True, category colors override nodes_color
                    self.assertIn('opacity="0.7"', content)
                    self.assertIn('stroke="gray"', content)
                    self.assertIn('fill="darkblue"', content)  # label_color

            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)

    def test_large_dataset_performance(self):
        """Test performance with larger datasets"""
        # Create larger CSV data
        large_csv = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)

        try:
            writer = csv.writer(large_csv)
            writer.writerow(['column', 'items', 'category', 'column order'])

            # Generate 5 columns with 20 items each
            for col in range(1, 6):
                for item in range(1, 21):
                    category = 'cat_A' if item % 3 == 0 else 'cat_B' if item % 3 == 1 else 'cat_C'
                    writer.writerow([f'2020-{col:02d}', f'item_{item:02d}', category, str(col)])

            large_csv.close()

            # Load and visualize
            data = pcf.read_file(
                large_csv.name,
                columns='column',
                nodes='items',
                categories='category',
                column_order='column order'
            )

            viz = pcf.visualize(
                data,
                spacing=10,
                width=800,
                connection_type='semi-curved',
                show_labels=False,  # Disable labels for performance
                legend=True
            )

            self.assertIsNotNone(viz)
            self.assertEqual(viz.width, 800)

            # Verify can export large visualization
            with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as output:
                try:
                    viz.save_svg(output.name)
                    self.assertTrue(os.path.exists(output.name))
                    # Large file should be substantial
                    self.assertGreater(os.path.getsize(output.name), 5000)

                finally:
                    if os.path.exists(output.name):
                        os.unlink(output.name)

        finally:
            if os.path.exists(large_csv.name):
                os.unlink(large_csv.name)

    def test_special_characters_handling(self):
        """Test handling of special characters in data"""
        # Create CSV with special characters
        special_csv = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8')

        try:
            special_content = [
                ['column', 'items', 'category'],
                ['2020-01', 'library-with-dashes', 'tools'],
                ['2020-01', 'library_with_underscores', 'tools'],
                ['2020-01', 'library.with.dots', 'tools'],
                ['2020-01', 'library with spaces', 'tools'],
                ['2020-01', 'library@symbol', 'tools'],
                ['2020-01', 'libraryñç', 'tools'],  # Unicode
                ['2020-02', 'library-with-dashes', 'tools'],
                ['2020-02', 'new-library', 'tools']
            ]

            writer = csv.writer(special_csv)
            writer.writerows(special_content)
            special_csv.close()

            # Load and visualize
            data = pcf.read_file(
                special_csv.name,
                columns='column',
                nodes='items',
                categories='category'
            )

            viz = pcf.visualize(
                data,
                spacing=20,
                width=400,
                show_labels=True,
                legend=True
            )

            self.assertIsNotNone(viz)

            # Export and verify special characters are preserved
            with tempfile.NamedTemporaryFile(suffix='.svg', delete=False) as output:
                try:
                    viz.save_svg(output.name)

                    with open(output.name, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.assertIn('library-with-dashes', content)
                        self.assertIn('library_with_underscores', content)
                        self.assertIn('library with spaces', content)
                        self.assertIn('libraryñç', content)

                finally:
                    if os.path.exists(output.name):
                        os.unlink(output.name)

        finally:
            if os.path.exists(special_csv.name):
                os.unlink(special_csv.name)

    def test_png_export_integration(self):
        """Test PNG export functionality if CairoSVG is available"""
        data = pcf.read_file(
            self.temp_csv.name,
            columns='column',
            nodes='items',
            categories='category'
        )

        viz = pcf.visualize(
            data,
            spacing=20,
            width=400,
            show_labels=True,
            legend=True
        )

        # Try PNG export (will skip if CairoSVG not available)
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as png_file:
                viz.save_png(png_file.name)

                if os.path.exists(png_file.name) and os.path.getsize(png_file.name) > 0:
                    # PNG export succeeded
                    self.assertTrue(os.path.exists(png_file.name))
                    self.assertGreater(os.path.getsize(png_file.name), 1000)
                    os.unlink(png_file.name)
                else:
                    # PNG export failed (CairoSVG not available)
                    self.skipTest("PNG export requires CairoSVG")

        except Exception as e:
            if "cairosvg" in str(e).lower():
                self.skipTest("PNG export requires CairoSVG")
            else:
                raise


if __name__ == '__main__':
    unittest.main(verbosity=2)
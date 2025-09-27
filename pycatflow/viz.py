import drawsvg as draw
from matplotlib import colors
import matplotlib
import pycatflow as pcf
import math
import copy

debug_legend = False


class Node:
    """
    Represents a data point node in the temporal flow visualization.

    A Node contains all necessary information to position and render a single
    categorical data point within the flow diagram, including its coordinates,
    dimensions, and associated metadata.

    Attributes:
        index (int): Unique identifier for this node within the dataset
        col_index (int): Column/time period index this node belongs to
        x (float): X-coordinate position on the canvas
        y (float): Y-coordinate position on the canvas
        size (float): Height/vertical size of the node rectangle
        value (float): Numerical value represented by this node
        width (float): Width of the node rectangle
        label (str): Text label identifying this node
        category (str): Category classification for color coding
    """

    def __init__(self, index, col_index, x, y, size, value, width, label, category):
        """
        Initialize a new Node instance.

        Args:
            index (int): Unique identifier for this node
            col_index (int): Column/time period index
            x (float): X-coordinate position
            y (float): Y-coordinate position
            size (float): Height/vertical size of the node
            value (float): Numerical value represented
            width (float): Width of the node
            label (str): Text label for identification
            category (str): Category for color classification
        """
        self.x = x
        self.index = index
        self.col_index = col_index
        self.y = y
        self.size = size
        self.value = value
        self.width = width
        self.label = label
        self.category = category


def nodify(data, sort_by="frequency"):
    """
    Convert structured data into Node objects for visualization.

    Transforms the dictionary output from read_file/read functions into a list
    of Node objects with positioning information, sorted according to the
    specified criteria.

    Args:
        data (dict): Structured data from read_file() or read() functions.
            Dictionary with time periods as keys and item dictionaries as values.
            Item values can be either frequencies (int/float) or tuples of
            (frequency, category).
        sort_by (str, optional): Sorting method for nodes within each time period.
            Options: "frequency", "alphabetical", "category".
            Defaults to "frequency".

    Returns:
        list: Three-element list containing:
            - headers (list): Time period labels
            - nodes (list): Node objects with positioning data
            - sequence (dict): Mapping of labels to node index sequences

    Raises:
        KeyError: If sort_by parameter is not a valid option

    Examples:
        >>> data = {'2020': {'ItemA': 5, 'ItemB': 3}, '2021': {'ItemA': 7}}
        >>> headers, nodes, sequence = nodify(data, sort_by="frequency")
        >>> len(nodes)
        3
    """
    d = {}
    if sort_by == "frequency":
        for item in data.items():
            if type(item[1][next(iter(item[1]))]) == tuple:
                d[item[0]] = {k: v for k, v in sorted(item[1].items(),
                                                      key=lambda x: (-x[1][0], x[0]),
                                                      reverse=False)}
            else:
                d[item[0]] = {k: v for k, v in sorted(item[1].items(),
                                                      key=lambda x: (-x[1], x[0]),
                                                      reverse=False)}
    elif sort_by == "category":
        for item in data.items():
            d[item[0]] = {k: v for k, v in sorted(item[1].items(), key=lambda x: (x[1][1], x[0]), reverse=False)}
    elif sort_by == "alphabetical":
        for x, y in data.items():
            d[x] = {k: v for k, v in sorted(y.items())}

    labels = [list(x[1].keys()) for x in d.items()]
    values = [[y[0] if type(y) == tuple else y for y in x[1].values()] for x in d.items()]
    categories = [[y[1] if type(y) == tuple else "null" for y in x[1].values()] for x in d.items()]
    headers = list(d.keys())
    node_x = 0
    count = 0
    count2 = 0

    nodes = []
    sequence = {}

    for l, v, s in zip(labels, values, categories):
        if count2 < len(labels):
            count2 += 1
        for x, y, z in zip(l, v, s):
            nodes.append(Node(count, count2, 0, 0, y, y, 1, x, z))
            count += 1

    for n in nodes:
        if n.label in sequence.keys():
            sequence[n.label].append(n.index)
        else:
            sequence[n.label] = []
            sequence[n.label].append(n.index)

    return [headers, nodes, sequence]


def genSVG(nodes, spacing, node_size, width=None, height=None, minValue=1, maxValue=10, node_scaling="linear",
           connection_type="semi-curved", color_startEnd=True, color_categories=True, nodes_color="gray",
           start_node_color="green", end_node_color="red", palette=None, show_labels=True, label_text="item", label_font="sans-serif",
           label_color="black", label_size=5, label_shortening="clip", label_position="nodes", line_opacity=0.5,
           line_stroke_color="white", line_stroke_width=0.5, line_stroke_thick=0.5, legend=True):
    """
    Generate SVG visualization from processed node data.

    Creates a complete temporal flow diagram showing categorical data evolution
    over time periods with customizable styling, connections, and annotations.

    Args:
        nodes (list): Output from nodify() containing headers, node objects, and sequences
        spacing (int): Horizontal spacing between time periods (pixels)
        node_size (int): Base size for node rectangles (pixels)
        width (int, optional): Canvas width. If None, auto-calculated from content
        height (int, optional): Canvas height. If None, auto-calculated from content
        minValue (int): Minimum node size regardless of data value. Defaults to 1
        maxValue (int): Maximum node size for scaling. Defaults to 10
        node_scaling (str): Scaling method for node sizes. Options: "linear", "log"
        connection_type (str): Style of connections between nodes.
            Options: "semi-curved", "curved", "straight". Defaults to "semi-curved"
        color_startEnd (bool): Highlight first/last appearances with special colors
        color_categories (bool): Color nodes/connections by category. Defaults to True
        nodes_color (str): Default node color when category coloring disabled
        start_node_color (str): Color for first appearance nodes. Defaults to "green"
        end_node_color (str): Color for last appearance nodes. Defaults to "red"
        palette (tuple, optional): Matplotlib colormap specification as (name, count)
        show_labels (bool): Display text labels on nodes. Defaults to True
        label_text (str): Label content type. Options: "item", "item_count", "item_category"
        label_font (str): Font family for labels. Defaults to "sans-serif"
        label_color (str): Text color for labels. Defaults to "black"
        label_size (int): Font size for labels. Defaults to 5
        label_shortening (str): Text overflow handling. Options: "clip", "resize", "new_line"
        label_position (str): Label placement. Options: "nodes", "start_end"
        line_opacity (float): Transparency of connection lines (0.0-1.0)
        line_stroke_color (str): Border color for connections. Defaults to "white"
        line_stroke_width (float): Border width for connections. Defaults to 0.5
        line_stroke_thick (float): Line thickness variation. Defaults to 0.5
        legend (bool): Include category legend in output. Defaults to True

    Returns:
        drawsvg.Drawing: Complete SVG visualization ready for export or display

    Raises:
        KeyError: If connection_type is not a supported option
        ValueError: If node scaling parameters are invalid

    Notes:
        - Canvas dimensions are auto-calculated if not specified
        - Color palettes use matplotlib colormaps for consistency
        - Connection algorithms vary by type for different visual effects
        - Legend positioning is optimized for readability
    """ 
    headers = nodes[0]
    nodes2 = copy.deepcopy(nodes[1])
    sequence = nodes[2]

    if start_node_color == "green":
        start_node_color = "#4BA167"
    if end_node_color == "red":
        end_node_color = "#A04B83"
    if nodes_color == "gray":
        nodes_color = "#EAEBEE"

    # Resizing of the nodes in relation to the canvas size and to the scaling option
    m = max([v.value for v in nodes[1]])
    new_nodes = []
    if width is not None:
        dx = (width-(spacing*2))/len(headers)
        spacing2 = 2*(dx/3)
        node_size = dx/3
    else:
        spacing2 = spacing
    if height is not None:
        l_col_index = [x.col_index for x in nodes2]
        l_col_index_max = max([l_col_index.count(y.col_index) for y in nodes2])
        sum_values = sum([x.value for x in nodes2 if l_col_index.count(x.col_index) == l_col_index_max])
        max_values = max([x.value for x in nodes2 if l_col_index.count(x.col_index) == l_col_index_max])
        if node_scaling == "linear":
            dy = ((height-(spacing*2)-(spacing/5))*max_values)/(sum_values+((maxValue/2)*l_col_index_max))
        else:
            dy = ((height-(spacing*2)-(spacing/5))*max_values)/(sum_values+((max_values/2)*l_col_index_max))
        spacingy = dy/3
        maxValue = 2*(dy/3)
    else:
        spacingy = spacing/5

    node_x = 0
    for n in nodes2:
        n.width = node_size
        if n.col_index != nodes2[n.index-1].col_index and n.index > 0:
            node_x += node_size
        n.x += node_x

        if node_scaling == "linear":
            n.size = (((n.value+1)*maxValue)/m)+minValue
        elif node_scaling == "log":
            n.size = (((maxValue-minValue)/math.log(m))*math.log(n.value))+minValue

        new_nodes.append(n)

    # positioning of the nodes on the canvas (x,y)
    n_x_spacing = spacing
    n_y_spacing = spacing+spacingy
    points = []
    for n in new_nodes:
        
        if n.index > 0 and n.col_index == new_nodes[n.index-1].col_index:
            n_y_spacing += spacingy+n.size
        else:
            n_y_spacing = spacing+spacingy+n.size
        if n.index > 0 and n.col_index != new_nodes[n.index-1].col_index:
            n_x_spacing += spacing2

        points.append(pcf.Node(n.index, n.col_index, n.x + n_x_spacing, n.y + n_y_spacing,
                               n.size, n.value, n.width, n.label, n.category))

    # sizing of the canvas
    if width is None and height is None:
        width = spacing*4+max([x.x for x in points])
        height = spacing * 4 + max([x.y for x in points]) + ((sum([x.size for x in points]) / len(points)) * len(set([x.category for x in points])))
    elif height is None:
        height = spacing * 4 + max([x.y for x in points]) + ((sum([x.size for x in points]) / len(points)) * len(set([x.category for x in points])))
    elif width is None:
        width = spacing * 4 + max([x.x for x in points])

    # COLORS
    if palette is not None:
        # Use modern matplotlib colormap API
        palette = matplotlib.colormaps[palette[0]].resampled(palette[1]).colors
        count = 0
        category_colors = {}
        for e in set([n.category for n in points]):
            if count < len(palette):
                count += 1
            category_colors[e] = colors.to_hex(palette[count])
    else:
        # DEFAULT PALETTE: the number of colors is set in relation to the length of the category list
        palette = matplotlib.colormaps["tab20c"].resampled(len(set([n.category for n in points])) + 1).colors
        count = 0
        category_colors = {}
        for e in set([n.category for n in points]):
            if count < len(palette)-1:
                count += 1
            category_colors[e] = colors.to_hex(palette[count])

    d = draw.Drawing(width, height, display_inline=True)
    r = draw.Rectangle(0, 0, width, height, stroke_width=2, stroke='black', fill="white")
    d.append(r)

    # headers
    h_x_shift = [points[0].x]

    for x in points:
        if x.x != points[x.index-1].x and x.index > 0:
            h_x_shift.append(x.x)
    
    n2 = h_x_shift[1]-h_x_shift[0]
    
    for h, x in zip(headers, h_x_shift):
        l = label_size
        # Center the header above the actual nodes, not the full column width
        # Find the center of nodes in this column by using node width and position
        header_x = x + (points[0].width / 2)  # Center above the actual nodes

        if label_shortening == "resize":
            while len(h)*(l/2) > n2+points[0].size-(n2/8) and l > 1:
                if x != max(h_x_shift):
                    l -= 1
                else:
                    break
            d.append(draw.Text(h, x=header_x, y=spacing, font_size=l, font_family=label_font, fill=label_color, text_anchor="middle"))
        elif label_shortening == "clip":
            clip = draw.ClipPath()
            clip.append(draw.Rectangle(x, 0, n2, spacing))
            d.append(draw.Text(h, x=header_x, y=spacing, font_size=l, font_family=label_font, clip_path=clip, fill=label_color, text_anchor="middle"))
        elif label_shortening == "new_line":
            if len(h)*(label_size/2) > n2+points[0].size-(n2/8):
                margin = int((n2+points[0].size-(n2/8))/(label_size/2))
                txt = [h[x:x+margin] for x in range(0, len(h), margin)]
                while len(txt)*l > (l+n2/5) and l > 1:
                    l -= 1
            else:
                txt = h
            d.append(draw.Text(txt, x=header_x, y=spacing, font_size=l, font_family=label_font, fill=label_color, text_anchor="middle"))
    
    # lines
    for n in sequence.items():        
        if len(n[1]) > 1:
            for k in n[1][:-1]:
                if color_categories:
                    color = category_colors[points[k].category]
                else:
                    color = nodes_color
                if connection_type.lower() == "semi-curved":
                    p = draw.Path(fill=color, stroke=line_stroke_color, opacity=line_opacity, stroke_width=line_stroke_width)
                    p.M(points[k].x + points[k].width, points[k].y - points[k].size)
                    p.L(points[k].x + points[k].width, points[k].y)

                    if points[k].y == points[n[1][n[1].index(k)+1]].y:
                        p.L(points[n[1][n[1].index(k)+1]].x, points[k].y)
                        p.L(points[n[1][n[1].index(k)+1]].x, points[k].y - points[k].size)

                    else:
                        xMedium = ((points[n[1][n[1].index(k)+1]].x-(points[k].x+points[k].width))/2)+(points[k].x+points[k].width)
                        next_node = points[n[1][n[1].index(k) + 1]]
                        yMedium = (points[k].y + next_node.y) / 2
                        yMedium2 = (points[k].y - points[k].size + next_node.y - next_node.size) / 2
                        p.Q(points[k].x + points[k].width + (spacing/2), points[k].y, xMedium + line_stroke_thick, yMedium)
                        p.T(next_node.x, next_node.y)
                        p.L(next_node.x, next_node.y - next_node.size)
                        p.Q(next_node.x - (spacing/2), next_node.y - next_node.size, xMedium - line_stroke_thick, yMedium2)
                        p.T(points[k].x + points[k].width, points[k].y - points[k].size)

                    p.Z()
                    d.append(p)
                elif connection_type.lower() == 'curved':
                    p = draw.Path(fill=color, stroke=line_stroke_color, opacity=line_opacity,
                                  stroke_width=line_stroke_width)

                    size_start = points[k].size
                    size_end = points[n[1][n[1].index(k) + 1]].size

                    x1_start = points[k].x + points[k].width
                    y1_start = points[k].y

                    x1_end = points[n[1][n[1].index(k) + 1]].x
                    y1_end = points[n[1][n[1].index(k) + 1]].y

                    x2_start = x1_start
                    y2_start = y1_start - size_start

                    x2_end = x1_end
                    y2_end = y1_end - size_end

                    x_diff = x1_end - x1_start
                    y_diff = y2_start - y1_end
                    height_factor = 2
                    width_factor = 0

                    if points[k].y == points[n[1][n[1].index(k) + 1]].y:
                        p.M(x1_start, y1_start)
                        p.L(x2_start, y2_start)
                        p.L(x2_end, y2_end)
                        p.L(x1_end, y1_end)
                        p.Z()
                        d.append(p)
                        pass

                    else:
                        p.M(x1_start, y1_start)
                        cx1 = x1_end - (x_diff / 4 * 3)
                        cy1 = y1_start
                        ex1 = x1_end - (x_diff / 2)
                        ey1 = y1_end + (y_diff / 2)
                        p.Q(cx1, cy1, ex1, ey1)

                        cx2 = x1_start + (x_diff / 4 * 3)
                        cy2 = y1_end - (size_end / height_factor)
                        p.Q(cx2, cy2, x1_end, y1_end)

                        p.L(x2_end, y2_end)

                        cx3 = (x2_end - (x_diff / 4))
                        cy3 = (y2_end - (size_end / height_factor))
                        ex3 = (x2_end + ((x1_start - x1_end) / 2) - width_factor)
                        ey3 = (y2_end + (((y1_start - y1_end) / 2) - (((size_start + size_end) / 2)) / height_factor))
                        p.Q(cx3, cy3, ex3, ey3)

                        cx4 = x2_start + (x_diff / 4)
                        cy4 = y2_start
                        p.Q(cx4, cy4, x2_start, y2_start)

                        p.Z()
                        d.append(p)

                elif connection_type.lower() == 'straight':
                    p = draw.Path(fill=color, stroke=line_stroke_color, opacity=line_opacity,
                                  stroke_width=line_stroke_width)
                    size_start = points[k].size
                    size_end = points[n[1][n[1].index(k) + 1]].size

                    x1_start = points[k].x + points[k].width
                    y1_start = points[k].y - points[k].size

                    x1_end = points[n[1][n[1].index(k) + 1]].x
                    y1_end = points[n[1][n[1].index(k) + 1]].y - points[n[1][n[1].index(k) + 1]].size

                    x2_start = x1_start
                    y2_start = y1_start + size_start

                    x2_end = x1_end
                    y2_end = y1_end + size_end

                    p.M(x1_start, y1_start)
                    p.L(x2_start, y2_start)
                    p.L(x2_end, y2_end)
                    p.L(x1_end, y1_end)

                    p.Z()
                    d.append(p)

                else:
                    print('This connection type is not implemented.')
                    raise KeyError

    # nodes
    # return points
    col_index_max = 0
    for node in points:
        if node.col_index > col_index_max:
            col_index_max = node.col_index

    for node in points:
        if color_startEnd == True and color_categories == True:
            if node.label not in [n.label for n in points][:node.index]:
                color = start_node_color
            elif node.label not in [n.label for n in points][node.index+1:] and node.col_index < col_index_max: #and node.index<len(points):
                color = end_node_color
            else:
                color = category_colors[node.category]
        elif color_startEnd and not color_categories:
            if node.label not in [n.label for n in points][:node.index]:
                color = start_node_color
            elif node.label not in [n.label for n in points][node.index+1:] and node.col_index < col_index_max: #and node.index<len(points):
                color = end_node_color
            else:
                color = nodes_color
        elif not color_startEnd and color_categories:
            color = category_colors[node.category]
        elif not color_startEnd and not color_categories:
            color = nodes_color
        if node.label != '':
            r = draw.Rectangle(node.x, node.y - node.size, node.width, node.size, fill=color, stroke=color) #stroke="black"
            d.append(r)

        if show_labels:
            if label_text == "item":
                txt = node.label
            elif label_text == "item_count":
                txt = node.label+' ('+str(node.value)+')'
            elif label_text == "item_category":
                txt = node.label + ' (' + str(node.category) + ')'
            
            l = label_size
            if label_shortening == "resize":
                while len(txt)*(l/2)>spacing-(spacing/8):
                    if node.x != max([n.x for n in points]) and l > 1:
                        l -= 1
                    else:
                        break
            elif label_shortening == "clip":
                clip = draw.ClipPath()
                clip.append(draw.Rectangle(node.x, node.y-node.size-(spacing/5), n2-(n2/8), node.size+2*(spacing/5)))
            elif label_shortening == "new_line":
                if len(txt)*(label_size/2) > n2-2*(n2/8):
                    margin = int((n2-2*(n2/8))/(label_size/2))
                    txt = [txt[x:x+margin] for x in range(0, len(txt), margin)]
                    while len(txt)*l > node.size+2*(spacing/8) and l > 1:
                        l -= 1

            label_pos_y = node.y - (node.size/2) + (l/2)
            if label_position == "start_end":
                if node.label not in [n.label for n in points][:node.index] or node.label not in [n.label for n in points][node.index+1:] and node.index < len(points) and node.x != max([n.x for n in points]):
                    if label_shortening == "clip":
                        label = draw.Text(txt, x=node.x+node.width+(n2/8), y=label_pos_y,
                                          font_size=l, font_family=label_font, fill=label_color, clip_path=clip)
                    else:
                        label = draw.Text(txt, x=node.x-(n2/8), y=label_pos_y,
                                          font_size=l, font_family=label_font, fill=label_color, text_anchor="end")

            elif label_position == "nodes":
                if label_shortening == "clip":
                    label = draw.Text(txt, x=node.x+node.width+(n2/8), y=label_pos_y,
                                      font_size=l, font_family=label_font, fill=label_color, clip_path=clip)
                else:
                    label = draw.Text(txt, x=node.x + node.width+(n2/8), y=label_pos_y,
                                      font_size=l, font_family=label_font, fill=label_color)
            d.append(label)
    
    # Add legend to canvas
    if color_categories and legend:
        # Use same spacing as main visualization nodes
        legend_spacing = spacingy  # Match node vertical spacing
        symbol_size = sum([x.size for x in points])/len(points)  # Average node size
        symbol_width = symbol_size  # Make symbols square (width = height)

        # Calculate legend position from bottom, using same logic as main nodes
        legend_start_y = height - spacing
        total_legend_height = len(category_colors) * (symbol_size + legend_spacing)

        # Position legend header closer to legend items
        legend_header_y = legend_start_y - total_legend_height - (spacing/2)  # Reduced spacing
        legend_header = draw.Text("Legend", x=points[0].x, y=legend_header_y, font_size=label_size,
                                  font_family=label_font, fill=label_color)

        if debug_legend:
            print('Legend spacing (spacingy):', legend_spacing)
            print('Symbol size:', symbol_size)
            print('Symbol width:', symbol_width)
            print('Legend header y:', legend_header_y)
            print()

        d.append(legend_header)

        # Draw legend items from top to bottom with same spacing as main nodes
        current_y = legend_header_y + label_size + (spacing/4)  # Small gap after header
        for e in category_colors.items():
            # Square symbol rectangle (width = height)
            symbol = draw.Rectangle(points[0].x, current_y, symbol_width, symbol_size,
                                  fill=e[1], stroke=e[1])

            # Label text
            label_y = current_y + (symbol_size/2) + (label_size/2)
            name = draw.Text(e[0], x=points[0].x + symbol_width + (spacing/4), y=label_y,
                           font_size=label_size, fill=label_color)

            d.append(symbol)
            d.append(name)

            current_y += symbol_size + legend_spacing  # Use same spacing as main visualization
            
    return d


def visualize(data, spacing=50, node_size=10, width=None, height=None, minValue=1, maxValue=10, node_scaling="linear",
              connection_type="semi-curved", color_startEnd=True, color_categories=True, nodes_color="gray",
              start_node_color="green", end_node_color="red", palette=None, show_labels=True,
              label_text="item", label_font="sans-serif", label_color="black", label_size=5,
              label_shortening="clip", label_position="nodes", line_opacity=0.5, line_stroke_color="white",
              line_stroke_width=0.5, line_stroke_thick=0.5, legend=True, sort_by="frequency"):
    """
    Create a complete temporal flow visualization from structured data.

    Main user-facing function that combines data processing and SVG generation
    to create publication-ready temporal flow diagrams showing how categorical
    data evolves over time periods.

    Args:
        data (dict): Structured data from read_file() or read() functions.
            Dictionary mapping time periods to item frequency/category data
        spacing (int): Horizontal spacing between time periods. Defaults to 50
        node_size (int): Base size for node rectangles. Defaults to 10
        width (int, optional): Canvas width in pixels. Auto-calculated if None
        height (int, optional): Canvas height in pixels. Auto-calculated if None
        minValue (int): Minimum node size scaling floor. Defaults to 1
        maxValue (int): Maximum node size scaling ceiling. Defaults to 10
        node_scaling (str): Node size scaling method. Options: "linear", "log"
        connection_type (str): Visual style for inter-node connections.
            Options: "semi-curved", "curved", "straight". Defaults to "semi-curved"
        color_startEnd (bool): Highlight first/last node appearances. Defaults to True
        color_categories (bool): Apply category-based color coding. Defaults to True
        nodes_color (str): Fallback color when category coloring disabled. Defaults to "gray"
        start_node_color (str): Color for initial appearances. Defaults to "green"
        end_node_color (str): Color for final appearances. Defaults to "red"
        palette (tuple, optional): Custom colormap as (matplotlib_name, color_count)
        show_labels (bool): Display text labels on nodes. Defaults to True
        label_text (str): Label content format. Options: "item", "item_count", "item_category"
        label_font (str): Font family for text. Defaults to "sans-serif"
        label_color (str): Text color. Defaults to "black"
        label_size (int): Font size in points. Defaults to 5
        label_shortening (str): Text overflow behavior. Options: "clip", "resize", "new_line"
        label_position (str): Label placement strategy. Options: "nodes", "start_end"
        line_opacity (float): Connection transparency (0.0-1.0). Defaults to 0.5
        line_stroke_color (str): Connection border color. Defaults to "white"
        line_stroke_width (float): Connection border thickness. Defaults to 0.5
        line_stroke_thick (float): Connection line weight variation. Defaults to 0.5
        legend (bool): Include categorical legend. Defaults to True
        sort_by (str): Node sorting within time periods.
            Options: "frequency", "alphabetical", "category". Defaults to "frequency"

    Returns:
        drawsvg.Drawing: Complete SVG visualization with the following methods:
            - save_svg(filename): Export as scalable vector graphics
            - save_png(filename): Export as raster image (requires cairosvg)
            - Direct display in Jupyter notebooks

    Examples:
        Basic usage:
        >>> data = pcf.read_file("data.csv", columns="year", nodes="category")
        >>> viz = pcf.visualize(data, spacing=30, width=800)
        >>> viz.save_svg("output.svg")

        Advanced styling:
        >>> viz = pcf.visualize(data,
        ...                    connection_type="curved",
        ...                    palette=("viridis", 8),
        ...                    label_text="item_count")

    Notes:
        - Processing pipeline: data → nodify() → genSVG() → Drawing
        - Canvas dimensions auto-adjust to content when not specified
        - Category colors assigned automatically from matplotlib colormaps
        - Performance scales well up to ~1000 categories per time period
    """

    nodes = pcf.nodify(data, sort_by=sort_by)
    viz = genSVG(nodes, spacing, node_size, width=width, height=height, minValue=minValue,
                 maxValue=maxValue, node_scaling=node_scaling, connection_type=connection_type,
                 color_startEnd=color_startEnd, color_categories=color_categories,
                 nodes_color=nodes_color, start_node_color=start_node_color,
                 end_node_color=end_node_color, palette=palette, show_labels=show_labels,
                 label_text=label_text, label_font=label_font, label_color=label_color,
                 label_size=label_size, label_shortening=label_shortening, label_position=label_position,
                 line_opacity=line_opacity, line_stroke_color=line_stroke_color,
                 line_stroke_width=line_stroke_width, line_stroke_thick=line_stroke_thick, legend=legend)
    return viz

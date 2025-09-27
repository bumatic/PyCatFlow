# PyCatFlow drawSVG 2.x Coordinate System Fixes

## Critical Issue Summary

The current implementation contains **17 instances** of Y-axis inversion logic (`height - y`) that must be removed for drawSVG 2.x compatibility. drawSVG 2.x uses native SVG coordinates where Y increases downward, eliminating the need for manual inversions.

## Required Code Changes

### 1. Header Positioning Fix (Lines 232, 235, 236)

**Current (WRONG):**
```python
# Line 232
d.append(draw.Text(h, x=x, y=height - spacing, font_size=l, font_family=label_font, fill=label_color))

# Line 235
clip.append(draw.Rectangle(x, height - spacing, n2, label_size))

# Line 236
d.append(draw.Text(h, x=x, y=height - spacing, font_size=l, font_family=label_font, clip_path=clip, fill=label_color))
```

**Fixed (CORRECT):**
```python
# Line 232
d.append(draw.Text(h, x=x, y=spacing, font_size=l, font_family=label_font, fill=label_color))

# Line 235
clip.append(draw.Rectangle(x, 0, n2, spacing + label_size))

# Line 236
d.append(draw.Text(h, x=x, y=spacing, font_size=l, font_family=label_font, clip_path=clip, fill=label_color))
```

### 2. Node Rectangle Positioning Fix (Line 393)

**Current (WRONG):**
```python
r = draw.Rectangle(node.x, height - node.y, node.width, node.size, fill=color, stroke=color)
```

**Fixed (CORRECT):**
```python
r = draw.Rectangle(node.x, node.y - node.size, node.width, node.size, fill=color, stroke=color)
```

### 3. Semi-Curved Connection Paths (Lines 257-272)

**Current (WRONG):**
```python
p.M(points[k].x + points[k].width, height - points[k].y)
p.L(points[k].x + points[k].width, height - points[k].y + points[k].size)

if points[k].y == points[n[1][n[1].index(k)+1]].y:
    p.L(points[n[1][n[1].index(k)+1]].x, height - points[k].y + points[k].size)
    p.L(points[n[1][n[1].index(k)+1]].x, height - points[k].y)
else:
    xMedium = ((points[n[1][n[1].index(k)+1]].x-(points[k].x+points[k].width))/2)+(points[k].x+points[k].width)
    yMedium = (((height - points[k].y + points[k].size) - (height - points[n[1][n[1].index(k) + 1]].y + points[k].size)) / 2) + (height - points[n[1][n[1].index(k) + 1]].y)
    yMedium2 = (((height - points[k].y) - (height - points[n[1][n[1].index(k) + 1]].y)) / 2) + (height - points[n[1][n[1].index(k) + 1]].y)
    p.Q(points[k].x + points[k].width + (spacing/2), height - points[k].y + points[k].size, xMedium + line_stroke_thick, yMedium + points[k].size)
    p.T(points[n[1][n[1].index(k)+1]].x, height - points[n[1][n[1].index(k) + 1]].y + points[n[1][n[1].index(k) + 1]].size)
    p.L(points[n[1][n[1].index(k)+1]].x, height - points[n[1][n[1].index(k) + 1]].y)
    p.Q(points[n[1][n[1].index(k)+1]].x - (spacing/2), height - points[n[1][n[1].index(k) + 1]].y, xMedium - line_stroke_thick, yMedium2)
    p.T(points[k].x + points[k].width, height - points[k].y)
```

**Fixed (CORRECT):**
```python
p.M(points[k].x + points[k].width, points[k].y)
p.L(points[k].x + points[k].width, points[k].y + points[k].size)

if points[k].y == points[n[1][n[1].index(k)+1]].y:
    p.L(points[n[1][n[1].index(k)+1]].x, points[k].y + points[k].size)
    p.L(points[n[1][n[1].index(k)+1]].x, points[k].y)
else:
    xMedium = ((points[n[1][n[1].index(k)+1]].x-(points[k].x+points[k].width))/2)+(points[k].x+points[k].width)
    yMedium = ((points[k].y + points[k].size) + (points[n[1][n[1].index(k) + 1]].y + points[k].size)) / 2
    yMedium2 = (points[k].y + points[n[1][n[1].index(k) + 1]].y) / 2
    p.Q(points[k].x + points[k].width + (spacing/2), points[k].y + points[k].size, xMedium + line_stroke_thick, yMedium)
    p.T(points[n[1][n[1].index(k)+1]].x, points[n[1][n[1].index(k) + 1]].y + points[n[1][n[1].index(k) + 1]].size)
    p.L(points[n[1][n[1].index(k)+1]].x, points[n[1][n[1].index(k) + 1]].y)
    p.Q(points[n[1][n[1].index(k)+1]].x - (spacing/2), points[n[1][n[1].index(k) + 1]].y, xMedium - line_stroke_thick, yMedium2)
    p.T(points[k].x + points[k].width, points[k].y)
```

### 4. Curved Connection Paths (Lines 284, 287)

**Current (WRONG):**
```python
y1_start = height - points[k].y + size_start
y1_end = height - points[n[1][n[1].index(k) + 1]].y + size_end
```

**Fixed (CORRECT):**
```python
y1_start = points[k].y + size_start
y1_end = points[n[1][n[1].index(k) + 1]].y + size_end
```

### 5. Straight Connection Paths (Lines 343, 346)

**Current (WRONG):**
```python
y1_start = height - points[k].y
y1_end = height - points[n[1][n[1].index(k) + 1]].y
```

**Fixed (CORRECT):**
```python
y1_start = points[k].y
y1_end = points[n[1][n[1].index(k) + 1]].y
```

### 6. Label Positioning Fix (Line 421)

**Current (WRONG):**
```python
label_pos_y = height - node.y + (node.size/2) - (l/2)
```

**Fixed (CORRECT):**
```python
label_pos_y = node.y + (node.size/2) + (l/2)
```

### 7. Clip Rectangle Fix (Line 413)

**Current (WRONG):**
```python
clip.append(draw.Rectangle(node.x, height-node.y-(spacing/5), n2-(n2/8), node.size+2*(spacing/5)))
```

**Fixed (CORRECT):**
```python
clip.append(draw.Rectangle(node.x, node.y-(spacing/5), n2-(n2/8), node.size+2*(spacing/5)))
```

### 8. Legend Positioning Fix

The legend positioning calculations need to be completely rewritten for bottom positioning in drawSVG 2.x coordinates:

**Current (WRONG):**
```python
legend_header_y = legend_height + symbol_size + spacing_bottom + (offset)
legend_label_y = spacing_bottom + legend_height + (symbol_size/2) - (label_size/2) - offset - symbol_y_shift
symbol_y = spacing_bottom+legend_height-offset-symbol_y_shift
```

**Fixed (CORRECT):**
```python
# Position legend at bottom of canvas
legend_start_y = height - legend_height - spacing_bottom
legend_header_y = legend_start_y - symbol_size - offset
legend_label_y = legend_start_y + (symbol_size/2) + (label_size/2) + symbol_y_shift
symbol_y = legend_start_y + symbol_y_shift
```

## Implementation Strategy

1. **Make a backup** of current `viz.py` before changes
2. **Update coordinates systematically** - one section at a time
3. **Test each section** after changes to isolate issues
4. **Use the test suite** to validate each fix
5. **Compare outputs** pixel-by-pixel with reference images

## Validation Checklist

After applying fixes, verify:

- [ ] Column headers appear at TOP of visualization
- [ ] Nodes flow from TOP to BOTTOM chronologically
- [ ] Labels are vertically CENTERED within nodes
- [ ] Legend appears at BOTTOM with proper spacing
- [ ] All connection types work correctly
- [ ] No elements appear outside canvas bounds
- [ ] Output matches reference image exactly

## Critical Notes

- In drawSVG 2.x, Y=0 is at the TOP of the canvas
- Y increases DOWNWARD (unlike mathematical coordinates)
- All `height - y` inversions must be removed
- Text baselines may need adjustment for proper centering
- Legend calculations need complete rewrite for bottom positioning

This represents a **complete coordinate system transformation** - not just simple API updates.
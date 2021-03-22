# pycatflow

<h1>pycatflow</h1>

<p>This package is a visualization tool which allows the representation of temporal developments, based on categorical data.</p>

<h6>Requirements</h6>
<p>The visualization and export stands on the **drawSvg** package; the colour palettes are from **matplotlib**</p>

<h6>Functions</h6>

**read_file(filepath,time_field=None,tag_field=None,subtag_field=None,orientation="horizontal",delimiter=None)**
* **filepath**: any textual data format (csv,txt,tsv);
* **time_field**: the name of the field with temporal data (leave None if orientation="vertical");
* **tag_field**: the name of the field with the category;
* **subtag_field**: the name of the field with the subcategory (optional);
* **orientation**: horizontal if the temporal data are in one field, vertical if the temporal data are the name of  the fields;
* **delimiter**: otpionally specify the delimiter, if None it will try to autodetect.

**read(data,time_field=None,tag_field=None,subtag_field=None,orientation="horizontal",delimiter=None,newLine=None)**
* **data**: string with records divided by newLine and fields divided by delimiter; list of lists with the first element as list of headers; dictionary with headers as keys and values as lists;
* **time_field**: the name of the field with temporal data (leave None if orientation="vertical");
* **tag_field**: the name of the field with the category;
* **subtag_field**: the name of the field with the subcategory (optional);
* **orientation**: horizontal if the temporal data are in one field, vertical if the temporal data are the name of  the fields;
* **delimiter**: otpionally specify the delimiter, if None it will try to autodetect.
* **newLine**: optionally define the newLine separator, by default \n.

**nodify(data,sort_by="frequency")**
* **data**: output of the **read_file**/**read** functions, a dictionary with keys the temporal data, and values a dictionary with keys the categories and values or the frequency of the category or a tuple with the frequency and the subtag;
* **sort_by**: frequency, subtag or alphabetical.

**genSVG(nodes,spacing,width=None,heigth=None,minValue=1,maxValue=10,node_scaling="linear",color_startEnd=True,color_subtag=True,nodes_color="gray",start_node_color="green",end_node_color="red",palette=None,show_labels=True,label_font="sans-serif",label_text="tag",label_color="black",label_size=5,label_shortening="clip",label_position="nodes",line_opacity=0.5,line_stroke_color="white",line_stroke_width=0.5,line_stroke_thick=0.5,legend=True)**
* **nodes**: output of nodify function, a list of headers, list of nodes and their sequence;
* **spacing**: the space between the nodes;
* **width** and **height**: sizes of the output image, if None they are automatically generated from the size of the nodes, if they are specified the nodes will be rescaled to fit the space;
* **minValue**: the minimum value of the height of the nodes, used as a reference to rescale the values of the frequency to set the height of the nodes;
* **maxValue**: the maximum value of the height of the nodes, used as a reference to rescale the values of the frequency to set the height of the nodes;
* **node_scaling**: linear or log (logaritmic), to set the methods for fitting the node's heigth to the min-max value range or to the selected heigth of the canvas;
* **color_startEnd**: boolean, if True it marks the colors of the first and last appearence of a category;
* **color_subtag**: boolean, if True the nodes and the lines are colored depending by the subcategory;
* **nodes_color**: the color of the nodes if the previous two options are false, used also for the lines and for the middle nodes in case of startEnd option;
* **start_node_color**: the color of the node where firstly a category appears;
* **end_node_color**: the color of the last node of a category;
* **palette**: a tuple with the name of the matplotlib palette and the number of colors ("viridis",12), if None it uses the "Paired" matplotlib palette;
* **show_labels**: boolean, it shows or hide the node's labels;
* **label_font**: the font family used for the headers, the labels and the legend;
* **label_color**: the color of the headers, the labels and the legend;
* **label_text**: "tag" shows the category, "tag_count" shows the category and the frequency, "tag_subtag" shows the category and the subcategory;
* **label_size**: set the size of the labels;
* **label_shortening**: "clip" cuts the text when it overlaps the margin; "resize" changes the size of the font to fit the available space; "new_line" wraps the text when it overlaps the margin and it rescale the size if the two lines overlaps the bottom margin;
* **label_position**: "nodes" shows a label for each node, "start_end" shows a label for the first and last node of a sequence
* **line_opacity**: it sets the opacity of the lines;
* **line_stroke_color**: it sets the color of the contour of the lines;
* **line_stroke_width**: it sets the thickness of the contour of the lines;
* **line_stroke_thick**: it adjusts the curvature of the lines. If set to 0, the middle point of the lines will coincide and the lines will have no thickness in their middle point. If it is set a value higher than 0, the middle point will move by this size up and down and the line will increase its thickness in the middle;
* **legend**: boolean, show or hide the legend.

To export the visualization, the package use the drawSVG functions on the genSVG output:

**saveSvg("file_path.svg")**: export the draw as svg
**saveSvg("file_path.png")**: export the draw as png

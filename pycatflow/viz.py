import drawSvg as draw
from matplotlib import cm,colors
import pycatflow as pcf
import math
import copy

class Node:
    def __init__(self,index,col_index,x,y,size,value,width,label,subtag):
        self.x=x
        self.index=index
        self.col_index=col_index
        self.y=y
        self.size=size
        self.value=value
        self.width=width
        self.label=label
        self.subtag=subtag

def nodify(data,sort_by="frequency"):
    d={}
    if sort_by=="frequency":
        for x in data.items():
            if type(x[1][next(iter(x[1]))])==tuple:
                d[x[0]]={k: v for k, v in sorted(x[1].items(), key=lambda item: item[1][0],reverse=True)}
            else:
                d[x[0]]={k: v for k, v in sorted(x[1].items(), key=lambda item: item[1],reverse=True)}
    elif sort_by=="subtag":
        for x in data.items():
            d[x[0]]={k: v for k, v in sorted(x[1].items(), key=lambda item: item[1][1],reverse=True)}
    elif sort_by=="alphabetical":
        for x,y in data.items():
            d[x]={k:v for k,v in sorted(y.items())}

    labels=[list(x[1].keys()) for x in d.items()]
    values=[[y[0] if type(y)==tuple else y for y in x[1].values()] for x in d.items()]
    subtags=[[y[1] if type(y)==tuple else "null" for y in x[1].values()] for x in d.items()]
    headers=list(d.keys())
    node_x=0
    count=0
    count2=0

    nodes=[]
    sequence={}

    for l,v,s in zip (labels,values,subtags):
        if count2<len(labels):
            count2+=1  

        for x,y,z in zip (l,v,s):
            nodes.append(Node(count,count2,0,0,y,y,1,x,z))        


            count+=1
           
    for n in nodes:
        if n.label in sequence.keys():
            sequence[n.label].append(n.index)
        else:
            sequence[n.label]=[]
            sequence[n.label].append(n.index)
    
    return [headers,nodes,sequence]


def genSVG(nodes,spacing,node_size,width=None,heigth=None,minValue=1,maxValue=10,node_scaling="linear",color_startEnd=True,color_subtag=True,nodes_color="gray",start_node_color="green",end_node_color="red",palette=None,show_labels=True,label_text="tag",label_font="sans-serif",label_color="black",label_size=5,label_shortening="clip",label_position="nodes",line_opacity=0.5,line_stroke_color="white",line_stroke_width=0.5,line_stroke_thick=0.5,legend=True):
    
    headers=nodes[0]
    nodes2=copy.deepcopy(nodes[1])
    sequence=nodes[2]

    if start_node_color == "green":
        start_node_color = "#4BA167"
    if end_node_color == "red":
        end_node_color = "#A04B83"
    if nodes_color == "gray":
        nodes_color = "#EAEBEE"

    #resizing of the nodes in relation to the canvas size and to the scaling option
    m=max([v.value for v in nodes[1]])
    new_nodes=[]
    if width is not None:
        dx=(width-(spacing*2))/len(headers)
        spacing2=2*(dx/3)
        node_size=dx/3      
    else:
        spacing2=spacing
    if heigth is not None:
        l_col_index=[x.col_index for x in nodes2]
        l_col_index_max=max([l_col_index.count(y.col_index) for y in nodes2])
        sum_values=sum([x.value for x in nodes2 if l_col_index.count(x.col_index)==l_col_index_max])
        max_values=max([x.value for x in nodes2 if l_col_index.count(x.col_index)==l_col_index_max])
        if node_scaling=="linear":
            dy=((heigth-(spacing*2)-(spacing/5))*max_values)/(sum_values+((maxValue/2)*l_col_index_max))
        else:
            dy=((heigth-(spacing*2)-(spacing/5))*max_values)/(sum_values+((max_values/2)*l_col_index_max))
        spacingy=dy/3       
        maxValue=2*(dy/3)
    else:
        spacingy=spacing/5

    node_x=0 
    for n in nodes2:

        n.width=node_size          
            
        if n.col_index!=nodes2[n.index-1].col_index and n.index>0:
            node_x+=node_size
        n.x+=node_x       
          
        
        if node_scaling=="linear":
            n.size=(((n.value+1)*maxValue)/m)+minValue
        elif node_scaling=="log":
            n.size=(((maxValue-minValue)/math.log(m))*math.log(n.value))+minValue

        new_nodes.append(n)
    

    #positioning of the nodes on the canvas (x,y)
    n_x_spacing=spacing
    n_y_spacing=spacing+spacingy
    
    points=[]
    for n in new_nodes:
        
        if n.index>0 and n.col_index==new_nodes[n.index-1].col_index:
            n_y_spacing+=spacingy+n.size
        else:
            n_y_spacing=spacing+spacingy+n.size
        if n.index>0 and n.col_index!=new_nodes[n.index-1].col_index:
            n_x_spacing+=spacing2
            

            
        points.append(pcf.Node(n.index,n.col_index,n.x+n_x_spacing,n.y+n_y_spacing,n.size,n.value,n.width,n.label,n.subtag))
        
    
    #sizing of the canvas
    if width is None and heigth is None:
        
        width=spacing*4+max([x.x for x in points])
        heigth=spacing*4+max([x.y for x in points])+((sum([x.size for x in points])/len(points))*len(set([x.subtag for x in points])))
        
    elif heigth is None:
        heigth=spacing*4+max([x.y for x in points])+((sum([x.size for x in points])/len(points))*len(set([x.subtag for x in points])))

        
    elif width is None:
        width=spacing*4+max([x.x for x in points])
 
    

    #COLORS
    if palette is not None:
        palette=cm.get_cmap(palette[0],palette[1]).colors
        count=0
        subtag_colors={}
        for e in set([n.subtag for n in points]):
            if count<len(palette):
                count+=1
            subtag_colors[e]=colors.to_hex(palette[count])
    else:
        #DEFAULT PALETTE: the number of colors is set in relation to the length of the subtags list
        palette=cm.get_cmap("tab20c",len(set([n.subtag for n in points]))+1).colors
        count=0
        subtag_colors={}
        for e in set([n.subtag for n in points]):
            if count<len(palette)-1:
                count+=1
            subtag_colors[e]=colors.to_hex(palette[count])



    
        
    
    d = draw.Drawing(width, heigth,displayInline=True)
    r = draw.Rectangle(0,0,width,heigth, stroke_width=2, stroke='black',fill="white")
    d.append(r)

    #headers
    h_x_shift=[points[0].x]
    
    
    for x in points:
        if x.x!=points[x.index-1].x and x.index>0:
            h_x_shift.append(x.x)
    
    n2=h_x_shift[1]-h_x_shift[0]
    
    for h,x in zip (headers,h_x_shift):
        l=label_size
        if label_shortening=="resize":
            while len(h)*(l/2)>n2+points[0].size-(n2/8) and l>1:
                if x!=max(h_x_shift):
                    l-=1
                else:
                    break
            d.append(draw.Text(h,x=x,y=heigth-spacing,fontSize=l,font_family=label_font,fill=label_color))
        elif label_shortening=="clip":
            clip = draw.ClipPath()
            clip.append(draw.Rectangle(x,heigth-spacing,n2,label_size))
            d.append(draw.Text(h,x=x,y=heigth-spacing,fontSize=l,font_family=label_font,clip_path=clip,fill=label_color))
        elif label_shortening=="new_line":
            if len(h)*(label_size/2)>n2+points[0].size-(n2/8):
                margin=int((n2+points[0].size-(n2/8))/(label_size/2))

                txt=[h[x:x+margin] for x in range(0,len(h),margin)] 
                while len(txt)*l>(l+n2/5) and l>1:
                    l-=1
            else:
                txt=h                                                              
            d.append(draw.Text(txt,x=x,y=heigth-spacing,fontSize=l,font_family=label_font,fill=label_color))
    
    #lines
    for n in sequence.items():        
        if len(n[1])>1:            
            for k in n[1][:-1]:
                if color_subtag == True:
                    color=subtag_colors[points[k].subtag]
                else:
                    color=nodes_color
                p = draw.Path(fill=color,stroke=line_stroke_color,opacity=line_opacity,stroke_width=line_stroke_width)           
                p.M(points[k].x+points[k].width,heigth-points[k].y)            
                p.L(points[k].x+points[k].width,heigth-points[k].y+points[k].size)
              
            
                if points[k].y==points[n[1][n[1].index(k)+1]].y:
                    p.L(points[n[1][n[1].index(k)+1]].x,heigth-points[k].y+points[k].size)                                    
                    p.L(points[n[1][n[1].index(k)+1]].x,heigth-points[k].y)
                    
                else:
                    xMedium=((points[n[1][n[1].index(k)+1]].x-(points[k].x+points[k].width))/2)+(points[k].x+points[k].width)
                    yMedium=(((heigth-points[k].y+points[k].size)-(heigth-points[n[1][n[1].index(k)+1]].y+points[k].size))/2)+(heigth-points[n[1][n[1].index(k)+1]].y)
                    yMedium2=(((heigth-points[k].y)-(heigth-points[n[1][n[1].index(k)+1]].y))/2)+(heigth-points[n[1][n[1].index(k)+1]].y)
                    p.Q(points[k].x+points[k].width+(spacing/2),heigth-points[k].y+points[k].size,xMedium+line_stroke_thick,yMedium+points[k].size)                    
                    #p.Q(points[k].x+points[k].width+(spacing/2),heigth-points[n[1][n[1].index(k)+1]].y+points[n[1][n[1].index(k)+1]].size,points[n[1][n[1].index(k)+1]].x,heigth-points[n[1][n[1].index(k)+1]].y+points[n[1][n[1].index(k)+1]].size)
                    p.T(points[n[1][n[1].index(k)+1]].x,heigth-points[n[1][n[1].index(k)+1]].y+points[n[1][n[1].index(k)+1]].size)
                    #p.L(points[n[1][n[1].index(k)+1]].x,heigth-points[n[1][n[1].index(k)+1]].y+points[n[1][n[1].index(k)+1]].size) 
                    p.L(points[n[1][n[1].index(k)+1]].x,heigth-points[n[1][n[1].index(k)+1]].y)
                    p.Q(points[n[1][n[1].index(k)+1]].x-(spacing/2),heigth-points[n[1][n[1].index(k)+1]].y,xMedium-line_stroke_thick,yMedium2)
                    #p.Q(points[k].x+points[k].width+(spacing/2),yMedium,points[k].x+points[k].width,points[k].y)
                    p.T(points[k].x+points[k].width,heigth-points[k].y)  

                                  
                p.Z()
                d.append(p)       
                     

    #nodes
    #return points
    col_index_max = 0
    for node in points:
        if node.col_index > col_index_max:
            col_index_max = node.col_index
    

    for node in points:
        if color_startEnd == True and color_subtag == True:
            if node.label not in [n.label for n in points][:node.index]:
                color=start_node_color
            elif node.label not in [n.label for n in points][node.index+1:] and node.col_index < col_index_max: #and node.index<len(points):
                color=end_node_color
            else:
                color=subtag_colors[node.subtag]
        elif color_startEnd == True and color_subtag == False:
            if node.label not in [n.label for n in points][:node.index]:
                color=start_node_color
            elif node.label not in [n.label for n in points][node.index+1:] and node.col_index < col_index_max: #and node.index<len(points):
                color=end_node_color
            else:
                color=nodes_color
        elif color_startEnd == False and color_subtag == True:
            color=subtag_colors[node.subtag]
        elif color_startEnd == False and color_subtag == False:
            color=nodes_color
        if node.label!='':
            r = draw.Rectangle(node.x,heigth-node.y,node.width,node.size, fill=color,stroke=color) #stroke="black"
            d.append(r)


        if show_labels==True:
            
            if label_text=="tag_count":
                txt=node.label+' ('+str(node.value)+')'
            elif label_text=="tag":
                txt=node.label
            elif label_text=="tag_subtag":
                txt=node.label+' ('+str(node.subtag)+')'  
            
            l=label_size
            if label_shortening=="resize":
                while len(txt)*(l/2)>spacing-(spacing/8):
                    if node.x!=max([n.x for n in points]) and l>1:
                        l-=1
                    else:
                        break
            elif label_shortening=="clip":
                clip = draw.ClipPath()
                clip.append(draw.Rectangle(node.x,heigth-node.y-(spacing/5),n2-(n2/8),node.size+2*(spacing/5)))
            elif label_shortening=="new_line":
                if len(txt)*(label_size/2)>n2-2*(n2/8):
                    margin=int((n2-2*(n2/8))/(label_size/2))                    
                    txt=[txt[x:x+margin] for x in range(0,len(txt),margin)]
                    while len(txt)*l>node.size+2*(spacing/8) and l>1:
                        l-=1

            label_pos_y = heigth-node.y+(node.size/2)-(l/2)
            if label_position=="start_end":
                if node.label not in [n.label for n in points][:node.index] or node.label not in [n.label for n in points][node.index+1:] and node.index<len(points) and node.x!=max([n.x for n in points]):
                    if label_shortening=="clip":
                        label= draw.Text(txt,x=node.x+node.width+(n2/8),y=label_pos_y,fontSize=l,font_family=label_font,fill=label_color,clip_path=clip)
                    else:
                        label= draw.Text(txt,x=node.x-(n2/8),y=label_pos_y,fontSize=l,font_family=label_font,fill=label_color,text_anchor="end")

                    
            elif label_position=="nodes":  
                if label_shortening=="clip":        
                
                    label= draw.Text(txt,x=node.x+node.width+(n2/8),y=label_pos_y,fontSize=l,font_family=label_font,fill=label_color,clip_path=clip)
                else:
                    label= draw.Text(txt,x=node.x+node.width+(n2/8),y=label_pos_y,fontSize=l,font_family=label_font,fill=label_color)
            d.append(label)
    
    #legend
    if color_subtag==True and legend==True:
        offset = spacing
        symbol_size=sum([x.size for x in points])/len(points)
        legend_heigth=(symbol_size+offset)*len(subtag_colors)
        legend_header_y = spacing + legend_heigth + (spacing*1.5)
        legend_header=draw.Text("Legend", x=points[0].x, y=legend_header_y,fontSize=label_size,font_family=label_font,fill=label_color)
        d.append(legend_header)
        symbol_y_shift=0
        for e in subtag_colors.items():
            legend_label_y = spacing + legend_heigth + (symbol_size/2) - (label_size/2) - offset - symbol_y_shift
            symbol=draw.Rectangle(points[0].x, spacing+legend_heigth-offset-symbol_y_shift, points[0].width, symbol_size,fill=e[1],stroke=e[1]) #stroke="black"
            name=draw.Text(e[0],x=points[0].x+node.width+(n2/12),y=legend_label_y,fontSize=label_size,fill=label_color)
            d.append(symbol)
            d.append(name)
            if spacing+legend_heigth-(offset)-symbol_y_shift>spacing:
                symbol_y_shift+=offset+symbol_size
            else:
                symbol_y_shift=0
            
    return d

def visualize(data, spacing=50, node_size=10, width=None,heigth=None,minValue=1,maxValue=10,node_scaling="linear",color_startEnd=True,color_subtag=True,nodes_color="gray",start_node_color="green",end_node_color="red",palette=None,show_labels=True,label_text="tag",label_font="sans-serif",label_color="black",label_size=5,label_shortening="clip",label_position="nodes",line_opacity=0.5,line_stroke_color="white",line_stroke_width=0.5,line_stroke_thick=0.5,legend=True, sort_by="frequency"):
    '''
    Generates an SVG from data loaded via the read functions.

    Parameters:
    data: output of the read_file/read functions, a dictionary with keys the temporal data, and values a dictionary with keys the categories and values or the frequency of the category or a tuple with the frequency and the subtag;
    spacing (int): the space between the nodes;
    node_size (int): default node size
    width (int): width of the visualization, if None they are generated from the size of the nodes, if they are specified the nodes will be rescaled to fit the space
    height (int): height of the visualization, if None they are generated from the size of the nodes, if they are specified the nodes will be rescaled to fit the space
    minValue (int): min size of a node 
    maxValue (int): max size of a node
    node_scaling (str): "linear" or ... " "
    color_startEnd (bool) : if True it marks the colors of the first and last appearence of a category;
    color_subtag (bool): if True the nodes and the lines are colored depending by the subcategory;
    nodes_color: the color of the nodes if the previous two options are false, used also for the lines and for the middle nodes in case of startEnd option;
    start_node_color (): Defaults to "green"
    end_node_color (): Defaults to "red"
    palette: a tuple with the name of the matplotlib palette and the number of colors ("viridis",12);
    show_labels (bool): Defaults to True
    label_text (str): "tag" shows the category, "tag_count" shows the category and the frequency, "tag_subtag" shows the category and the subcategory;
    label_font (str): Defaults to "sans-serif"
    label_color (str): Defaults to "black"
    label_size (int): Defaults to 5
    label_shortening (str): "clip" cuts the text when it overlaps the margin; "resize" changes the size of the font to fit the available space; "new_line" wraps the text when it overlaps the margin and it rescale the size if the two lines overlaps the bottom margin;
    label_position (str): "nodes" shows a label for each node, "start_end" shows a label for the first and last node of a sequence
    line_opacity (float): Defaults to 0.5
    line_stroke_color (str): Defaults to "white"
    line_stroke_width (float): Defaults to 0.5
    line_stroke_thick (float): Defaults to 0.5
    legend (bool): If True a Legend is included
    sort_by (str): "frequency" or "alphabetical" or "subtag"

    Returns:
    viz (drawSvg.drawing.Drawing)
    '''

    nodes = pcf.nodify(data, sort_by=sort_by)
    viz = genSVG(nodes, spacing,node_size,width=width, heigth=heigth, minValue=minValue, maxValue= maxValue,node_scaling=node_scaling, color_startEnd=color_startEnd, color_subtag=color_subtag, nodes_color=nodes_color, start_node_color=start_node_color, end_node_color=end_node_color, palette=palette, show_labels=show_labels, label_text=label_text, label_font=label_font, label_color=label_color, label_size=label_size,label_shortening=label_shortening,label_position=label_position,line_opacity=line_opacity,line_stroke_color=line_stroke_color,line_stroke_width=line_stroke_width,line_stroke_thick=line_stroke_thick,legend=legend)
    return viz
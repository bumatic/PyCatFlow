import drawSvg as draw
from matplotlib import cm,colors
import pycatflow as pcf
import math

def genSVG(nodes,spacing,node_size,width=None,heigth=None,minValue=1,maxValue=10,node_scaling="linear",color_startEnd=True,color_subtag=True,nodes_color="gray",start_node_color="green",end_node_color="red",palette=None,show_labels=True,label_text="tag",label_font="sans-serif",label_color="black",label_size=5,label_shortening="clip",label_position="nodes",line_opacity=0.5,line_stroke_color="white",line_stroke_width=0.5,line_stroke_thick=0.5,legend=True):
    headers=nodes[0]
    
    sequence=nodes[2]

    m=max([v.value for v in nodes[1]])
    new_nodes=[]
    if width is not None:
        dx=(width-(spacing*2))/len(headers)
        spacing2=2*(dx/3)
        node_size=dx/3      
    else:
        spacing2=spacing
    if heigth is not None:
        #rows=max([[x.col_index for x in nodes[1]].count(y.col_index) for y in nodes[1]])
        #med=m/len(nodes[1])
        l_col_index=[x.col_index for x in nodes[1]]
        l_col_index_max=max([l_col_index.count(y.col_index) for y in nodes[1]])
        sum_values=sum([x.value for x in nodes[1] if l_col_index.count(x.col_index)==l_col_index_max])
        max_values=max([x.value for x in nodes[1] if l_col_index.count(x.col_index)==l_col_index_max])
        dy=((heigth-(spacing*2)-(spacing/5))*max_values)/((sum_values)+((spacing/5)*l_col_index_max))
        spacingy=dy/3       
        maxValue=2*(dy/3)

    
    
    node_x=0 
    for n in nodes[1]:

        n.width=node_size          
            
        if n.col_index!=nodes[1][n.index-1].col_index and n.index>0:
            node_x+=node_size
        n.x+=node_x  

        
            
        
        if node_scaling=="linear":
            n.size=(((n.value+1)*maxValue)/m)-minValue
        elif node_scaling=="log":
            n.size=(((maxValue-minValue)/math.log(m))*math.log(n.value))+minValue

        new_nodes.append(n)
    
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
        
    
    
    if width is None and heigth is None:
        
        width=spacing*4+max([x.x for x in points])
        heigth=spacing*4+max([x.y for x in points])+((sum([x.size for x in points])/len(points))*len(set([x.subtag for x in points])))
        
    elif heigth is None:
        heigth=spacing*4+max([x.y for x in points])+((sum([x.size for x in points])/len(points))*len(set([x.subtag for x in points])))
        #points=[pcf.Node(n.index,(n.x*(width-spacing*2)/max([x.x for x in points])),n.y,n.size,n.value,n.width,n.label,n.subtag) for n in points]
        #spacing=points[1].x-(points[0].x+points[0].size)
        
    elif width is None:
        width=spacing*4+max([x.x for x in points])
        #points=[pcf.Node(n.index,n.x,(n.y*(heigth-spacing*2)/max([x.y for x in points])),n.size,n.value,n.width,n.label,n.subtag) for n in points]
        #n_y_spacing=(spacing/3)
        #for n in points:
        #    if n.index>0 and n.x==nodes[1][n.index-1].x:
        #        n_y_spacing+=spacing/5
        #    else:
        #        n_y_spacing=(spacing/3)
        #    n.y+=n_y_spacing

        
    #else:  
        #points=[pcf.Node(n.index,(n.x*(width-spacing)/max([x.x for x in points])),(n.y*(heigth-spacing)/max([x.y for x in points])),n.size,n.value,n.width,n.label,n.subtag) for n in points]    
        #n_y_spacing=(spacing/3)
        #for n in points:
        #    if n.index>0 and n.x==nodes[1][n.index-1].x:
        #        n_y_spacing+=spacing/5
        #    else:
        #        n_y_spacing=(spacing/3)
        #    n.y+=n_y_spacing      
    

    
    if palette is not None:
        palette=cm.get_cmap(palette[0],palette[1]).colors
        count=0
        subtag_colors={}
        for e in set([n.subtag for n in points]):
            if count<len(palette):
                count+=1
            subtag_colors[e]=colors.to_hex(palette[count])
    else:
        palette=cm.get_cmap("Paired",len(set([n.subtag for n in points]))).colors
        
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
    #n_x_shift=spacing
    #n_y_shift=spacing
    for node in points:
        if color_startEnd == True and color_subtag == True:
            if node.label not in [n.label for n in points][:node.index]:
                color=start_node_color
            elif node.label not in [n.label for n in points][node.index+1:] and node.index<len(points):
                color=end_node_color
            else:
                color=subtag_colors[node.subtag]
        elif color_startEnd == True and color_subtag == False:
            if node.label not in [n.label for n in points][:node.index]:
                color=start_node_color
            elif node.label not in [n.label for n in points][node.index+1:] and node.index<len(points):
                color=end_node_color
            else:
                color=nodes_color
        elif color_startEnd == False and color_subtag == True:
            color=subtag_colors[node.subtag]
        elif color_startEnd == False and color_subtag == False:
            color=nodes_color
        #if node.x!=points[node.index-1].x:
            #n_x_shift+=spacing
        r = draw.Rectangle(node.x,heigth-node.y,node.width,node.size, fill=color,stroke="black")
        d.append(r)


        if show_labels==True:
            
            if label_text=="tag_count":
                txt=node.label+' ('+str(node.value)+')'
            elif label_text=="tag":
                txt=node.label
            elif label_text=="tag_subtag":
                txt=node.label+' ('+str(node.subtag)+')'  
            
            #if len(txt)*(label_size/2)>spacing-2*(spacing/8):
                #txt=[txt[:int((spacing-2*(spacing/8))/(label_size/2))],txt[int((spacing-2*(spacing/8))/(label_size/2)):]]
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


            if label_position=="start_end":
                if node.label not in [n.label for n in points][:node.index] or node.label not in [n.label for n in points][node.index+1:] and node.index<len(points) and node.x!=max([n.x for n in points]):
                    if label_shortening=="clip":
                        label= draw.Text(txt,x=node.x+node.width+(n2/8),y=heigth-node.y+(node.size/2),fontSize=l,font_family=label_font,fill=label_color,clip_path=clip)
                    else:
                        label= draw.Text(txt,x=node.x-(n2/8),y=heigth-node.y+(node.size/2),fontSize=l,font_family=label_font,fill=label_color,text_anchor="end")

                    
            elif label_position=="nodes":  
                if label_shortening=="clip":        
                
                    label= draw.Text(txt,x=node.x+node.width+(n2/8),y=heigth-node.y+(node.size/2),fontSize=l,font_family=label_font,fill=label_color,clip_path=clip)
                else:
                    label= draw.Text(txt,x=node.x+node.width+(n2/8),y=heigth-node.y+(node.size/2),fontSize=l,font_family=label_font,fill=label_color)
            d.append(label)
    
    #legend
    if color_subtag==True and legend==True:
        
        
        symbol_size=sum([x.size for x in points])/len(points)
        legend_heigth=symbol_size*len(subtag_colors)
        legend_header=draw.Text("Legend",x=points[0].x,y=spacing+legend_heigth,fontSize=label_size,font_family=label_font,fill=label_color)
        d.append(legend_header)
        symbol_y_shift=0
        symbol_x_shift=0
        for e in subtag_colors.items():            
            symbol=draw.Rectangle(points[0].x+symbol_x_shift,spacing+legend_heigth-n2/5-symbol_y_shift,points[0].width,symbol_size,fill=e[1],stroke="black")
            name=draw.Text(e[0],x=points[0].x+node.width+(n2/12)+symbol_x_shift,y=spacing+legend_heigth-n2/5-symbol_y_shift,fontSize=label_size,fill=label_color)
            d.append(symbol)
            d.append(name)
            if spacing+legend_heigth-n2/5-symbol_y_shift>spacing:
                symbol_y_shift+=n2/5+symbol_size
            else:
                symbol_x_shift+=spacing+n2/5
                symbol_y_shift=0



    return d
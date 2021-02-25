class Node:
    def __init__(self,index,x,y,size,value,width,label,subtag):
        self.x=x
        self.index=index
        self.y=y
        self.size=size
        self.value=value
        self.width=width
        self.label=label
        self.subtag=subtag

def nodify(data,size,maxValue=10,sort_by="frequency"):
    d={}
    if sort_by=="frequency":
        for x in data.items():
            d[x[0]]={k: v for k, v in sorted(x[1].items(), key=lambda item: item[1],reverse=True)}
    else:
        for x,y in data.items():
            d[x]={k:v for k,v in sorted(y.items())}

    labels=[list(x[1].keys()) for x in d.items()]
    values=[[y[0] if type(y)==tuple else y for y in x[1].values()] for x in d.items()]
    m=max([max([y[0] if type(y)==tuple else y for y in x[1].values()]) for x in d.items()] )
    subtags=[[y[1] if type(y)==tuple else "null" for y in x[1].values()] for x in d.items()]
    headers=list(d.keys())
    node_x=0
    count=0
    count2=0

    nodes=[]
    sequence={}

    for l,v,s in zip (labels,values,subtags):
        if count2<len(labels)-1:
            count2+=1  
        node_y=0
        for x,y,z in zip (l,v,s):
            #node_y+=y
            nodes.append(Node(count,node_x,node_y,y*maxValue/m,y,size,x,z))

            count+=1
           
        node_x+=size

    for n in nodes:
        if n.label in sequence.keys():
            sequence[n.label].append(n.index)
        else:
            sequence[n.label]=[]
            sequence[n.label].append(n.index)
    
    return [headers,nodes,sequence]

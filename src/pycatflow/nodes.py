import math

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
    #m=max([max([y[0] if type(y)==tuple else y for y in x[1].values()]) for x in d.items()] )
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

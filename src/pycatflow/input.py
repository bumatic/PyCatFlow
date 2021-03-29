def find_delimiter (data):
    if type(data)==str:
        headers=data.split("\n")[0]
    else:
        headers=data.decode("utf-8").split("\n")[0]
    delimiters=[",",";","\t","\s","|"]
    l={}
    for d in delimiters:
        count=0
        for c in headers:
            if c.find(d)!=-1:
                count+=1
        l[d]=count
    return [k for k,v in l.items() if v== max(l.values())][0]

def typeDetect(data,prefix):
    t1=[]
    t2=[]
    for x in data:
        x=x.replace(prefix,"")
        try:
            t1.append(int(x))
            t2.append("int")            
        except ValueError:
            try:
                t1.append(float(x))
                t2.append("float")
            except ValueError:
                from dateutil.parser import parse,ParserError
                try:
                    t1.append(parse(x))
                    t2.append("date")
                except ParserError:
                    t1.append(x)
                    t2.append("string")
                    continue
    t=[]
    for k in set(t2):
        [t.append(data[t1.index(h)]) for h in sorted([x for x,y in zip(t1,t2) if y==k]) if h not in t]
    return t  

def temporal_data(data,time_field,tag_field,subtag_field,orientation,sort_field,prefix):
    new_data={}
    if orientation=='horizontal':
        if sort_field is None:
            columns=typeDetect(data[time_field],prefix)
        else:
            columns=[]
            n_sort_field=[int(x) for x in data[sort_field]]
            [columns.append(data[time_field][n_sort_field.index(x)]) for x in sorted(n_sort_field) if x not in columns]
            
        tags=data[tag_field]
        counts=[[x for x in tags].count(x) for x in tags]
        if subtag_field is not None:    
            for l in columns:
                d={x:(z,y) for t,x,y,z in zip(data[time_field],tags,data[subtag_field],counts)if l==t}
                new_data[l]={k: v for k, v in d.items()}
        else:
            for l in columns:
                d={x:z for t,x,z in zip(data[time_field],tags,counts)if l==t}
                new_data[l]={k: v for k, v in d.items()}
    else:
        if subtag_field is not None:
            columns=typeDetect(list(data.keys()),prefix)
            
            tags=[]
            for l in columns:
                [tags.append(y) for y in data[l]]
            counts=[[x for x in tags].count(x) for x in tags]
            for l in columns:
                data[l+"_count"]=[counts[tags.index(x)] for x in data[l]]
                d={x:(z,y) for x,y,z in zip(data[l],data[l+subtag_field],data[l+"_count"])}
                new_data[l]={k: v for k, v in d.items()}
        else:
            types=typeDetect(list(data.keys()),prefix)
            columns=typeDetect(list(data.keys()),prefix)
            tags=[]
            for l in columns:
                [tags.append(y) for y in data[l]]
            counts=[[x for x in tags].count(x) for x in tags]
            for l in columns:
                data[l+"_count"]=[counts[tags.index(x)] for x in data[l]]
                d={x:z for x,z in zip(data[l],data[l+"_count"])}
                new_data[l]={k: v for k, v in d.items()}
        
    return new_data

def read_file(filepath,time_field=None,tag_field=None,subtag_field=None,sort_field=None,orientation="horizontal",delimiter=None,prefix=""):
    with open (filepath,"rb") as f:
        data=f.read()
    if delimiter is None:
        delimiter=find_delimiter(data)        
    else:
        delimiter=delimiter    
    headers=data.decode("utf-8-sig").split("\n")[0].split(delimiter)
    lines=data.decode("utf-8-sig").split("\n")[1:]
    data={}
    for h in headers:
        data[h]=[l.split(delimiter)[headers.index(h)] for l in lines]

    data=temporal_data(data,time_field,tag_field,subtag_field,orientation,sort_field,prefix)
    return data

def read(data,time_field=None,tag_field=None,subtag_field=None,sort_field=None,orientation="horizontal",delimiter=None,newLine=None,prefix=""):
    if type(data)==str:
        if delimiter is None:
            delimiter=find_delimiter(data)        
        else:
            delimiter=delimiter
        if newLine is None:
            newLine="\n"       
        else:
            newLine=newLine
        headers=data.split(newLine)[0].split(delimiter)
        lines=data.split(newLine)[1:]
        data={}
        for h in headers:
            data[h]=[l.split(delimiter)[headers.index(h)] for l in lines]
    if type(data)==list:
        headers=data[0]
        lines=data[1:]
        data={}
        for h in headers:
            data[h]=[l[headers.index(h)] for l in lines]   
    
        
    new_data=temporal_data(data,time_field,tag_field,subtag_field,orientation,sort_field,prefix)
    return new_data
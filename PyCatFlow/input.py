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

def temporal_data(data,time_field,tag_field,subtag_field,orientation,sorted_by):
    new_data={}
    if orientation=='horizontal':
        columns=sorted(set(data[time_field]))
        tags=data[tag_field]
        counts=[[x for x in tags].count(x) for x in tags]
        if subtag_field is not None:    
            for l in columns:
                d={x:(z,y) for t,x,y,z in zip(data[time_field],tags,data[subtag_field],counts)if l==t}
                if sorted_by=="frequency":
                    new_data[l]={k: v for k, v in sorted(d.items(), key=lambda item: item[1],reverse=True)}
                else:
                    new_data[l]={k: v for k, v in d.items()}

        else:
            for l in columns:
                d={x:z for t,x,z in zip(data[time_field],tags,counts)if l==t}
                if sorted_by=="frequency":
                    new_data[l]={k: v for k, v in sorted(d.items(), key=lambda item: item[1],reverse=True)}
                else:
                    new_data[l]={k: v for k, v in d.items()}
    else:
        if subtag_field is not None:
            columns=sorted([x for x in data.keys() if not x.endswith(subtag_field)])
            tags=[]
            for l in columns:
                [tags.append(y) for y in data[l]]
            counts=[[x for x in tags].count(x) for x in tags]
            for l in columns:
                data[l+"_count"]=[counts[tags.index(x)] for x in data[l]]
                d={x:(z,y) for x,y,z in zip(data[l],data[l+subtag_field],data[l+"_count"])}
                if sorted_by=="frequency":
                    new_data[l]={k: v for k, v in sorted(d.items(), key=lambda item: item[1],reverse=True)}
                else:
                    new_data[l]={k: v for k, v in d.items()}
        else:
            columns=sorted(list(data.keys()))
            tags=[]
            for l in columns:
                [tags.append(y) for y in data[l]]
            counts=[[x for x in tags].count(x) for x in tags]
            for l in columns:
                data[l+"_count"]=[counts[tags.index(x)] for x in data[l]]
                d={x:z for x,z in zip(data[l],data[l+"_count"])}
                if sorted_by=="frequency":
                    new_data[l]={k: v for k, v in sorted(d.items(), key=lambda item: item[1],reverse=True)}
                else:
                    new_data[l]={k: v for k, v in d.items()}

        
    return new_data









def read_file(filepath,time_field=None,tag_field=None,subtag_field=None,orientation="horizontal",delimiter=None,sorted_by="frequency"):
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

    data=temporal_data(data,time_field,tag_field,subtag_field,orientation,sorted_by)
    return data

def read(data,time_field=None,tag_field=None,subtag_field=None,orientation="horizontal",delimiter=None,newLine=None):
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
    
        
    new_data=temporal_data(data,time_field,tag_field,subtag_field,orientation)
    return new_data
        
        





def find_delimiter(data):
    """
    This function finds and returns the delimiter of the given data.

    Parameters:
    data (string): data in which to look for the used delimiter

    Returns:
    (string): delimiter used in given data
    """
    if type(data) == str:
        headers = data.split("\n")[0]
    else:
        headers = data.decode("utf-8").split("\n")[0]
    delimiters = [",", ";", "\t"]  # Removed: , "\s", "|"
    l = {}
    for d in delimiters:
        count = 0
        for c in headers:
            if c.find(d) != -1:
                count += 1
        l[d] = count
    return [k for k, v in l.items() if v == max(l.values())][0]


def detect_dtype(data, prefix):
    """
    Transforms objects inside data into the correct datatypes and returns a sorted and duplicate-free list.

    Parameters:
    data (list): a single column
    prefix (str): delete an unwanted prefix out of the data

    Returns:
    (list): original data without duplicates in correct datatypes
    """
    t1 = []
    t2 = []
    for x in data:
        x = x.replace(prefix, "")
        try:
            t1.append(int(x))
            t2.append("int")            
        except ValueError:
            try:
                t1.append(float(x))
                t2.append("float")
            except ValueError:
                from dateutil.parser import parse, ParserError
                try:
                    t1.append(parse(x))
                    t2.append("date")
                except ParserError:
                    t1.append(x)
                    t2.append("string")
                    continue
    t = []
    for k in set(t2):
        [t.append(data[t1.index(h)]) for h in sorted([x for x, y in zip(t1, t2) if y == k]) if h not in t]
    return t  


def prepare_data(data, columns_data, node_data, category_data, orientation, sort_field, prefix):
    """
    Arranges the data into a new format to make is usable for the flow visualisation.

    Parameters:
    data (dict): original data transformed to a dict
    columns_data (str): Name of the column with temporal data (None if orientation="vertical")
    node_data (str): which column to use as nodes in the graph 
    category_data (str): Name of the column containing optional categories of nodes
    orientation (str): Horizontal if the temporal data are in one columns, vertical if the temporal data are the name of the column
    sort_field (str): Optionally provide the name of a column determining the order of the time_field columns
    prefix (str): delete an unwanted prefix out of the data

    Returns:
    (dict): Dictionary of parsed data
    """
    new_data = {}
    if orientation == 'horizontal':
        if sort_field is None:
            columns = detect_dtype(data[columns_data], prefix)
        else:
            columns = []
            n_sort_field = [int(x) for x in data[sort_field]]
            [columns.append(data[columns_data][n_sort_field.index(x)]) for x in sorted(n_sort_field) if x not in columns]
            
        tags = data[node_data]
        counts = [[x for x in tags].count(x) for x in tags]
        if category_data is not None:
            for l in columns:
                d = {x: (z, y) for t, x, y, z in zip(data[columns_data], tags, data[category_data], counts) if l == t}
                new_data[l] = {k: v for k, v in d.items()}
        else:
            for l in columns:
                d = {x: z for t, x, z in zip(data[columns_data], tags, counts) if l == t}
                new_data[l] = {k: v for k, v in d.items()}
    else:
        if category_data is not None:
            columns = detect_dtype(list(data.keys()), prefix)
            
            tags = []
            for l in columns:
                [tags.append(y) for y in data[l]]
            counts = [[x for x in tags].count(x) for x in tags]
            for l in columns:
                data[l+"_count"] = [counts[tags.index(x)] for x in data[l]]
                d = {x: (z, y) for x, y, z in zip(data[l], data[l + category_data], data[l + "_count"])}
                new_data[l] = {k: v for k, v in d.items()}
        else:
            types = detect_dtype(list(data.keys()), prefix)
            columns = detect_dtype(list(data.keys()), prefix)
            tags = []
            for l in columns:
                [tags.append(y) for y in data[l]]
            counts = [[x for x in tags].count(x) for x in tags]
            for l in columns:
                data[l+"_count"] = [counts[tags.index(x)] for x in data[l]]
                d = {x: z for x, z in zip(data[l], data[l+"_count"])}
                new_data[l] = {k: v for k, v in d.items()}
    return new_data


def read_file(filepath,
              columns=None,
              nodes=None,
              categories=None,
              column_order=None,
              orientation="horizontal",
              delimiter=None,
              line_delimiter=None,
              prefix=""):
    """
    Loads data from file and returns structured data for visualisation.
    
    Parameters:
    filepath (str): Path to file
    columns (str): Name of the column with temporal data (leave None if orientation="vertical")
    nodes (str): Name of the column containing the node data
    categories (str): Name of the column containing optional categories of nodes
    column_order (str): Optionally provide the name of a column determining the order of the columns
    orientation (str): Horizontal if the temporal data are in one columns, vertical if the temporal data are the name of the column
    delimiter (str): Otpionally specify the delimiter, if None it will try to autodetect
    line_delimiter (str): optionally define the line_delimiter separator, by default \n
    prefix (str): delete an unwanted prefix out of the data

    Returns:
    (dict): Dictionary of parsed data
    """

    with open(filepath, "rb") as f:
        data = f.read()
    if delimiter is None:
        delimiter = find_delimiter(data)
    else:
        delimiter = delimiter
    if line_delimiter is None:
        line_delimiter = "\n"
    else:
        line_delimiter = line_delimiter
    headers = data.decode("utf-8-sig").split(line_delimiter)[0].split(delimiter)
    lines = data.decode("utf-8-sig").split(line_delimiter)[1:]
    lines = [line for line in lines if line != '']
    data = {}
    for h in headers:
        data[h.replace('\r', '')] = [line.split(delimiter)[headers.index(h)].replace('\r', '') for line in lines]
    
    data = prepare_data(data, columns, nodes, categories, orientation, column_order, prefix)
    return data


def read(data,
         columns=None,
         nodes=None,
         categories=None,
         column_order=None,
         orientation="horizontal",
         delimiter=None,
         line_delimiter=None,
         prefix=""):
    """
    Parses a string into structured data for visualization.

    Parameters:
    data (str): String with records divided by line_delimiter and fields divided by delimiter; list of lists with the first element as list of headers; dictionary with headers as keys and values as lists
    columns (str): Name of the column with temporal data (leave None if orientation="vertical")
    nodes (str): Name of the column containing the node data
    categories (str): Name of the column containing optional categories of nodes
    column_order (str): Optionally provide the name of a column determining the order of the columns
    orientation (str): Horizontal if the temporal data are in one columns, vertical if the temporal data are the name of the column
    delimiter (str): Otpionally specify the delimiter, if None it will try to autodetect
    line_delimiter (str): optionally define the line_delimiter separator, by default \n
    prefix (str): delete an unwanted prefix out of the data

    Returns:
    (dict): Dictionary of parsed data
    """

    if type(data) == str:
        if delimiter is None:
            delimiter = find_delimiter(data)
        else:
            delimiter = delimiter
        if line_delimiter is None:
            line_delimiter = "\n"
        else:
            line_delimiter = line_delimiter
        headers = data.split(line_delimiter)[0].split(delimiter)
        lines = data.split(line_delimiter)[1:]
        data = {}
        for h in headers:
            data[h] = [line.split(delimiter)[headers.index(h)] for line in lines]
    if type(data) == list:
        headers = data[0]
        lines = data[1:]
        data = {}
        for h in headers:
            data[h.replace('\r', '')] = [line.split(delimiter)[headers.index(h)].replace('\r', '') for line in lines]
    
    data = prepare_data(data, columns, nodes, categories, orientation, column_order, prefix)
    return data
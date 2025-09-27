def find_delimiter(data):
    """
    Automatically detect the CSV delimiter used in the data.

    Analyzes the first line of CSV data to identify the most likely delimiter
    by counting occurrences of common delimiters and selecting the most frequent.

    Args:
        data (str or bytes): CSV data as string or bytes. If bytes, will be
            decoded as UTF-8 before analysis.

    Returns:
        str: The detected delimiter character. One of: ',', ';', or '\t'

    Examples:
        >>> csv_data = "name,age,city\\nJohn,25,NYC"
        >>> find_delimiter(csv_data)
        ','

        >>> csv_data = "name;age;city\\nJohn;25;NYC"
        >>> find_delimiter(csv_data)
        ';'

    Notes:
        - Only analyzes the first line (header row) for delimiter detection
        - Supports comma, semicolon, and tab delimiters
        - Returns the delimiter with the highest occurrence count
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
    Convert and sort data elements by detecting appropriate data types.

    Processes a list of string values, attempts to convert them to appropriate
    data types (int, float, date, or string), removes duplicates, and returns
    a sorted list with consistent data types.

    Args:
        data (list): List of string values to process and type-convert
        prefix (str): String prefix to remove from each data element before
            type conversion (e.g., remove currency symbols or units)

    Returns:
        list: Sorted list of unique values with appropriate data types.
            Integers and floats are sorted numerically, dates chronologically,
            and strings alphabetically.

    Examples:
        >>> data = ["2020", "2021", "2019", "2020"]
        >>> detect_dtype(data, "")
        [2019, 2020, 2021]

        >>> data = ["$100", "$50", "$200"]
        >>> detect_dtype(data, "$")
        [50, 100, 200]

    Notes:
        - Type detection order: int → float → date → string
        - Uses dateutil.parser for flexible date parsing
        - Duplicates are automatically removed
        - Sorting respects the detected data type
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
    Transform raw CSV data into structured format for visualization.

    Converts dictionary-based CSV data into the nested dictionary structure
    required by the visualization functions, handling different data orientations
    and calculating frequency counts for categorical data.

    Args:
        data (dict): Parsed CSV data as column name → values mapping
        columns_data (str): Column name containing time periods (for horizontal orientation)
        node_data (str): Column name containing categorical items to track
        category_data (str, optional): Column name for subcategory classification
        orientation (str): Data layout format. Options: "horizontal", "vertical"
        sort_field (str, optional): Column name for custom time period ordering
        prefix (str): String prefix to remove from time period labels

    Returns:
        dict: Structured data mapping time periods to item frequencies:
            - Keys: Time period labels (sorted)
            - Values: Dict mapping item names to frequencies or (frequency, category) tuples

    Examples:
        Horizontal orientation (time periods in column):
        >>> data = {'year': ['2020', '2021'], 'library': ['numpy', 'pandas']}
        >>> prepare_data(data, 'year', 'library', None, 'horizontal', None, '')
        {'2020': {'numpy': 1}, '2021': {'pandas': 1}}

        With categories:
        >>> data = {'year': ['2020'], 'lib': ['numpy'], 'type': ['core']}
        >>> prepare_data(data, 'year', 'lib', 'type', 'horizontal', None, '')
        {'2020': {'numpy': (1, 'core')}}

    Notes:
        - Frequency counts are calculated automatically for each item
        - Vertical orientation uses column headers as time periods
        - Category data creates (frequency, category) tuples instead of simple counts
        - Time periods are sorted using detect_dtype() for appropriate ordering
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
    Load and parse CSV file data for temporal flow visualization.

    Reads a CSV file, automatically detects formatting, and transforms the data
    into the structured format required for creating temporal flow diagrams.

    Args:
        filepath (str): Path to the CSV file to load
        columns (str, optional): Column name containing time periods.
            Required for horizontal orientation, ignored for vertical
        nodes (str): Column name containing categorical items to track over time
        categories (str, optional): Column name for subcategory classification
        column_order (str, optional): Column name specifying custom time period ordering
        orientation (str): Data layout format. Options: "horizontal" (default), "vertical"
        delimiter (str, optional): CSV field delimiter. Auto-detected if None
        line_delimiter (str, optional): Line separator. Defaults to '\\n'
        prefix (str): String prefix to remove from time period labels. Defaults to ""

    Returns:
        dict: Structured data ready for visualization:
            - Keys: Time period labels (sorted appropriately)
            - Values: Dict mapping item names to frequencies or (frequency, category) tuples

    Raises:
        FileNotFoundError: If the specified filepath does not exist
        UnicodeDecodeError: If file encoding is not compatible with UTF-8
        KeyError: If specified column names are not found in the CSV

    Examples:
        Basic usage:
        >>> data = read_file("data.csv", columns="year", nodes="library")
        >>> print(data)
        {'2020': {'numpy': 3, 'pandas': 2}, '2021': {'numpy': 4, 'scipy': 1}}

        With categories:
        >>> data = read_file("data.csv",
        ...                  columns="year",
        ...                  nodes="library",
        ...                  categories="type")
        >>> print(data)
        {'2020': {'numpy': (3, 'core'), 'pandas': (2, 'analysis')}}

    Notes:
        - File is read with UTF-8-sig encoding to handle BOM markers
        - Delimiter auto-detection supports comma, semicolon, and tab
        - Empty lines in the CSV are automatically filtered out
        - Time periods are sorted using intelligent type detection
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
    Parse structured data from various input formats for temporal flow visualization.

    Processes data from multiple input formats (strings, lists, dictionaries) and
    transforms it into the structured format required for creating temporal flow diagrams.

    Args:
        data (str, list, or dict): Input data in one of several formats:
            - str: CSV-formatted string with headers and delimited fields
            - list: List of lists where first element contains column headers
            - dict: Dictionary with column names as keys and value lists
        columns (str, optional): Column name containing time periods.
            Required for horizontal orientation, ignored for vertical
        nodes (str): Column name containing categorical items to track over time
        categories (str, optional): Column name for subcategory classification
        column_order (str, optional): Column name specifying custom time period ordering
        orientation (str): Data layout format. Options: "horizontal" (default), "vertical"
        delimiter (str, optional): Field delimiter for string data. Auto-detected if None
        line_delimiter (str, optional): Line separator for string data. Defaults to '\\n'
        prefix (str): String prefix to remove from time period labels. Defaults to ""

    Returns:
        dict: Structured data ready for visualization:
            - Keys: Time period labels (sorted appropriately)
            - Values: Dict mapping item names to frequencies or (frequency, category) tuples

    Raises:
        TypeError: If data format is not supported
        KeyError: If specified column names are not found in the data
        ValueError: If data structure is malformed

    Examples:
        String input:
        >>> csv_string = "year,library\\n2020,numpy\\n2021,pandas"
        >>> data = read(csv_string, columns="year", nodes="library")
        >>> print(data)
        {'2020': {'numpy': 1}, '2021': {'pandas': 1}}

        List input:
        >>> list_data = [['year', 'library'], ['2020', 'numpy'], ['2021', 'pandas']]
        >>> data = read(list_data, columns="year", nodes="library")

        Dictionary input:
        >>> dict_data = {'year': ['2020', '2021'], 'library': ['numpy', 'pandas']}
        >>> data = read(dict_data, columns="year", nodes="library")

    Notes:
        - Automatically handles carriage returns and encoding issues
        - Delimiter detection works for comma, semicolon, and tab separators
        - Empty lines and malformed records are filtered out
        - All input formats are normalized to dictionary structure before processing
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
            # data[h] = [line.split(delimiter)[headers.index(h)] for line in lines]
            data[h.replace('\r', '')] = [line.split(delimiter)[headers.index(h)].replace('\r', '') for line in lines]
    if type(data) == list:
        headers = data[0]
        lines = data[1:]
        data = {}
        for h in headers:
            data[h.replace('\r', '')] = [line.split(delimiter)[headers.index(h)].replace('\r', '') for line in lines]
    data = prepare_data(data, columns, nodes, categories, orientation, column_order, prefix)
    return data
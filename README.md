# PyCatFlow

This package is a visualization tool which allows the representation of temporal developments, based on categorical data.

## Install 

Download the repository install the package by running the setup.py install routine. 
Make sure to install the requirements as well:

```python
pip3 install -r requirements.txt
python3 setup.py install
```
Alternatively you can download the folder and place the pycatflow subfolder in your project directory. 

**Additional Requirements:** 
The visualization and export is based on the [drawSvg](https://pypi.org/project/drawSvg/) package that 
in turn requires cairo to be installed as an external requirement. Platform-specific instructions for installing cairo are available on the 
[cairo homepage](https://www.cairographics.org/download/).

On macOS cairo can be installed easily using [homebrew](https://brew.sh/):

```Bash
$ brew install cairo
```

## Basic usage

The visualization library provides many functionalities for adjusting the visual output. It's simplest use is however as follows:

```Python
import pycatflow as pcf

# Loading and parsing data:
data = pcf.read_file("sample_data.tsv", columns="versions", nodes="permissions", categories="app_review",
                     column_order="col_order")

# Generating the visualization
viz = pcf.visualize(data, 35, 10, width=1200, height=250, label_size=4, label_shortening="resize")
viz.savePng('sample_viz.png')
viz.saveSvg('sample_viz.svg')
viz
```

The code and sample data are provided in the example folder. Running it creates this visualization:

![Sample Visualization](example/sample_viz.svg)


## Credits

PyCatFlow was conceptualized by Marcus Burkhardt and implemented by Herbert Natta (@herbertmn). It is inspired by the Rankflow visualization tool develped by Bernhard Rieder.


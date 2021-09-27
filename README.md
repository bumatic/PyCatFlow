[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5531785.svg)](https://doi.org/10.5281/zenodo.5531785)

# PyCatFlow

This package is a visualization tool which allows the representation of temporal developments, based on categorical data.

## Install 

PyCatFlow is available on PyPi:

```Shell
$ pip3 install pycatflow
```
Alternatively you can download the repository and install the package by running 
the setup.py install routine. Make sure to install the requirements as well:

```python
pip3 install -r requirements.txt
python3 setup.py install
```

**Additional Requirements:** 
The visualization and export is based on the [drawSvg](https://pypi.org/project/drawSvg/) package that 
in turn requires cairo to be installed as an external requirement. Platform-specific instructions for installing cairo are available on the 
[cairo homepage](https://www.cairographics.org/download/).

On macOS cairo can be installed easily using [homebrew](https://brew.sh/):

```Bash
$ brew install cairo
```

## Basic usage

The visualization library provides many functionalities for adjusting the visual output. A simple use case is however as follows:

```Python
import pycatflow as pcf

# Loading and parsing data:
data = pcf.read_file("sample_data_ChatterBot_Requirements.csv", columns="column", nodes="items", categories="category", column_order="column order")

# Generating the visualization
viz = pcf.visualize(data, spacing=20, width=800, maxValue=20, minValue=2)
viz.savePng('sample_viz.png')
viz.saveSvg('sample_viz.svg')
viz
```

The code and sample data are provided in the example folder. The data contains 
annual snapshots of requirements of the [ChatterBots framework](https://github.com/gunthercox/ChatterBot) 
developed and maintained by Gunther Cox.

Running the above code creates this visualization:

![Sample Visualization](https://raw.githubusercontent.com/bumatic/PyCatFlow/main/example/sample_viz.svg)


## Credits & License

PyCatFlow was conceptualized by Marcus Burkhardt and implemented by Herbert Natta ([@herbertmn](https://github.com/herbertmn)). It is inspired by the Rankflow visualization tool develped by Bernhard Rieder. 

**Cite as:** Marcus Burkhardt, and Herbert Natta. 2021. “PyCatFlow: A Python Package for Visualizing Categorical Data over Time”. Zenodo. https://doi.org/10.5281/zenodo.5531785.

The package is released under MIT License.



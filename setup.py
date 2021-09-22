import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycatflow", 
    version="0.0.5",
    author="Marcus Burkhardt",
    author_email="marcus.burkhardt@gmail.com",
    description="A tool for visualizing categorical data over time.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bumatic/PyCatFlow",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=['drawSVG', 'matplotlib']
)

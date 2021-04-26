import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycatflow", # Replace with your own username
    version="0.0.1",
    author="Digital Methods Tool Lab",
    author_email="marcus.burkhardt@gmail.com",
    description="A visualization tool which allows the representation of temporal developments, based on categorical data.",
    long_description="PyCatFlow was conceptualized by Marcus Burkhardt and implemented by Herbert Natta (Email: herbert.natta@gmail.com, Github: @herbertmn). It is inspired by the Rankflow visualization tool develped by Bernhard Rieder.",
    long_description_content_type="text/markdown",
    url="https://github.com/bumatic/PyCatFlow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires = ['drawSVG', 'matplotlib']
)

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycatflow", # Replace with your own username
    version="0.0.1",
    author="herbertmn",
    author_email="herbert.natta@gmail.com",
    description="A visualization tool which allows the representation of temporal developments, based on on categorical data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/herbertmn/PyCatFlow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
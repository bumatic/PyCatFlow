import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycatflow",
    version="0.2.1",
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
    install_requires=['drawsvg>=2.0', 'matplotlib'],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.10.0',
            'flake8>=3.8.0',
            'black>=21.0.0',
            'build>=0.7.0',
            'twine>=3.4.0'
        ],
        'png': ['cairosvg>=2.3.0'],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=1.0.0'
        ]
    }
)

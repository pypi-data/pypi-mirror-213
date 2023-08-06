"""
    Project: Shinigami (https://github.com/shinigamilib/shinigami)
    Author: azazelm3dj3d (https://github.com/azazelm3dj3d)
    License: BSD 2-Clause
"""

import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "shinigami",
    version = "0.2.0",
    author = "azazelm3dj3d",
    description = "Shinigami is an open source Python library allowing the user to generate and build Dockerfiles during runtime",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules=['shinigami'],
    url = "https://github.com/shinigamilib/shinigami",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "argparse",
        "faye"
    ],
    entry_points={
        'console_scripts': ["shinigami=shinigami:CLI.run"]
    },
    python_requires = ">=3.6"
)

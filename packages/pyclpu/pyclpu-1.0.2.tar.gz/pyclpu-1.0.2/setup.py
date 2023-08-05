# -*- coding: utf-8 -*-
#! anaconda create -n CLPU python=3.5 && conda activate CLPU && pip install .
""" Setup for pythonic CLPU utilities

This module is the setup file for pythonic CLPU utilities.

| --------------- | ---------- |
| project         | standardized modules for often used python functions at CLPU |
| acronym         | pyCLPU |
| created         | 2023-05-31 20:11:00|
| @author         | Michael Ehret (MEmx), CLPU, Villamayor, Spain |
| @moderator      | Eduardo Flores, CLPU, Villamayor, Spain |
| @updator        | Diego de Luis (MEmx), CLPU, Villamayor, Spain |
| @contact        | tic@clpu.es |
| interpreter     | python 3.11.3 |
| version control | [git](https://git.clpu.es/mehret/pyclpu) |
| documentation   | [html](./html/pydoc/index.html) and [markdown](./md/pydoc/index.md) |
| --------------- | ---------- |

requires explicitely {
 - setuptools
 - glob
}

execute installation via {
  > pip install .
}

import without installation via {
  root = os.path.dirname(os.path.abspath(/path/to/pyclpu/MODULE.py))
  sys.path.append(os.path.abspath(root))
  import MODULE
  from importlib import reload 
  reload(MODULE)
}

"""

# credits to https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/

from setuptools import setup

import glob

# read the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(\
    name="pyclpu",\
    description='CLPU Utilities',\
    long_description = long_description,\
    long_description_content_type='text/markdown',\
    author='Michael Ehret',\
    author_email='mehret@clpu.es',\
    url='https://git.clpu.es/mehret/pyclpu',\
    license='MIT',\
    packages=['pyclpu'],
    scripts=glob.glob("pyclpu/*.py"),
    install_requires=[\
        'numpy','scipy','opencv-python','cython','pillow',\
        'matplotlib',\
    ],\
    # and build in modules cython, importlib.reload, inspect.getsourcefile, glob, math, opencv, pillow, os, sys, time
    classifiers=[\
        'Development Status :: 1 - Planning',\
        'Intended Audience :: Science/Research',\
        'Programming Language :: Python :: 3.11',\
    ],\
)
"""
pyclpu.

CLPU Utilities.
"""
# main attributes
__version__ = "1.0.2"
__author__ = 'Michael Ehret'
__credits__ = 'Centro de Laseres Pulsados, Villamayor, Spain'

"""
DEVELOPMENT ZONE

Until the following is not resolved, attributes below __init__.py require manual import as from pyclpu import ATTRIBUTE

# runtime
import os
import sys
import inspect

# make attributes in scripts known to users of `import pyclpu` that fall into this `__init__.py`
script_directory = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
import .image # relative import of content in image.py

"""
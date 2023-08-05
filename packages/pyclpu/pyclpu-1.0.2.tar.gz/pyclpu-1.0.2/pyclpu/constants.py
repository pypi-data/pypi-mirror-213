# -*- coding: utf-8 -*-
"""
This is the constants module. Please do only add but not delete content.

"""

# =============================================================================
# PYTHON HEADER
# =============================================================================
# EXTERNAL
import os
from inspect import getsourcefile

# EXTEND PATH
# ..

# INTERNAL
# ..

# RELOAD
# ..

# ==============================================================================
# DEFINE VARIABLES
# ==============================================================================
# prevent multiple calls
constants = True

# set up root_const for environment
root = os.path.dirname(os.path.abspath(getsourcefile(lambda:0)))

# set up standard namespace
# ..

# ==============================================================================
# DEFINE CONSTANTS
# ==============================================================================
# scales
inch_to_um = 25400.
inch_to_mm = 25.4
inch_to_m  = 0.0254

nm_to_m = 1.e-9

um_to_m = 1.e-6
um_to_mm = 1.e-3

mm_to_um = 1000.
mm_to_m = 1.e-3

cm_to_m = 0.01

m_to_um = 1000000.
m_to_mm = 1000.
m_to_cm = 100.

# physics in SI units
mu_0 = 1.256637062e-6                 # !! vacuum permeability
epsilon_0 = 8.85418781e-12            # !! vacuum permittivity
avogadro = 6.02214076e23              # !! Avogadro constant
m_e = 9.10938370e-31                  # !! electron mass
m_u = 1.660539066e-27                 # !! atomic mass unit
q_e = 1.602176634e-19                 # !! elementary charge
speed_of_light = 299792458            # !! speed of light in vacuum

# ==============================================================================
# DEFINE CALLS TO CONSTANTS' LIB
# ==============================================================================
# ..
"""
pyDIWASP: DIrectional WAve SPectrum analysis for Python

A Python conversion of the DIWASP package (Version 1.4) for directional wave spectrum analysis.

Main functions:
- dirspec: Main function for directional wave analysis
- infospec: Returns information about a directional spectrum
- plotspec: Plots DIWASP spectrums
- writespec: Writes DIWASP format spectrum files
- interpspec: Interpolates spectrum data

Copyright (C) 2002 Coastal Oceanography Group, CWR, UWA, Perth
License: GNU General Public License v3.0
"""

__version__ = "1.4.0"

from .dirspec import dirspec
from .infospec import infospec
from .plotspec import plotspec
from .writespec import writespec
from .interpspec import interpspec

__all__ = ['dirspec', 'infospec', 'plotspec', 'writespec', 'interpspec', '__version__']

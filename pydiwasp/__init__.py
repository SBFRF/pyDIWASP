"""
pyDIWASP - DIrectional WAve SPectrum analysis in Python

Python conversion of the DIWASP package (DIrectional WAve SPectrum analysis Version 1.4)

Main Functions:
- dirspec: Main directional wave spectrum estimation
- infospec: Calculate wave statistics from spectrum
- plotspec: Plot directional spectrum
- interpspec: Interpolate spectrum to different grid
- writespec: Write spectrum to file
"""

__version__ = "0.1.0"

# Import main API functions
from .dirspec import dirspec
from .infospec import infospec, compangle
from .plotspec import plotspec
from .interpspec import interpspec
from .writespec import writespec

__all__ = [
    'dirspec',
    'infospec',
    'compangle',
    'plotspec',
    'interpspec',
    'writespec',
]

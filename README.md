# pyDiwasp
conversion of diwasp package (DIWASP: DIrectional WAve SPectrum analysis Version 1.4) for python
converted from https://github.com/metocean/diwasp

I would LOVE help making this into better package of the original diwasp tool. Please check issues for needed functionality adds.

## Installation

### Install from source
```bash
git clone https://github.com/SBFRF/pyDIWASP.git
cd pyDIWASP
pip install .
```

### Install in development mode
```bash
git clone https://github.com/SBFRF/pyDIWASP.git
cd pyDIWASP
pip install -e .
```

### Build distribution packages
```bash
python setup.py sdist bdist_wheel
```

## Usage

After installation, you can import and use the main functions:

```python
from dirspec import dirspec
from infospec import infospec
from plotspec import plotspec
from writespec import writespec
from interpspec import interpspec

# Use the functions as described in the DIWASP documentation
# [SMout, EPout] = dirspec(ID, SM, EP, Options_)
```

## Toolbox contents:
### Main functions:
- dirspec.py           Main function for directional wave analysis
- infospec.py          Returns information about a directional spectrum
- interpspec.py        Interpolates between spectral matrix bases
- plotspec.py          Plots DIWASP spectrums
- writespec.py         Writes DIWASP format spectrum files

## Private functions (some can be used as stand alone functions):
### The transfer functions
- /private/elev.py
- /private/pres.py
- /private/velx.py
- /private/vely.py

### The estimation functions
- /private/IMLM.py
- /private/EMEP.py

### Miscellaneous functions
- /private/smoothspec.py
- /private/wavenumber.py
- /private/hsig.py
- /private/check_data.py
- /private/diwasp_csd.py
- /private/spectobasis.py
  

carying original license agreement and copyright

## License agreement
DIWASP, is free software; you can redistribute it and/or modify it under the terms of the 
GNU General Public License as published by the Free Software Foundation. 
However, the DIWASP license includes the following addendum concerning its usage:
This software and any derivatives of it shall only be used for educational purposes or 
scientific research without the intention of any financial gain. 
Use of this software or derivatives for any purpose that results in financial gain 
for a person or organization without written consent from the author is a breach of the license agreement.
This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
In addition the author is not liable in any way for consequences arising from the application of 
software output for any design or decision-making process.
The GNU General Public License forms the main part of the license agreement included in the package. 

Copyright (C) 2002 David Johnson   Coastal Oceanography Group, CWR, UWA, Perth


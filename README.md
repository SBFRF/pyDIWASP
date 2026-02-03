# pyDiwasp

[![CI](https://github.com/SBFRF/pyDIWASP/actions/workflows/ci.yml/badge.svg)](https://github.com/SBFRF/pyDIWASP/actions/workflows/ci.yml)

conversion of diwasp package (DIWASP: DIrectional WAve SPectrum analysis Version 1.4) for python
converted from https://github.com/metocean/diwasp

I would LOVE help making this into better package of the original diwasp tool. Please check issues for needed functionality adds.

## Installation

### From source
```bash
git clone https://github.com/SBFRF/pyDIWASP.git
cd pyDIWASP
pip install -r requirements.txt
```

### Requirements
- Python 3.8+
- NumPy >= 1.20.0, < 2.0
- SciPy >= 1.7.0, < 2.0
- Matplotlib >= 3.3.0, < 4.0

## Testing

The package includes a comprehensive test suite that documents the existing capabilities:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=. --cov-report=term
```

**Test Coverage:**
- 25 tests covering core functionality
- Core functions: wavenumber calculations, wave height calculations, data validation
- API functions: spectrum info, interpolation, file I/O
- Integration tests: full directional analysis workflow

## Toolbox contents:
### Main functions:
- dirspec.m           Main function for directional wave analysis
- readspec.m          Reads in DIWASP format spectrum files
- writespec.m         Writes DIWASP format spectrum files
- plotspec.m          Plots DIWASP spectrums
- testspec.m          Testing function for the estimation methods
- makespec.m          Makes a fake spectrum and generates fake data for testing dirspec.m
- infospec.m          Returns information about a directional spectrum
- data_structures.m   is a help file describing the new Version 1.1 data structures

## Private functions (some can be used as stand alone functions):
### The transfer functions
- /private/elev.m
- /private/pres.m
- /private/velx.m
- /private/vely.m
- /private/velz.m
- /private/slpx.m
- /private/slpy.m
- /private/vels.m
- /private/accs.m

### The estimation functions
- /private/DFTM.m
- /private/EMLM.m
- /private/IMLM.m
- /private/EMEP.m
- /private/BDM.m

### Miscellaneous functions
- /private/smoothspec.m
- /private/wavenumber.m
- /private/makerandomsea.m
- /private/makewavedata.m
- /private/Hsig.m
- /private/gsamp.m
- /private/check_data.m
  

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

## CI/CD Pipeline

This repository includes GitHub Actions workflows for:

### Continuous Integration (CI)
- Automated testing on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- Code linting with flake8
- Code coverage reporting
- Runs on all pull requests and pushes to main branches

### Deployment to PyPI
- Automated publishing to PyPI on release
- Manual deployment option via GitHub Actions
- Support for Test PyPI for pre-release testing

See [`.github/workflows/README.md`](.github/workflows/README.md) for more details on the CI/CD setup.


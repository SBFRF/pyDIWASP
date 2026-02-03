# pyDIWASP

Python conversion of the DIWASP package (DIrectional WAve SPectrum analysis Version 1.4)

pyDIWASP is a Python implementation of the DIWASP toolbox for estimating directional wave spectra from wave measurement data. It provides functions to analyze wave measurements from arrays of instruments (e.g., pressure sensors, current meters, wave gauges) and compute the directional distribution of wave energy.

Converted from: https://github.com/metocean/diwasp

## Features

- **Directional Wave Analysis**: Estimate directional wave spectra from instrument array data
- **Multiple Estimation Methods**: Supports IMLM and EMEP methods
- **Flexible Input**: Works with various instrument types (pressure, velocity, elevation sensors)
- **Visualization**: Built-in plotting functions for 3D and polar spectral plots
- **Wave Statistics**: Calculate significant wave height, peak period, and dominant direction

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/SBFRF/pyDIWASP.git
cd pyDIWASP

# Install the package
pip install -e .
```

### Requirements

- Python 3.8+
- NumPy
- SciPy
- Matplotlib

## Quick Start

```python
import numpy as np
from pydiwasp import dirspec

# Define instrument data structure
ID = {
    'layout': np.array([[0, 10, 20], [0, 0, 0], [0, 0, 0]]),  # x, y, z positions
    'datatypes': ['pres', 'pres', 'pres'],  # instrument types
    'depth': 10.0,  # water depth in meters
    'fs': 2.0,  # sampling frequency in Hz
    'data': wave_data  # nsamples x ninstruments array
}

# Define spectral matrix structure
SM = {
    'freqs': np.linspace(0.05, 0.5, 50),  # frequency bins in Hz
    'dirs': np.linspace(-np.pi, np.pi, 36)  # direction bins in radians
}

# Define estimation parameters
EP = {
    'method': 'IMLM',  # estimation method
    'iter': 100  # number of iterations
}

# Compute directional spectrum
SMout, EPout = dirspec(ID, SM, EP)
```

For more detailed examples, see the [example notebook](examples/pyDIWASP_example.ipynb).

## Main Functions

### dirspec.py
Main function for directional wave spectrum analysis.

**Usage:**
```python
SMout, EPout = dirspec(ID, SM, EP, Options)
```

**Parameters:**
- `ID`: Instrument data structure (dict)
- `SM`: Spectral matrix structure (dict)
- `EP`: Estimation parameters structure (dict)
- `Options`: Optional parameters (list of key-value pairs)

**Returns:**
- `SMout`: Output spectral matrix with computed directional spectrum
- `EPout`: Estimation parameters with actual values used

### infospec.py
Calculates and displays information about a directional spectrum.

**Returns:** Significant wave height (Hsig), peak period (Tp), direction of peak period (DTp), and dominant direction (Dp).

### plotspec.py
Plots the spectral matrix in 3D or polar form.

**Plot types:**
1. 3D surface plot
2. Polar plot
3. 3D surface plot (compass bearings)
4. Polar plot (compass bearings)

### writespec.py
Writes directional spectrum data to file in DIWASP format.

### interpspec.py
Interpolates a spectrum onto a different frequency/direction grid.

## Private Functions

The `private/` directory contains internal functions used by the main analysis routines:

### Transfer Functions
Calculate instrument response to waves:
- `elev.py` - Surface elevation transfer function
- `pres.py` - Pressure sensor transfer function
- `velx.py`, `vely.py` - Horizontal velocity transfer functions
- `wavenumber.py` - Dispersion relation solver

### Estimation Methods
Directional spectrum estimation algorithms:
- `IMLM.py` - Iterated Maximum Likelihood Method (default)
- `EMEP.py` - Extended Maximum Entropy Principle

### Utility Functions
- `smoothspec.py` - Spectral smoothing
- `hsig.py` - Significant wave height calculation
- `check_data.py` - Data structure validation
- `diwasp_csd.py` - Cross-spectral density estimation
- `spectobasis.py` - Spectral basis conversion

## Data Structures

### Instrument Data Structure (ID)
Dictionary with the following fields:
- `layout`: 3×N array of instrument positions [x; y; z] in meters
- `datatypes`: List of instrument types ('pres', 'elev', 'velx', 'vely', etc.)
- `depth`: Water depth in meters
- `fs`: Sampling frequency in Hz
- `data`: N_samples × N_instruments array of measurements

### Spectral Matrix Structure (SM)
Dictionary with the following fields:
- `freqs`: Array of frequency values
- `dirs`: Array of direction values (radians or degrees)
- `S`: Frequency × Direction array of spectral density (output only)
- `funit`: Frequency unit ('Hz' or 'rad/s')
- `dunit`: Direction unit ('rad' or 'deg')
- `xaxisdir`: Reference axis direction (default: 90 = East)

### Estimation Parameters Structure (EP)
Dictionary with the following fields:
- `method`: Estimation method ('IMLM' or 'EMEP')
- `nfft`: FFT length (auto-calculated if not specified)
- `dres`: Directional resolution (default: 180)
- `iter`: Number of iterations for iterative methods (default: 100)
- `smooth`: Spectral smoothing ('ON' or 'OFF', default: 'ON')

## Estimation Methods

### IMLM (Iterated Maximum Likelihood Method)
- **Default method**
- Iteratively refines directional spectrum estimate
- Good balance of accuracy and computational efficiency
- Recommended for most applications

### EMEP (Extended Maximum Entropy Principle)
- Based on maximum entropy principle
- Works well for narrow directional spreads
- Suitable for swell-dominated conditions

**Note:** The original DIWASP MATLAB toolbox includes additional methods (EMLM, DFTM, BDM) that are not yet implemented in this Python version. Contributions to add these methods are welcome!

## Examples

See the [examples directory](examples/) for Jupyter notebooks demonstrating:
- Basic directional spectrum estimation
- Working with different instrument configurations
- Comparing estimation methods
- Visualization options

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:
- Bug fixes
- Documentation improvements
- New features
- Additional examples

## References

All implemented calculation algorithms are described in:

Hashimoto, N. (1997). "Analysis of the directional wave spectrum from field data". 
In: *Advances in Coastal Engineering Vol. 3*. Ed: Liu, P.L-F. 
Pub: World Scientific, Singapore.

## Original Copyright and License
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


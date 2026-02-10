.. pyDIWASP documentation master file

pyDIWASP: Directional Wave Spectrum Analysis in Python
=======================================================

.. image:: https://img.shields.io/pypi/v/pyDIWASP.svg
   :target: https://pypi.org/project/pyDIWASP/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pyDIWASP.svg
   :target: https://pypi.org/project/pyDIWASP/
   :alt: Python versions

**pyDIWASP** is a Python implementation of the DIWASP (DIrectional WAve SPectrum) toolbox for estimating directional wave spectra from wave measurement data.

Key Features
------------

* **Directional Wave Analysis**: Estimate directional wave spectra from instrument array data
* **Multiple Estimation Methods**: Supports IMLM (Iterated Maximum Likelihood Method) and EMEP (Extended Maximum Entropy Principle)
* **Flexible Input**: Works with various instrument types (pressure, velocity, elevation sensors)
* **Visualization**: Built-in plotting functions for 3D and polar spectral plots
* **Wave Statistics**: Calculate significant wave height, peak period, and dominant direction

Quick Start
-----------

Installation::

    pip install pyDIWASP

Basic usage:

.. code-block:: python

    import numpy as np
    from pydiwasp import dirspec, infospec, plotspec
    
    # Define instrument data
    ID = {
        'layout': np.array([[0, 10, 20], [0, 0, 0], [0, 0, 0]]),
        'datatypes': ['pres', 'pres', 'pres'],
        'depth': 10.0,
        'fs': 2.0,
        'data': wave_data  # your measurement data
    }
    
    # Define spectral matrix
    SM = {
        'freqs': np.linspace(0.05, 0.5, 50),
        'dirs': np.linspace(-np.pi, np.pi, 36)
    }
    
    # Define estimation parameters
    EP = {'method': 'IMLM', 'iter': 100}
    
    # Compute directional spectrum
    SMout, EPout = dirspec(ID, SM, EP)
    
    # Display wave statistics
    Hsig, Tp, DTp, Dp = infospec(SMout)
    
    # Plot the spectrum
    plotspec(SMout, 1)

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   
   installation
   quickstart
   user_guide/index
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   
   api/index

.. toctree::
   :maxdepth: 1
   :caption: Developer Guide
   
   developer/contributing
   developer/structure

.. toctree::
   :maxdepth: 1
   :caption: Additional Information
   
   references
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

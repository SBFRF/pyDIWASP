Quick Start Guide
=================

This guide will get you started with pyDIWASP in just a few minutes.

What is Directional Wave Spectrum Analysis?
--------------------------------------------

A directional wave spectrum describes how wave energy is distributed across:

* **Frequencies** (or wave periods): Different wave oscillation rates
* **Directions**: Where waves are coming from

This is more informative than a simple frequency spectrum because it tells you not just how much energy exists at each frequency, but also the direction that energy is traveling.

Basic Workflow
--------------

The typical pyDIWASP workflow consists of three steps:

1. **Prepare data**: Define instrument array geometry and load measurements
2. **Compute spectrum**: Use ``dirspec()`` to estimate the directional spectrum
3. **Analyze results**: Use ``infospec()`` for statistics and ``plotspec()`` for visualization

Minimal Example
---------------

Here's a complete minimal example:

.. code-block:: python

    import numpy as np
    from pydiwasp import dirspec, infospec, plotspec
    
    # Step 1: Define instrument data
    ID = {
        'layout': np.array([
            [0, 10, 5],      # x positions (m)
            [0, 0, 8.66],    # y positions (m)  
            [0, 0, 0]        # z positions (m)
        ]),
        'datatypes': ['pres', 'pres', 'pres'],  # pressure sensors
        'depth': 10.0,     # water depth (m)
        'fs': 2.0,         # sampling frequency (Hz)
        'data': wave_data  # time series data (nsamples x 3)
    }
    
    # Step 2: Define output grid
    SM = {
        'freqs': np.linspace(0.05, 0.5, 50),  # frequencies (Hz)
        'dirs': np.linspace(-180, 180, 36)    # directions (degrees)
    }
    
    # Step 3: Set estimation parameters
    EP = {
        'method': 'IMLM',  # estimation method
        'iter': 100        # iterations
    }
    
    # Step 4: Compute spectrum
    SMout, EPout = dirspec(ID, SM, EP)
    
    # Step 5: Get wave statistics
    Hsig, Tp, DTp, Dp = infospec(SMout)
    
    # Step 6: Visualize
    plotspec(SMout, 1)  # 3D surface plot

Understanding the Data Structures
----------------------------------

Instrument Data (ID)
~~~~~~~~~~~~~~~~~~~~

The ``ID`` dictionary describes your instrument array:

* **layout**: 3×N array with x, y, z positions of N instruments
* **datatypes**: List specifying what each instrument measures
* **depth**: Water depth at the array location
* **fs**: Data sampling rate
* **data**: The actual time series measurements (nsamples × N)

Valid instrument types:

* ``'pres'``: Pressure sensor (most common)
* ``'elev'``: Surface elevation (e.g., wave staff)
* ``'velx'``, ``'vely'``: Horizontal velocities
* ``'vels'``: Horizontal velocity magnitude

Spectral Matrix (SM)
~~~~~~~~~~~~~~~~~~~~~

The ``SM`` dictionary defines the frequency-direction grid for the output:

* **freqs**: Array of frequencies where you want spectrum values
* **dirs**: Array of directions where you want spectrum values

After computation, ``SMout`` also contains:

* **S**: The computed spectral density (nfreqs × ndirs)

Estimation Parameters (EP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``EP`` dictionary controls the analysis:

* **method**: ``'IMLM'`` (default, recommended) or ``'EMEP'``
* **iter**: Number of iterations (default: 100)
* **nfft**: FFT length (auto-computed if omitted)
* **dres**: Directional resolution (default: 180)

Loading Your Data
-----------------

pyDIWASP works with NumPy arrays. Here's how to load data from common formats:

From CSV:

.. code-block:: python

    import numpy as np
    
    # Load from CSV file
    wave_data = np.loadtxt('wave_measurements.csv', delimiter=',')
    
    ID['data'] = wave_data

From MATLAB:

.. code-block:: python

    from scipy.io import loadmat
    
    # Load from .mat file
    mat_data = loadmat('wave_measurements.mat')
    wave_data = mat_data['wave_data']
    
    ID['data'] = wave_data

From netCDF:

.. code-block:: python

    import netCDF4 as nc
    
    # Load from netCDF file
    dataset = nc.Dataset('wave_measurements.nc')
    wave_data = dataset.variables['wave_data'][:]
    
    ID['data'] = wave_data

Next Steps
----------

* See :doc:`user_guide/index` for detailed information on all features
* Check :doc:`examples` for more complex use cases
* Read :doc:`api/index` for complete function documentation

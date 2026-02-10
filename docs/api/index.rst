API Reference
=============

This section provides detailed documentation for all public functions in pyDIWASP.

Main Functions
--------------

.. toctree::
   :maxdepth: 2
   
   dirspec
   infospec
   plotspec
   interpspec
   writespec

Utility Functions
-----------------

.. autofunction:: pydiwasp.infospec.compangle

Data Structures
---------------

pyDIWASP uses Python dictionaries to represent data structures. This section describes
the expected structure and fields for each type.

Instrument Data Structure (ID)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dictionary containing information about the instrument array and measurements.

**Required Fields:**

* ``layout`` : ndarray, shape (3, N)
    Instrument positions as [x; y; z] in meters. Each column represents one instrument.
    
* ``datatypes`` : list of str, length N
    Type of measurement for each instrument. Valid values: 'pres', 'elev', 'velx', 'vely', 'vels', 'accs'.
    
* ``depth`` : float
    Water depth in meters at the array location.
    
* ``fs`` : float
    Sampling frequency in Hz.
    
* ``data`` : ndarray, shape (nsamples, N)
    Time series measurements. Each column corresponds to one instrument.

**Example:**

.. code-block:: python

    ID = {
        'layout': np.array([[0, 10, 20], [0, 0, 0], [0, 0, 0]]),
        'datatypes': ['pres', 'pres', 'pres'],
        'depth': 10.0,
        'fs': 2.0,
        'data': measurements  # shape: (nsamples, 3)
    }

Spectral Matrix Structure (SM)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dictionary defining the frequency-direction grid for the spectrum.

**Required Fields (Input):**

* ``freqs`` : ndarray
    Frequency values for the output grid (Hz or rad/s).
    
* ``dirs`` : ndarray  
    Direction values for the output grid (radians or degrees).

**Optional Fields (Input):**

* ``funit`` : str, default 'Hz'
    Frequency units: 'Hz' or 'rad/s'.
    
* ``dunit`` : str, default 'rad'
    Direction units: 'rad' or 'deg'.
    
* ``xaxisdir`` : float, default 90
    Direction of positive x-axis in compass degrees (90 = East, 0 = North).

**Output Fields (Added by dirspec):**

* ``S`` : ndarray, shape (nfreqs, ndirs)
    Computed spectral density values.

**Example:**

.. code-block:: python

    # Input
    SM = {
        'freqs': np.linspace(0.05, 0.5, 50),
        'dirs': np.linspace(-180, 180, 36),
        'funit': 'Hz',
        'dunit': 'deg'
    }
    
    # After dirspec()
    SMout = {
        'freqs': ...,
        'dirs': ...,
        'S': ...  # shape (50, 36)
    }

Estimation Parameters Structure (EP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dictionary specifying parameters for the spectral estimation algorithm.

**Optional Fields (all have defaults):**

* ``method`` : str, default 'IMLM'
    Estimation method: 'IMLM' or 'EMEP'.
    
* ``nfft`` : int, default: auto-calculated
    FFT length for spectral estimation. Should be power of 2.
    
* ``dres`` : int, default 180
    Directional resolution (number of direction bins for internal calculation).
    
* ``iter`` : int, default 100
    Number of iterations for iterative methods.
    
* ``smooth`` : str, default 'ON'
    Spectral smoothing: 'ON' or 'OFF'.

**Example:**

.. code-block:: python

    # Use defaults
    EP = {}
    
    # Or specify parameters
    EP = {
        'method': 'IMLM',
        'iter': 100,
        'nfft': 512,
        'dres': 180,
        'smooth': 'ON'
    }

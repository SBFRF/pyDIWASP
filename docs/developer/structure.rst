Code Structure
==============

This document describes the organization of the pyDIWASP codebase.

Directory Structure
-------------------

::

    pyDIWASP/
    ├── pydiwasp/              # Main package directory
    │   ├── __init__.py        # Package initialization, public API
    │   ├── dirspec.py         # Main spectral estimation function
    │   ├── infospec.py        # Wave statistics calculation
    │   ├── plotspec.py        # Spectrum visualization
    │   ├── interpspec.py      # Spectrum interpolation
    │   ├── writespec.py       # File output
    │   └── private/           # Internal functions
    │       ├── __init__.py
    │       ├── IMLM.py        # IMLM estimation method
    │       ├── EMEP.py        # EMEP estimation method
    │       ├── wavenumber.py  # Dispersion relation
    │       ├── pres.py        # Pressure transfer function
    │       ├── elev.py        # Elevation transfer function
    │       ├── velx.py        # X-velocity transfer function
    │       ├── vely.py        # Y-velocity transfer function
    │       ├── vels.py        # Velocity magnitude transfer
    │       ├── accs.py        # Acceleration transfer
    │       ├── diwasp_csd.py  # Cross-spectral density
    │       ├── smoothspec.py  # Spectral smoothing
    │       ├── hsig.py        # Significant wave height
    │       ├── check_data.py  # Input validation
    │       └── spectobasis.py # Coordinate transformations
    ├── tests/                 # Test suite
    │   ├── test_api.py        # API tests
    │   ├── test_core.py       # Core functionality tests
    │   └── test_integration.py # Integration tests
    ├── examples/              # Example notebooks and scripts
    │   └── pyDIWASP_example.ipynb
    ├── docs/                  # Documentation
    │   ├── conf.py            # Sphinx configuration
    │   ├── index.rst          # Documentation index
    │   └── ...
    ├── setup.py               # Package setup script
    ├── pyproject.toml         # Modern Python package metadata
    ├── README.md              # Project README
    └── requirements.txt       # Dependencies

Module Overview
---------------

Public API (pydiwasp/)
~~~~~~~~~~~~~~~~~~~~~~

These modules form the user-facing API:

**dirspec.py**
    Main function for directional spectrum estimation. Orchestrates the entire
    analysis workflow:
    
    1. Validates input data structures
    2. Computes cross-spectral densities
    3. Calculates wavenumbers and transfer functions
    4. Calls the selected estimation method
    5. Interpolates to user-specified grid
    6. Optionally smooths and plots results

**infospec.py**
    Computes wave statistics from a directional spectrum:
    
    * Significant wave height (Hsig)
    * Peak period (Tp)
    * Direction at peak (DTp)
    * Dominant direction (Dp)
    
    Also includes ``compangle()`` for converting between angle conventions.

**plotspec.py**
    Creates visualizations of directional spectra:
    
    * 3D surface plots
    * Polar contour plots
    * Mathematical or nautical angle conventions

**interpspec.py**
    Interpolates spectra between different frequency-direction grids.
    Uses 2D interpolation in transformed coordinates to handle periodicity.

**writespec.py**
    Exports spectra to DIWASP text format for archiving or compatibility.

Private Modules (pydiwasp/private/)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These are internal implementation details, not part of the public API:

Estimation Methods
^^^^^^^^^^^^^^^^^^

**IMLM.py**
    Implements the Iterated Maximum Likelihood Method.
    
    * Iteratively refines directional estimate
    * Maximizes likelihood of observed cross-spectra
    * Good for complex, multi-modal distributions

**EMEP.py**
    Implements the Extended Maximum Entropy Principle.
    
    * Based on maximum entropy principle
    * Good for narrow directional spreads
    * Non-iterative formulation

Transfer Functions
^^^^^^^^^^^^^^^^^^

Each instrument type has a transfer function relating measurements to surface elevation:

**pres.py**
    Pressure sensor transfer function. Accounts for pressure attenuation with depth
    according to linear wave theory.

**elev.py**
    Surface elevation transfer function (identity, no transformation needed).

**velx.py, vely.py**
    Horizontal velocity transfer functions. Convert velocity measurements to
    equivalent surface elevation using linear wave theory.

**vels.py**
    Horizontal velocity magnitude transfer function.

**accs.py**
    Acceleration transfer function.

Core Utilities
^^^^^^^^^^^^^^

**wavenumber.py**
    Solves the dispersion relation to compute wave numbers from frequency and depth.
    Uses iterative method based on hyperbolic tangent.

**diwasp_csd.py**
    Computes cross-spectral density between two time series using Welch's method.

**smoothspec.py**
    Applies smoothing to directional spectra to reduce noise.

**hsig.py**
    Computes significant wave height from integrated spectrum energy.

**check_data.py**
    Validates input data structures (ID, SM, EP) and fills in default values.

**spectobasis.py**
    Handles coordinate system transformations for spectral interpolation.

Data Flow
---------

The typical data flow through pyDIWASP:

1. **User Input**:
   
   * ID (instrument data)
   * SM (spectral matrix grid)
   * EP (estimation parameters)

2. **dirspec() Main Function**:
   
   a. **Validation** (check_data.py):
      - Verify data structures
      - Fill in defaults
      
   b. **Preprocessing**:
      - Detrend data
      - Determine FFT parameters
      
   c. **Cross-Spectral Density** (diwasp_csd.py):
      - Compute CSD for all instrument pairs
      - Uses Welch's method with windowing
      
   d. **Wave Numbers** (wavenumber.py):
      - Compute k from frequency and depth
      - Uses dispersion relation
      
   e. **Transfer Functions** (pres.py, etc.):
      - Compute transfer matrix for each instrument
      - Accounts for instrument type and position
      
   f. **Estimation** (IMLM.py or EMEP.py):
      - Apply selected method
      - Estimate S(f, θ)
      
   g. **Interpolation** (interpspec.py):
      - Map to user-specified grid
      - Preserve energy
      
   h. **Post-processing**:
      - Optional smoothing (smoothspec.py)
      - Optional plotting (plotspec.py)
      - Optional file output (writespec.py)

3. **Output**:
   
   * SMout (spectrum with estimated S field)
   * EPout (parameters actually used)

Key Algorithms
--------------

Dispersion Relation (wavenumber.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Solves:

.. math::

   \\omega^2 = gk \\tanh(kh)

where ω is angular frequency, g is gravity, k is wavenumber, h is depth.

Uses Newton-Raphson iteration starting from an initial guess based on the
deep-water approximation.

Cross-Spectral Density (diwasp_csd.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Computes:

.. math::

   C_{ij}(f) = \\langle X_i(f) X_j^*(f) \\rangle

where X_i(f) is the Fourier transform of signal i, * denotes complex conjugate,
and ⟨⟩ denotes averaging over segments.

IMLM Algorithm (IMLM.py)
~~~~~~~~~~~~~~~~~~~~~~~~~

Iteratively updates the directional distribution:

.. math::

   E^{(n+1)}(\\theta) = E^{(n)}(\\theta) \\cdot f(E^{(n)})

where f depends on the comparison between observed and predicted cross-spectra.

Converges to maximum likelihood estimate.

Extension Points
----------------

Adding New Features
~~~~~~~~~~~~~~~~~~~

**New Instrument Type:**

1. Create transfer function in ``private/newtype.py``
2. Follow same signature as existing transfer functions
3. Add to valid datatypes in ``check_data.py``
4. Update documentation

**New Estimation Method:**

1. Create method in ``private/NEWMETHOD.py``
2. Follow same signature as IMLM.py
3. Method will be called via eval() in dirspec.py
4. Add tests and documentation

**New Output Format:**

1. Add function to main package or private/
2. Follow similar pattern to writespec.py
3. Document file format

Testing Strategy
----------------

The test suite uses pytest and is organized by scope:

**test_api.py**
    Tests the public API functions with various inputs. Ensures backward compatibility.

**test_core.py**
    Tests core algorithms and private functions. Verifies mathematical correctness.

**test_integration.py**
    End-to-end tests with realistic scenarios. Ensures components work together.

Run tests with::

    pytest tests/

For coverage report::

    pytest --cov=pydiwasp tests/

Dependencies
------------

Core Dependencies
~~~~~~~~~~~~~~~~~

* **NumPy**: Array operations, FFT
* **SciPy**: Interpolation, signal processing
* **Matplotlib**: Plotting

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

* **pytest**: Testing framework
* **pytest-cov**: Coverage reporting
* **flake8**: Code style checking
* **sphinx**: Documentation generation

Performance Considerations
--------------------------

Computational Bottlenecks
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Cross-spectral density computation**: O(N² × nfft × log(nfft))
   
   * Scales quadratically with number of instruments
   * Consider parallel computation for large arrays

2. **Estimation methods**: O(nfreqs × ndirs × iters)
   
   * IMLM: Linear in iterations
   * Most time in matrix operations

3. **Interpolation**: O(nfreqs_in × ndirs_in × log(npoints))
   
   * Uses scipy's griddata (QHull algorithm)

Memory Usage
~~~~~~~~~~~~

Main memory consumers:

* Cross-spectral matrix: N × N × nfreqs (complex)
* Transfer matrices: N × nfreqs × ndirs
* Wavenumber matrix: N × N × nfreqs × ndirs

For typical arrays (3-5 instruments), memory is not a concern.

Optimization Opportunities
~~~~~~~~~~~~~~~~~~~~~~~~~~

Potential improvements (contributions welcome):

* Parallel cross-spectral density computation
* Cython/Numba acceleration for IMLM inner loops
* Sparse matrix operations where applicable
* GPU acceleration for large arrays

Coding Conventions
------------------

* Variables follow MATLAB naming from original DIWASP for easier comparison
* Function names are lowercase with underscores
* Private functions start with underscore (though in private/ dir)
* Dictionary keys for data structures match MATLAB field names
* Comments explain *why*, not *what* (code should be self-documenting)

See Also
--------

* :doc:`contributing` for contribution guidelines
* Original DIWASP documentation for algorithm details
* Hashimoto (1997) for mathematical foundations

Troubleshooting
===============

This guide helps you diagnose and fix common problems when using pyDIWASP.

Installation Issues
-------------------

Module Not Found
~~~~~~~~~~~~~~~~

**Error**: ``ModuleNotFoundError: No module named 'pydiwasp'``

**Solutions**:

1. Verify installation::

    pip list | grep pyDIWASP

2. If not installed, install it::

    pip install -e .  # from source
    # or
    pip install pyDIWASP  # from PyPI

3. Check you're using the correct Python environment::

    which python
    python -c "import sys; print(sys.path)"

Dependency Issues
~~~~~~~~~~~~~~~~~

**Error**: Import errors for numpy, scipy, or matplotlib

**Solution**::

    pip install numpy scipy matplotlib

Data Structure Issues
---------------------

Invalid Data Structure
~~~~~~~~~~~~~~~~~~~~~~

**Error**: ``check_data`` warnings or errors

**Common causes**:

1. **Missing required fields**::

    # Wrong: missing 'datatypes'
    ID = {
        'layout': ...,
        'depth': 10.0,
        'fs': 2.0,
        'data': ...
    }
    
    # Correct:
    ID = {
        'layout': ...,
        'datatypes': ['pres', 'pres', 'pres'],
        'depth': 10.0,
        'fs': 2.0,
        'data': ...
    }

2. **Wrong array shapes**::

    # Wrong: layout should be (3, N) not (N, 3)
    layout = np.array([[0, 0, 0], [10, 0, 0], [20, 0, 0]])
    
    # Correct:
    layout = np.array([[0, 10, 20], [0, 0, 0], [0, 0, 0]])

3. **Mismatched dimensions**::

    # Wrong: 3 instruments but data has 4 columns
    ID['layout'] = np.array([[0, 10, 20], [0, 0, 0], [0, 0, 0]])
    ID['datatypes'] = ['pres', 'pres', 'pres']
    ID['data'] = np.random.randn(1000, 4)  # 4 columns!
    
    # Correct: match number of columns to number of instruments
    ID['data'] = np.random.randn(1000, 3)

Computation Issues
------------------

Data Length Too Small
~~~~~~~~~~~~~~~~~~~~~

**Error**: ``Data length of N too small``

**Cause**: The specified ``nfft`` is larger than the data length.

**Solutions**:

1. Reduce ``nfft``::

    EP = {
        'method': 'IMLM',
        'nfft': 256  # reduce from default
    }

2. Use longer data records (recommended)

3. Let pyDIWASP auto-calculate ``nfft`` (omit the parameter)

NaN or Inf Values
~~~~~~~~~~~~~~~~~

**Issue**: Spectrum contains NaN or infinite values

**Causes and solutions**:

1. **Constant or near-constant data**:
   - Check that your data contains actual wave variations
   - Remove DC offset if needed

2. **Very small variance**:
   - Check units of input data
   - Verify instruments are working

3. **Numerical instability**:
   - Try different estimation method
   - Reduce frequency range
   - Check array geometry

Poor Spectral Estimates
-----------------------

Unrealistic Peak Directions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue**: Estimated directions don't match expectations

**Checks**:

1. Verify array orientation:
   - Check that layout coordinates match actual positions
   - Verify x-axis direction (``xaxisdir``)

2. Check instrument order:
   - Ensure ``data`` columns match ``layout`` columns
   - Verify ``datatypes`` order matches instruments

3. Coordinate system:
   - Confirm mathematical vs. nautical conventions
   - Use ``compangle`` to convert between conventions

Missing Energy at High Frequencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue**: Spectrum shows little energy at high frequencies

**Causes**:

1. **Pressure sensor too deep**:
   - Pressure attenuates with depth
   - Solution: Use sensors closer to surface or use velocimeters

2. **Sampling rate too low**:
   - Check Nyquist criterion: fs > 2*fₘₐₓ
   - Solution: Increase sampling rate

3. **Natural wave conditions**:
   - May be realistic if no high-frequency waves present

Over-Smoothed Spectrum
~~~~~~~~~~~~~~~~~~~~~~~

**Issue**: Spectrum looks too smooth, missing details

**Solutions**:

1. Disable smoothing::

    EP = {'method': 'IMLM', 'smooth': 'OFF'}

2. Increase frequency resolution::

    SM = {
        'freqs': np.linspace(0.05, 0.5, 100),  # more points
        'dirs': np.linspace(-180, 180, 72)
    }

3. Try different estimation method (IMLM vs EMEP)

Noisy Spectrum
~~~~~~~~~~~~~~

**Issue**: Spectrum has many small spurious peaks

**Solutions**:

1. Enable smoothing::

    EP = {'method': 'IMLM', 'smooth': 'ON'}

2. Check data quality:
   - Remove spikes or outliers
   - Verify instrument calibration
   - Check for electronic noise

3. Reduce directional resolution::

    EP = {'dres': 90}  # coarser resolution

4. Average multiple spectra:
   - Compute spectra from overlapping windows
   - Average the results

Poor Directional Resolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue**: Cannot distinguish between nearby directions

**Causes**:

1. **Array too small**:
   - Aperture limits resolution
   - Solution: Use larger array if possible

2. **Insufficient angular resolution**:
   - Increase ``dres``::
   
       EP = {'dres': 360}

3. **Waves too short relative to array**:
   - Array spacing must be appropriate for wavelength
   - Solution: Adjust focus to lower frequencies

Interpolation Warnings
~~~~~~~~~~~~~~~~~~~~~~

**Warning**: ``User defined grid may be too coarse``

**Cause**: The output grid cannot adequately represent the spectrum without 
significant loss of energy.

**Solutions**:

1. Increase frequency resolution::

    SM = {
        'freqs': np.linspace(0.05, 0.5, 100),  # more points
        'dirs': ...
    }

2. Increase directional resolution::

    SM = {
        'freqs': ...,
        'dirs': np.linspace(-180, 180, 72)  # more points
    }

3. If the warning persists but Hsig error is small (<2%), it may be acceptable

Visualization Issues
--------------------

Plot Appears Empty
~~~~~~~~~~~~~~~~~~

**Issue**: ``plotspec`` creates figure but shows no data

**Checks**:

1. Verify spectrum was computed::

    print(SMout['S'].shape)
    print(np.max(SMout['S']))

2. Check for NaN values::

    print(np.sum(np.isnan(SMout['S'])))

3. Ensure matplotlib backend is working::

    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3])
    plt.show()  # should display a simple plot

Wrong Direction Convention
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Issue**: Directions appear rotated or flipped

**Solution**: Adjust ``xaxisdir`` and use correct plot type:

.. code-block:: python

    # For mathematical angles
    plotspec(SMout, 1)  # or 2
    
    # For compass bearings
    plotspec(SMout, 3)  # or 4
    
    # Adjust x-axis direction if needed
    SMout['xaxisdir'] = 90  # for East = 0° in math coordinates

Performance Issues
------------------

Slow Computation
~~~~~~~~~~~~~~~~

**Issue**: Analysis takes too long

**Solutions**:

1. Reduce number of iterations::

    EP = {'iter': 50}  # instead of 100

2. Reduce directional resolution::

    EP = {'dres': 90}  # instead of 180

3. Reduce number of frequencies::

    SM = {
        'freqs': np.linspace(0.05, 0.5, 25),  # fewer points
        ...
    }

4. Use EMEP instead of IMLM (faster but different results)

5. Process fewer instruments (if some are redundant)

Memory Errors
~~~~~~~~~~~~~

**Issue**: Out of memory errors

**Solutions**:

1. Reduce ``nfft``::

    EP = {'nfft': 256}

2. Process data in segments

3. Reduce number of directions::

    EP = {'dres': 90}

Diagnostic Checklist
--------------------

When encountering problems, work through this checklist:

Input Data
~~~~~~~~~~

- [ ] Check data shape: ``print(ID['data'].shape)``
- [ ] Verify no NaN: ``print(np.sum(np.isnan(ID['data'])))``
- [ ] Check data range: ``print(np.min(ID['data']), np.max(ID['data']))``
- [ ] Verify variance: ``print(np.var(ID['data'], axis=0))``

Array Configuration
~~~~~~~~~~~~~~~~~~~

- [ ] Check layout shape: ``print(ID['layout'].shape)`` → should be (3, N)
- [ ] Verify datatypes length: ``print(len(ID['datatypes']))`` → should match N
- [ ] Check spacing: instruments too close or too far?
- [ ] Verify depth: reasonable for your location?

Parameters
~~~~~~~~~~

- [ ] Frequency range: appropriate for your waves?
- [ ] Direction range: covers all possible directions?
- [ ] Sampling frequency: satisfies Nyquist?
- [ ] Record length: sufficient for lowest frequency?

Output
~~~~~~

- [ ] Check spectrum shape: ``print(SMout['S'].shape)``
- [ ] Verify no NaN: ``print(np.sum(np.isnan(SMout['S'])))``
- [ ] Check energy: ``print(np.max(SMout['S']))`` → should be > 0
- [ ] Compare Hsig: does it match expectations?

Getting Help
------------

If you're still stuck:

1. **Check examples**: See the example notebook for working code

2. **Review documentation**: Ensure you're using the API correctly

3. **Search issues**: Check GitHub issues for similar problems

4. **Create an issue**: If you've found a bug, report it on GitHub with:
   - Minimal reproducible example
   - Error message (full traceback)
   - System info (Python version, OS, package versions)

5. **Contact maintainers**: See CONTRIBUTING.md for contact information

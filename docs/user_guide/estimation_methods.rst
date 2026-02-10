Estimation Methods
==================

pyDIWASP implements two methods for estimating directional wave spectra from
instrument array measurements. This guide explains when to use each method.

Available Methods
-----------------

IMLM: Iterated Maximum Likelihood Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Default and recommended method for most applications.**

The IMLM method iteratively refines the directional spectrum estimate to maximize
the likelihood that the observed cross-spectra would result from the estimated
directional spectrum.

**Characteristics:**

* Good balance of accuracy and computational efficiency
* Handles multi-modal directional distributions well
* Robust to noise
* Recommended for general ocean wave conditions

**Usage:**

.. code-block:: python

    EP = {
        'method': 'IMLM',
        'iter': 100  # number of iterations
    }
    
    SMout, EPout = dirspec(ID, SM, EP)

**Parameters:**

* ``iter``: Number of iterations (default: 100)
  - More iterations → better convergence but slower computation
  - 50-200 iterations is typical
  - Monitor convergence by checking if results stabilize

EMEP: Extended Maximum Entropy Principle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The EMEP method is based on the principle of maximum entropy. It finds the directional
spectrum that is "smoothest" (maximum entropy) while still consistent with the
measurements.

**Characteristics:**

* Works well for narrow directional spreads
* Good for swell-dominated conditions
* May over-smooth in complex sea states
* Faster than IMLM (non-iterative in original form)

**Usage:**

.. code-block:: python

    EP = {
        'method': 'EMEP',
        'iter': 100  # still used for consistency
    }
    
    SMout, EPout = dirspec(ID, SM, EP)

**Best For:**

* Long-period swell with narrow directional spread
* Conditions with dominant single wave direction
* Quick preliminary analyses

Comparing Methods
-----------------

The choice between methods depends on your wave conditions:

Wind Waves (Complex, Multi-Directional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Preferred**: IMLM
* **Reason**: Better handles multiple wave components from different directions

Swell (Long-Period, Narrow Spread)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Preferred**: EMEP or IMLM (both work well)
* **Reason**: EMEP's entropy principle matches the physics of narrow-spread swell

Mixed Seas (Wind Waves + Swell)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Preferred**: IMLM
* **Reason**: Better separation of multiple wave systems

Example Comparison
------------------

.. code-block:: python

    import numpy as np
    from pydiwasp import dirspec, infospec, plotspec
    import matplotlib.pyplot as plt
    
    # Same data, same grid
    ID = {...}  # your instrument data
    SM = {...}  # your spectral grid
    
    # IMLM estimation
    EP_imlm = {'method': 'IMLM', 'iter': 100}
    SM_imlm, EP_imlm_out = dirspec(ID, SM, EP_imlm, ['PLOTTYPE', 0])
    
    # EMEP estimation
    EP_emep = {'method': 'EMEP', 'iter': 100}
    SM_emep, EP_emep_out = dirspec(ID, SM, EP_emep, ['PLOTTYPE', 0])
    
    # Compare visually
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    plt.subplot(121)
    plotspec(SM_imlm, 1)
    plt.title('IMLM Method')
    
    plt.subplot(122)
    plotspec(SM_emep, 1)
    plt.title('EMEP Method')
    
    plt.tight_layout()
    plt.show()
    
    # Compare statistics
    print("IMLM:")
    H_imlm, Tp_imlm, DTp_imlm, Dp_imlm = infospec(SM_imlm)
    
    print("\\nEMEP:")
    H_emep, Tp_emep, DTp_emep, Dp_emep = infospec(SM_emep)

Other Parameters
----------------

Beyond the method choice, several other parameters affect the estimation:

Directional Resolution (dres)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Controls the number of directions used in internal calculations:

.. code-block:: python

    EP = {
        'method': 'IMLM',
        'dres': 180  # default
    }

* Higher ``dres`` → finer directional resolution but slower computation
* Typical range: 36-360
* Default (180) works well for most cases

FFT Length (nfft)
~~~~~~~~~~~~~~~~~

Controls frequency resolution:

.. code-block:: python

    EP = {
        'method': 'IMLM',
        'nfft': 512  # auto-calculated if omitted
    }

* Must be power of 2 (256, 512, 1024, ...)
* Larger ``nfft`` → finer frequency resolution
* Auto-calculation usually optimal
* Constrained by data length: nfft ≤ length of data

Spectral Smoothing (smooth)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Controls whether to apply spectral smoothing:

.. code-block:: python

    EP = {
        'method': 'IMLM',
        'smooth': 'ON'  # default
    }

* ``'ON'``: Applies smoothing (recommended for noisy data)
* ``'OFF'``: No smoothing (use if data is already clean)

Smoothing reduces noise but may blur sharp features.

Number of Iterations (iter)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For IMLM, controls how many refinement iterations to perform:

.. code-block:: python

    EP = {
        'method': 'IMLM',
        'iter': 100  # default
    }

* More iterations generally improve accuracy
* Returns diminish after ~50-100 iterations
* Check convergence if concerned about accuracy

Performance Considerations
--------------------------

Computational Cost
~~~~~~~~~~~~~~~~~~

Typical computation times (3 sensors, 50 frequencies, 36 directions):

* IMLM with 100 iterations: ~2-5 seconds
* EMEP: ~1-3 seconds

Factors affecting speed:

* Number of instruments: O(N²) scaling
* Number of frequencies: Linear scaling  
* Number of directions: Linear scaling
* Number of iterations (IMLM only): Linear scaling

Memory Usage
~~~~~~~~~~~~

Memory requirements scale with:

* Number of cross-spectral pairs: N×N×nfreqs
* Directional resolution: O(dres)

For typical arrays (3-10 sensors), memory is not usually a concern.

Validation and Quality Control
-------------------------------

After computing a spectrum, always:

1. **Visual inspection**: Plot the spectrum and check if it looks physically reasonable

2. **Check statistics**: Verify Hsig, Tp match expectations

3. **Compare methods**: If results differ significantly between IMLM and EMEP, 
   investigate your data quality

4. **Energy conservation**: The integrated spectrum should match the variance of 
   measurements

5. **Frequency limits**: Check that spectral energy is concentrated in expected 
   frequency range

When Results Are Poor
~~~~~~~~~~~~~~~~~~~~~

If estimated spectra look unrealistic:

* Check array geometry (spacing, configuration)
* Verify instrument synchronization
* Inspect raw data for quality issues
* Try different frequency/direction grids
* Adjust smoothing or iteration count

See Also
--------

* :doc:`understanding_spectra` for background on directional spectra
* :doc:`instrument_types` for array design considerations
* :doc:`troubleshooting` for debugging problems

References
----------

Hashimoto, N. (1997). "Analysis of the directional wave spectrum from field data".
In: Advances in Coastal Engineering Vol. 3. Ed: Liu, P.L-F.
Pub: World Scientific, Singapore.

This reference describes the mathematical basis for both IMLM and EMEP methods.

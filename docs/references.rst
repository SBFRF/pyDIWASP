References
==========

This page lists key references for pyDIWASP and directional wave spectrum analysis.

Primary Reference
-----------------

The estimation algorithms implemented in pyDIWASP are described in:

    Hashimoto, N. (1997). "Analysis of the directional wave spectrum from field data".
    In: *Advances in Coastal Engineering Vol. 3*. Ed: Liu, P.L-F.
    Pub: World Scientific, Singapore.

This comprehensive chapter covers:

* Theoretical foundations of directional spectrum estimation
* Description of multiple estimation methods (MLM, IMLM, EMLM, EMEP, BDM, DFTM)
* Array design considerations
* Validation and comparison studies

Wave Theory
-----------

Linear Wave Theory
~~~~~~~~~~~~~~~~~~

Dean, R. G., & Dalrymple, R. A. (1991). *Water wave mechanics for engineers and scientists*.
World Scientific.

Comprehensive treatment of linear wave theory, dispersion relations, and wave kinematics.

Mei, C. C., Stiassnie, M., & Yue, D. K. P. (2005). *Theory and applications of ocean surface waves*.
World Scientific.

Advanced treatment of water wave theory including directional spectra.

Directional Spectra
-------------------

Theoretical Background
~~~~~~~~~~~~~~~~~~~~~~

Longuet-Higgins, M. S., Cartwright, D. E., & Smith, N. D. (1963). 
"Observations of the directional spectrum of sea waves using the motions of a floating buoy". 
In: *Ocean Wave Spectra*, Prentice-Hall, 111-136.

Early foundational work on estimating directional spectra from buoy measurements.

Capon, J. (1969). "High-resolution frequency-wavenumber spectrum analysis". 
*Proceedings of the IEEE*, 57(8), 1408-1418.

Introduction of Maximum Likelihood Method for spectral estimation.

Maximum Entropy Methods
~~~~~~~~~~~~~~~~~~~~~~~~

Lygre, A., & Krogstad, H. E. (1986). 
"Maximum entropy estimation of the directional distribution in ocean wave spectra". 
*Journal of Physical Oceanography*, 16(12), 2052-2060.

Development of the Maximum Entropy Principle for directional wave estimation.

Estimation Methods Comparison
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Benoit, M., Frigaard, P., & Schäffer, H. A. (1997).
"Analyzing multidirectional wave spectra: a tentative classification of available methods".
In: *IAHR seminar multidirectional waves and their interaction with structures*.

Comprehensive comparison of various directional spectrum estimation methods.

Array Design
------------

Barber, N. F., & Ursell, F. (1948).
"The generation and propagation of ocean waves and swell".
*Philosophical Transactions of the Royal Society of London. Series A*, 240(824), 527-560.

Early work on array-based wave measurement.

Krogstad, H. E. (1988).
"Maximum likelihood estimation of ocean wave spectra from general arrays of wave gauges".
*Modeling, Identification and Control*, 9(2), 81-97.

Theory for array design and optimal sensor placement.

Applications
------------

Coastal Engineering
~~~~~~~~~~~~~~~~~~~

Goda, Y. (2010). *Random seas and design of maritime structures* (3rd ed.).
World Scientific.

Application of directional wave spectra in coastal structure design.

Wave Modeling
~~~~~~~~~~~~~

Komen, G. J., Cavaleri, L., Donelan, M., Hasselmann, K., Hasselmann, S., & Janssen, P. A. E. M. (1994).
*Dynamics and modelling of ocean waves*. Cambridge University Press.

Use of directional spectra in numerical wave models.

DIWASP Software
---------------

Original MATLAB Version
~~~~~~~~~~~~~~~~~~~~~~~

Johnson, D. (2002). *DIWASP, a directional wave spectrum analysis package*.
Research Report WP-1601-DJ, Centre for Water Research, University of Western Australia.

Documentation for the original MATLAB implementation that pyDIWASP is based on.

Available at: https://github.com/metocean/diwasp

Standards and Guidelines
------------------------

Measurement Standards
~~~~~~~~~~~~~~~~~~~~~

ISO 19901-1:2015. *Petroleum and natural gas industries — Specific requirements for offshore structures — Part 1: Metocean design and operating considerations*.

Includes guidelines for wave measurement and spectrum estimation.

IAHR (1989). *List of sea-state parameters*.
Journal of Waterway, Port, Coastal, and Ocean Engineering, 115(6), 793-808.

Standardized definitions of wave parameters.

Related Software
----------------

Python Wave Analysis
~~~~~~~~~~~~~~~~~~~~

* **WAVEWATCH III**: Spectral wave model (FORTRAN, with Python interfaces)
* **SWAN**: Simulating WAves Nearshore model
* **oceanwaves**: Python package for wave data analysis
* **wafo**: Wave Analysis for Fatigue and Oceanography (Python port of MATLAB toolbox)

MATLAB Tools
~~~~~~~~~~~~

* **DIWASP**: Original MATLAB version
* **WAFO**: Wave Analysis for Fatigue and Oceanography
* **CDIP toolbox**: Coastal Data Information Program tools

Historical Context
------------------

The field of directional wave spectrum estimation has evolved significantly since the 1950s:

* **1940s-1950s**: Initial theoretical work (Barber & Ursell, Longuet-Higgins)
* **1960s-1970s**: Development of estimation methods (Capon, Oltman-Shay)
* **1980s**: Maximum Entropy methods (Lygre & Krogstad)
* **1990s**: Iterative methods (IMLM), comparison studies
* **2000s**: Software packages (DIWASP), operational systems
* **2010s**: Advanced methods, machine learning approaches

Online Resources
----------------

Organizations and Data
~~~~~~~~~~~~~~~~~~~~~~

* **CDIP** (Coastal Data Information Program): https://cdip.ucsd.edu/
  
  Provides wave data and analysis tools

* **NDBC** (National Data Buoy Center): https://www.ndbc.noaa.gov/
  
  Real-time wave measurements from buoys

* **Copernicus Marine Service**: https://marine.copernicus.eu/
  
  European wave forecasts and reanalysis

* **WAVEWATCH III**: https://github.com/NOAA-EMC/WW3
  
  Global wave model

Educational Resources
~~~~~~~~~~~~~~~~~~~~~

* **Coastal Engineering Manual**: https://www.publications.usace.army.mil/USACE-Publications/Engineer-Manuals/
  
  Comprehensive coastal engineering reference

* **Ocean Wave Spectra**: Prentice-Hall symposium proceedings (1963)
  
  Classic collection of papers on wave spectra

Software Documentation
~~~~~~~~~~~~~~~~~~~~~~

* **NumPy**: https://numpy.org/doc/
* **SciPy**: https://docs.scipy.org/
* **Matplotlib**: https://matplotlib.org/stable/contents.html

Citation
--------

If you use pyDIWASP in your research, please cite both pyDIWASP and the original DIWASP:

**pyDIWASP**::

    SBFRF. (2024). pyDIWASP: Directional Wave Spectrum Analysis in Python.
    GitHub repository: https://github.com/SBFRF/pyDIWASP

**Original DIWASP**::

    Johnson, D. (2002). DIWASP, a directional wave spectrum analysis package.
    Research Report WP-1601-DJ, Centre for Water Research, University of Western Australia.

**Algorithms**::

    Hashimoto, N. (1997). Analysis of the directional wave spectrum from field data.
    In: Advances in Coastal Engineering Vol. 3. Ed: Liu, P.L-F.
    World Scientific, Singapore.

Contact and Support
-------------------

* **GitHub Issues**: https://github.com/SBFRF/pyDIWASP/issues
* **Email**: support@sbfrf.org
* **Documentation**: https://pydiwasp.readthedocs.io/ (when published)

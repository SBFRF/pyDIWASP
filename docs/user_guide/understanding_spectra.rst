Understanding Directional Wave Spectra
=======================================

This section explains the concepts behind directional wave spectrum analysis.

What is a Wave Spectrum?
-------------------------

A wave spectrum describes how wave energy is distributed across different frequencies.
In nature, ocean waves are not simple sinusoids but a superposition of many different
wave components with different frequencies, amplitudes, and phases.

A **frequency spectrum** S(f) shows the distribution of wave energy as a function of 
frequency f. The units are typically m²/Hz or m²s (energy per unit frequency).

Why Directional Spectra?
-------------------------

While a frequency spectrum tells you *how much* energy exists at each frequency, it
doesn't tell you *where* that energy is coming from. Ocean waves can arrive from
multiple directions simultaneously:

* Locally generated wind waves from one direction
* Swell from distant storms from another direction
* Reflected waves from coastlines or structures

A **directional spectrum** S(f, θ) extends the frequency spectrum to include direction θ.
It shows the distribution of wave energy as a function of both frequency and direction.

Mathematical Definition
-----------------------

The directional spectrum S(f, θ) satisfies:

.. math::

   \\int_{f_1}^{f_2} \\int_{\\theta_1}^{\\theta_2} S(f, \\theta) \\, d\\theta \\, df
   
This integral gives the energy in the frequency band [f₁, f₂] coming from the 
directional sector [θ₁, θ₂].

The frequency spectrum (1D) can be recovered by integrating over all directions:

.. math::

   S(f) = \\int_{-\\pi}^{\\pi} S(f, \\theta) \\, d\\theta

Key Wave Parameters
--------------------

From the directional spectrum, we can compute important wave statistics:

Significant Wave Height (Hₛᵢ��)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The significant wave height is defined as:

.. math::

   H_{sig} = 4\\sqrt{m_0}
   
where m₀ is the zeroth moment (total energy):

.. math::

   m_0 = \\int_{0}^{\\infty} \\int_{-\\pi}^{\\pi} S(f, \\theta) \\, d\\theta \\, df

Hₛᵢ𝗀 approximates the average height of the highest one-third of waves.

Peak Period (Tₚ)
~~~~~~~~~~~~~~~~~

The peak period is the period (reciprocal of frequency) at which the frequency 
spectrum has its maximum:

.. math::

   T_p = 1/f_p, \\quad \\text{where} \\quad f_p = \\arg\\max_f S(f)

Dominant Direction (Dₚ)
~~~~~~~~~~~~~~~~~~~~~~~~

The dominant direction is the direction from which the most energy arrives,
integrated over all frequencies:

.. math::

   D_p = \\arg\\max_{\\theta} \\int_{0}^{\\infty} S(f, \\theta) \\, df

Direction at Peak (DTₚ)
~~~~~~~~~~~~~~~~~~~~~~~~

The direction at the spectral peak is the direction θ at the point (fₚ, θ) where
the 2D spectrum has its maximum value:

.. math::

   DT_p = \\arg\\max_{\\theta} S(f_p, \\theta)

Directional Conventions
-----------------------

Directions in oceanography can be specified in different ways:

Mathematical Convention
~~~~~~~~~~~~~~~~~~~~~~~

* Measured counter-clockwise from the positive x-axis
* Range: -180° to +180° or 0° to 360°
* Used in most mathematical and computational contexts

Nautical/Oceanographic Convention  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Measured clockwise from North
* Called "compass bearing" or "azimuth"
* Range: 0° to 360° (North = 0°, East = 90°, South = 180°, West = 270°)

Direction To vs. Direction From
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Direction to**: Direction waves are traveling toward (mathematical convention)
* **Direction from**: Direction waves are coming from (oceanographic convention)
* These differ by 180°

pyDIWASP can work with either convention using the ``xaxisdir`` parameter in the
spectral matrix structure.

Array-Based Estimation
----------------------

pyDIWASP estimates directional spectra from measurements by an array of instruments.
The basic principle is:

1. Measure waves at multiple spatial locations simultaneously
2. Compute cross-spectral densities between all instrument pairs
3. The phase relationships between instruments contain directional information
4. Apply an estimation algorithm (IMLM or EMEP) to reconstruct S(f, θ)

The array geometry is critical:

* **Aperture**: The array size determines the shortest wavelength (highest frequency) 
  that can be resolved
* **Spacing**: Instrument spacing should be less than half the shortest wavelength 
  of interest
* **Configuration**: Triangular or cross arrays work well; linear arrays have 
  directional ambiguity

For more details on array design, see the original DIWASP manual or Hashimoto (1997).

Applications
------------

Directional wave spectra are used in:

* **Coastal engineering**: Design of breakwaters, jetties, and coastal structures
* **Ship design**: Assessing vessel performance in different sea states
* **Wave modeling**: Validation of numerical wave models
* **Renewable energy**: Optimizing wave energy converter designs
* **Ocean forecasting**: Understanding wave climate and extremes

References
----------

Hashimoto, N. (1997). "Analysis of the directional wave spectrum from field data".
In: Advances in Coastal Engineering Vol. 3. Ed: Liu, P.L-F.
Pub: World Scientific, Singapore.

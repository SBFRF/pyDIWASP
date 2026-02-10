Working with Different Instrument Types
========================================

pyDIWASP supports various types of wave measurement instruments. This guide explains
how to configure your instrument array for each type.

Supported Instrument Types
---------------------------

pyDIWASP supports the following instrument types (specified in the ``datatypes`` field):

* ``'pres'``: Pressure sensors
* ``'elev'``: Surface elevation (e.g., wave staff, laser, ultrasonic)
* ``'velx'``: Horizontal velocity in x-direction
* ``'vely'``: Horizontal velocity in y-direction
* ``'vels'``: Horizontal velocity magnitude
* ``'accs'``: Acceleration (vertical)

Each type has a different transfer function relating the measurement to surface elevation.

Pressure Sensors
----------------

Pressure sensors are the most commonly used instruments for directional wave analysis.

**Principle:**

Pressure sensors measure the pressure variation due to passing waves. The relationship
between surface elevation and pressure depends on water depth and wave frequency due
to pressure attenuation with depth.

**Configuration:**

.. code-block:: python

    ID = {
        'layout': np.array([
            [0, 10, 5],      # x positions
            [0, 0, 8.66],    # y positions
            [0, 0, 0]        # z positions (seabed = 0)
        ]),
        'datatypes': ['pres', 'pres', 'pres'],
        'depth': 10.0,       # water depth
        'fs': 2.0,
        'data': pressure_data  # in Pascals or meters of water
    }

**Considerations:**

* Pressure attenuation limits the maximum frequency that can be resolved
* In shallow water (depth/wavelength < 0.5), attenuation is minimal
* In deep water, high-frequency waves may not be detectable near the bottom
* Rule of thumb: kh > 1 for good measurement (k = wavenumber, h = depth)

**Frequency Limits:**

For depth h and frequency f, the pressure attenuation factor is:

.. math::

   A(f, h) = \\frac{\\cosh(kh)}{\\cosh(k(h-z))}
   
where z is the sensor elevation (z=0 at seabed). As A approaches zero, the signal
becomes too weak.

Surface Elevation Sensors
--------------------------

Surface elevation sensors directly measure the water surface position.

**Types:**

* Resistance wave staffs
* Capacitance wave staffs  
* Ultrasonic sensors (downward-looking)
* Radar sensors
* Laser sensors

**Configuration:**

.. code-block:: python

    ID = {
        'layout': np.array([
            [0, 10, 5],      # x positions
            [0, 0, 8.66],    # y positions
            [0, 0, 0]        # z positions (not critical for elevation)
        ]),
        'datatypes': ['elev', 'elev', 'elev'],
        'depth': 10.0,
        'fs': 2.0,
        'data': elevation_data  # in meters
    }

**Considerations:**

* No frequency-dependent attenuation (ideal for all frequencies)
* Wave staffs work in shallow to moderate depths
* Ultrasonic/radar sensors may have limitations in extreme wave conditions
* Best for laboratory or nearshore applications

Velocity Sensors
----------------

Velocity sensors (e.g., Acoustic Doppler Velocimeters, ADVs) measure water particle
velocity.

**Configuration (separate x, y components):**

.. code-block:: python

    ID = {
        'layout': np.array([
            [0, 0, 10, 10],     # x positions
            [0, 0, 0, 0],       # y positions
            [-2, -2, -2, -2]    # z positions (depth below surface)
        ]),
        'datatypes': ['velx', 'vely', 'velx', 'vely'],
        'depth': 10.0,
        'fs': 2.0,
        'data': velocity_data  # in m/s
    }

**Configuration (velocity magnitude):**

.. code-block:: python

    ID = {
        'layout': np.array([
            [0, 10, 5],
            [0, 0, 8.66],
            [-2, -2, -2]
        ]),
        'datatypes': ['vels', 'vels', 'vels'],
        'depth': 10.0,
        'fs': 2.0,
        'data': velocity_magnitude_data
    }

**Considerations:**

* Velocity measurements also have depth-dependent attenuation
* Horizontal velocities attenuate less rapidly than pressure
* ADVs work well in moderate-depth applications
* The measurement volume should be small compared to wavelength

Mixed Arrays
------------

You can combine different instrument types in the same array:

.. code-block:: python

    ID = {
        'layout': np.array([
            [0, 10, 20, 30],
            [0, 0, 0, 0],
            [0, 0, -1, -1]
        ]),
        'datatypes': ['pres', 'pres', 'velx', 'vely'],
        'depth': 15.0,
        'fs': 2.0,
        'data': mixed_data
    }

This allows you to leverage the strengths of different sensor types.

Array Geometry Guidelines
--------------------------

Regardless of instrument type, follow these guidelines for array design:

Minimum Requirements
~~~~~~~~~~~~~~~~~~~~

* At least 3 instruments (for unique directional resolution)
* Non-collinear arrangement (not all in a line)
* Known, precise locations

Optimal Configurations
~~~~~~~~~~~~~~~~~~~~~~

**Triangular Array:**

.. code-block:: python

    # Equilateral triangle, 10m sides
    layout = np.array([
        [0, 10, 5],
        [0, 0, 8.66],
        [0, 0, 0]
    ])

Good for omnidirectional resolution.

**Cross Array:**

.. code-block:: python

    # Cross pattern, 10m arms
    layout = np.array([
        [0, 10, -10, 0, 0],
        [0, 0, 0, 10, -10],
        [0, 0, 0, 0, 0]
    ])

Excellent directional resolution, especially for dominant directions aligned with axes.

Spacing Considerations
~~~~~~~~~~~~~~~~~~~~~~

The instrument spacing should satisfy:

.. math::

   d < \\frac{\\lambda_{min}}{2}
   
where d is spacing and λₘᵢₙ is the shortest wavelength of interest.

For deep water: λ ≈ 1.56 T² (T in seconds, λ in meters)

Example: For waves up to 0.5 Hz (T=2s), λ ≈ 6.2m, so use spacing < 3m.

Data Quality Considerations
----------------------------

Regardless of instrument type:

* **Sampling rate**: Should satisfy Nyquist criterion (fs > 2*fₘₐₓ)
  Typically 1-4 Hz is sufficient for ocean waves

* **Record length**: Longer records give better statistical estimates
  Typical: 20-30 minutes for ocean waves

* **Synchronization**: All instruments must be precisely time-synchronized

* **Calibration**: Ensure all instruments are properly calibrated to physical units

* **Quality control**: Remove spikes, check for sensor failures, verify data ranges

Common Issues and Solutions
----------------------------

**Issue**: High-frequency energy appears unrealistic

**Solution**: Check pressure sensor depth; may be too deep for high frequencies

**Issue**: Directional resolution is poor

**Solution**: Check array aperture; may be too small relative to wavelength

**Issue**: Spurious peaks in spectrum

**Solution**: Check for electronic noise, sensor aliasing, or motion artifacts

**Issue**: Missing low-frequency energy

**Solution**: Record length may be too short; use longer time series

See Also
--------

* :doc:`estimation_methods` for choosing the right algorithm
* :doc:`troubleshooting` for debugging common problems

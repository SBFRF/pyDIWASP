Examples
========

This section provides example usage of pyDIWASP for various scenarios.

Example Notebook
----------------

The main example is provided as a Jupyter notebook in the repository:

* `pyDIWASP_example.ipynb <https://github.com/SBFRF/pyDIWASP/blob/main/examples/pyDIWASP_example.ipynb>`_

This notebook demonstrates:

* Setting up instrument data structures
* Computing directional spectra
* Analyzing wave statistics
* Creating visualizations
* Comparing estimation methods

Basic Usage Examples
--------------------

Example 1: Three Pressure Sensors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import numpy as np
    from pydiwasp import dirspec, infospec, plotspec
    import matplotlib.pyplot as plt
    
    # Generate synthetic wave data (for demonstration)
    t = np.arange(0, 1024) / 2.0  # 512 seconds at 2 Hz
    
    # Simulate waves from 45° with period 8s
    freq = 1/8  # 0.125 Hz
    wave = np.sin(2*np.pi*freq*t)
    
    # Three sensors in triangular array
    sensor1 = wave + 0.1*np.random.randn(len(t))
    sensor2 = wave + 0.1*np.random.randn(len(t))  
    sensor3 = wave + 0.1*np.random.randn(len(t))
    
    data = np.column_stack([sensor1, sensor2, sensor3])
    
    # Define instrument data
    ID = {
        'layout': np.array([[0, 10, 5], [0, 0, 8.66], [0, 0, 0]]),
        'datatypes': ['pres', 'pres', 'pres'],
        'depth': 10.0,
        'fs': 2.0,
        'data': data
    }
    
    # Define spectral matrix
    SM = {
        'freqs': np.linspace(0.05, 0.5, 50),
        'dirs': np.linspace(-180, 180, 36)
    }
    
    # Estimation parameters
    EP = {'method': 'IMLM', 'iter': 100}
    
    # Compute spectrum
    SMout, EPout = dirspec(ID, SM, EP, ['PLOTTYPE', 0])
    
    # Get statistics
    Hsig, Tp, DTp, Dp = infospec(SMout)
    
    # Plot
    plotspec(SMout, 4)  # polar plot with compass bearings
    plt.show()

Example 2: Mixed Instrument Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import numpy as np
    from pydiwasp import dirspec
    
    # Load your data
    pressure_data = np.loadtxt('pressure.csv', delimiter=',')
    velocity_x = np.loadtxt('velocity_x.csv', delimiter=',')
    velocity_y = np.loadtxt('velocity_y.csv', delimiter=',')
    elevation = np.loadtxt('elevation.csv', delimiter=',')
    
    # Combine into single array
    data = np.column_stack([
        pressure_data[:, 0],
        pressure_data[:, 1],
        velocity_x,
        velocity_y,
        elevation
    ])
    
    # Mixed array configuration
    ID = {
        'layout': np.array([
            [0, 10, 15, 15, 5],     # x positions
            [0, 0, 5, 5, 10],       # y positions
            [0, 0, -2, -2, 0]       # z positions
        ]),
        'datatypes': ['pres', 'pres', 'velx', 'vely', 'elev'],
        'depth': 12.0,
        'fs': 4.0,
        'data': data
    }
    
    SM = {
        'freqs': np.linspace(0.05, 0.5, 50),
        'dirs': np.linspace(-np.pi, np.pi, 36)
    }
    
    EP = {'method': 'IMLM'}
    
    SMout, EPout = dirspec(ID, SM, EP)

Example 3: Time Series Analysis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import numpy as np
    from pydiwasp import dirspec, infospec
    import matplotlib.pyplot as plt
    
    # Load long time series
    full_data = np.loadtxt('wave_timeseries.csv', delimiter=',')
    
    # Analysis parameters
    fs = 2.0  # sampling frequency
    window_length = 20 * 60 * fs  # 20 minutes
    overlap = 0.5
    step = int(window_length * (1 - overlap))
    
    # Fixed structures
    ID = {
        'layout': np.array([[0, 10, 20], [0, 0, 0], [0, 0, 0]]),
        'datatypes': ['pres', 'pres', 'pres'],
        'depth': 10.0,
        'fs': fs,
        'data': None  # will be filled for each window
    }
    
    SM = {
        'freqs': np.linspace(0.05, 0.5, 50),
        'dirs': np.linspace(-180, 180, 36)
    }
    
    EP = {'method': 'IMLM', 'iter': 100}
    
    # Process each window
    times = []
    Hsigs = []
    Tps = []
    Dps = []
    
    for i in range(0, len(full_data) - window_length, step):
        window = full_data[i:i+int(window_length), :]
        ID['data'] = window
        
        # Compute spectrum
        SMout, EPout = dirspec(ID, SM, EP, ['MESSAGE', 0, 'PLOTTYPE', 0])
        
        # Get statistics
        Hsig, Tp, DTp, Dp = infospec(SMout)
        
        times.append(i / fs / 3600)  # time in hours
        Hsigs.append(Hsig)
        Tps.append(Tp)
        Dps.append(Dp)
    
    # Plot time series of parameters
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    
    axes[0].plot(times, Hsigs)
    axes[0].set_ylabel('Hsig (m)')
    axes[0].grid(True)
    
    axes[1].plot(times, Tps)
    axes[1].set_ylabel('Tp (s)')
    axes[1].grid(True)
    
    axes[2].plot(times, Dps)
    axes[2].set_ylabel('Dp (deg)')
    axes[2].set_xlabel('Time (hours)')
    axes[2].grid(True)
    
    plt.tight_layout()
    plt.show()

Example 4: Comparing Estimation Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import numpy as np
    from pydiwasp import dirspec, infospec, plotspec
    import matplotlib.pyplot as plt
    
    # Your data setup
    ID = {...}
    SM = {...}
    
    # Compare IMLM and EMEP
    methods = ['IMLM', 'EMEP']
    results = {}
    
    for method in methods:
        EP = {'method': method, 'iter': 100}
        SMout, EPout = dirspec(ID, SM, EP, ['PLOTTYPE', 0])
        
        Hsig, Tp, DTp, Dp = infospec(SMout)
        
        results[method] = {
            'spectrum': SMout,
            'Hsig': Hsig,
            'Tp': Tp,
            'DTp': DTp,
            'Dp': Dp
        }
    
    # Plot comparison
    fig = plt.figure(figsize=(14, 5))
    
    for i, method in enumerate(methods):
        plt.subplot(1, 2, i+1)
        plotspec(results[method]['spectrum'], 1)
        plt.title(f"{method}: Hsig={results[method]['Hsig']:.2f}m, "
                  f"Tp={results[method]['Tp']:.1f}s")
    
    plt.tight_layout()
    plt.show()
    
    # Print statistics comparison
    print("Method Comparison:")
    print("-" * 60)
    for method in methods:
        r = results[method]
        print(f"{method}:")
        print(f"  Hsig = {r['Hsig']:.3f} m")
        print(f"  Tp = {r['Tp']:.2f} s")
        print(f"  DTp = {r['DTp']:.1f}°")
        print(f"  Dp = {r['Dp']:.1f}°")
        print()

Example 5: Exporting Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import numpy as np
    from pydiwasp import dirspec, infospec, writespec
    
    # Compute spectrum
    SMout, EPout = dirspec(ID, SM, EP)
    Hsig, Tp, DTp, Dp = infospec(SMout)
    
    # Write spectrum to DIWASP format
    writespec(SMout, 'output_spectrum.txt')
    
    # Export statistics to CSV
    stats = {
        'Hsig': Hsig,
        'Tp': Tp,
        'DTp': DTp,
        'Dp': Dp
    }
    
    with open('wave_statistics.csv', 'w') as f:
        f.write('Parameter,Value\\n')
        for key, value in stats.items():
            f.write(f'{key},{value}\\n')
    
    # Export spectrum to numpy format
    np.savez('spectrum.npz',
             freqs=SMout['freqs'],
             dirs=SMout['dirs'],
             S=SMout['S'],
             Hsig=Hsig,
             Tp=Tp,
             DTp=DTp,
             Dp=Dp)
    
    # Load back later
    loaded = np.load('spectrum.npz')
    freqs = loaded['freqs']
    dirs = loaded['dirs']
    S = loaded['S']

Example 6: Custom Frequency Range
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import numpy as np
    from pydiwasp import dirspec
    
    # Focus on swell (long period waves)
    SM_swell = {
        'freqs': np.linspace(0.04, 0.15, 30),  # 6.7 to 25 seconds
        'dirs': np.linspace(-180, 180, 36)
    }
    
    EP = {'method': 'EMEP'}  # EMEP good for swell
    SMout_swell, _ = dirspec(ID, SM_swell, EP)
    
    # Focus on wind waves (short period)
    SM_wind = {
        'freqs': np.linspace(0.15, 0.5, 40),  # 2 to 6.7 seconds
        'dirs': np.linspace(-180, 180, 36)
    }
    
    EP = {'method': 'IMLM'}  # IMLM good for complex seas
    SMout_wind, _ = dirspec(ID, SM_wind, EP)

More Examples
-------------

For more examples, see:

* The `examples directory <https://github.com/SBFRF/pyDIWASP/tree/main/examples>`_ in the repository
* The test files in `tests/ <https://github.com/SBFRF/pyDIWASP/tree/main/tests>`_ directory
* The original MATLAB DIWASP manual for conceptual guidance

import warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import detrend
from .interpspec import interpspec
from .infospec import infospec
from .writespec import writespec
from .plotspec import plotspec
from .private.velx import velx
from .private.vely import vely
from .private.pres import pres
from .private.elev import elev
from .private.vels import vels
from .private.accs import accs, accz
from .private.wavenumber import wavenumber
from .private.IMLM import IMLM
from .private.EMEP import EMEP
from .private.smoothspec import smoothspec
from .private.diwasp_csd import diwasp_csd
from .private.check_data import check_data

def dirspec(ID, SM, EP, Options_=None):
    """
    Estimate directional wave spectrum from instrument array measurements.
    
    This is the main function for directional wave spectrum analysis. It takes 
    measurements from an array of wave instruments and estimates the distribution 
    of wave energy as a function of frequency and direction.
    
    Parameters
    ----------
    ID : dict
        Instrument data structure containing measured wave data. Required fields:
        
        * 'layout' : ndarray, shape (3, N)
            Instrument positions as [x; y; z] coordinates in meters.
            x, y are horizontal positions, z is vertical (typically 0 or depth).
        * 'datatypes' : list of str
            Type of measurement for each instrument. Valid types: 
            'pres' (pressure), 'elev' (surface elevation), 
            'velx' (x-velocity), 'vely' (y-velocity), 
            'vels' (horizontal velocity magnitude), 'accs' (acceleration).
        * 'depth' : float
            Water depth in meters.
        * 'fs' : float
            Sampling frequency in Hz.
        * 'data' : ndarray, shape (nsamples, ninstruments)
            Time series measurements from each instrument.
            
    SM : dict
        Spectral matrix structure defining the output grid. Required fields:
        
        * 'freqs' : ndarray
            Frequency values for the output spectrum. Values should match
            the units specified by 'funit' (see below).
        * 'dirs' : ndarray
            Direction values for the output spectrum. Values should match
            the convention specified by 'dunit' (see below).
            
        Optional fields:
        
        * 'funit' : str, optional
            Frequency units (case-insensitive). Accepted values:
            
            - 'hz' (default): Frequencies in cycles per second (Hz)
            - Any other value: Treated as angular frequency (rad/s)
            
        * 'dunit' : str, optional
            Direction convention (case-insensitive). Accepted values:
            
            - 'cart' (default): Cartesian/mathematical directions in degrees,
              measured counter-clockwise from x-axis
            - 'naut': Nautical/meteorological directions in degrees,
              measured clockwise from North (compass bearings)
            
            Note: Both conventions expect directions in degrees, not radians.
            
        * 'xaxisdir' : float, optional
            Direction of the positive x-axis in compass degrees (default: 90 = East).
            Used for coordinate transformations.
            
    EP : dict
        Estimation parameters. Use empty dict {} for default values. Fields:
        
        * 'method' : str, optional
            Estimation method: 'IMLM' (default) or 'EMEP'.
        * 'nfft' : int, optional
            FFT length for spectral estimation. Auto-calculated if not provided.
        * 'dres' : int, optional
            Directional resolution (number of direction bins, default: 180).
        * 'iter' : int, optional
            Number of iterations for iterative methods (default: 100).
        * 'smooth' : str, optional
            Spectral smoothing: 'ON' (default) or 'OFF'.
            
    Options_ : list, optional
        Optional parameters as alternating name/value pairs.
        Example: ['MESSAGE', 1, 'PLOTTYPE', 2, 'FILEOUT', 'output.txt']
        
        Available options:
        
        * 'MESSAGE' : int, default 1
            Level of console output (0=none, 1=normal, 2=verbose).
        * 'PLOTTYPE' : int, default 1
            Plot type: 0=none, 1=3D surface, 2=polar, 
            3=3D compass, 4=polar compass.
        * 'FILEOUT' : str, default ''
            Output filename (empty string = no file output).
    
    Returns
    -------
    SMout : dict
        Output spectral matrix with computed directional spectrum. Contains all
        input SM fields plus:
        
        * 'S' : ndarray, shape (nfreqs, ndirs)
            Spectral density values [m²/Hz/degree or m²s/rad].
            
    EPout : dict
        Estimation parameters actually used, including any default values that
        were applied.
    
    Examples
    --------
    Basic example with three pressure sensors in a triangular array:
    
    >>> import numpy as np
    >>> from pydiwasp import dirspec
    >>> 
    >>> # Define instrument array
    >>> ID = {
    ...     'layout': np.array([[0, 10, 5], [0, 0, 8.66], [0, 0, 0]]),
    ...     'datatypes': ['pres', 'pres', 'pres'],
    ...     'depth': 10.0,
    ...     'fs': 2.0,
    ...     'data': wave_measurements  # shape: (nsamples, 3)
    ... }
    >>> 
    >>> # Define output frequency-direction grid
    >>> SM = {
    ...     'freqs': np.linspace(0.05, 0.5, 50),  # 0.05 to 0.5 Hz
    ...     'dirs': np.linspace(-180, 180, 36)    # -180 to 180 degrees
    ... }
    >>> 
    >>> # Use default estimation parameters (IMLM method)
    >>> EP = {'method': 'IMLM', 'iter': 100}
    >>> 
    >>> # Compute directional spectrum
    >>> SMout, EPout = dirspec(ID, SM, EP)
    >>> 
    >>> # Access the directional spectrum
    >>> spectrum = SMout['S']  # shape: (50, 36)
    
    With custom options:
    
    >>> # Suppress output and skip plotting
    >>> options = ['MESSAGE', 0, 'PLOTTYPE', 0]
    >>> SMout, EPout = dirspec(ID, SM, EP, options)
    
    Notes
    -----
    The implemented estimation algorithms are described in:
    
    Hashimoto, N. (1997). "Analysis of the directional wave spectrum from field data".
    In: Advances in Coastal Engineering Vol. 3. Ed: Liu, P.L-F.
    Pub: World Scientific, Singapore.
    
    The function automatically:
    - Detects and removes trends from input data
    - Calculates cross-spectral densities between all instrument pairs
    - Computes wave numbers using linear wave theory
    - Calculates instrument transfer functions
    - Applies the selected estimation method
    - Interpolates results onto the requested output grid
    - Optionally smooths the spectrum
    
    See Also
    --------
    infospec : Calculate wave statistics from directional spectrum
    plotspec : Plot directional spectrum
    interpspec : Interpolate spectrum to different grid
    
    References
    ----------
    Original MATLAB version: Copyright (C) 2002 Coastal Oceanography Group, 
    CWR, UWA, Perth
    
    Python translation: Chuan Li and Spicer Bak, Field Research Facility, 
    US Army Corps of Engineers
    """

    Options = {'MESSAGE':1, 'PLOTTYPE':1, 'FILEOUT':''}

    if Options_ is not None:
        nopts = len(Options_)
    else:
        nopts = 0

    ID = check_data(ID, 1)
    if len(ID) == 0:
        return [], []
    SM = check_data(SM, 2)
    if len(SM) == 0:
        return [], []
    EP = check_data(EP, 3)
    if len(EP) == 0:
        return [], []

    if nopts != 0:
        if nopts % 2 != 0:
            warnings.warn('Options must be in Name/Value pairs - setting to '
                'defaults')
        else:
            for i in range(int(nopts / 2)):
                arg = Options_[2 * i + 1]
                field = Options_[2 * i]
                Options[field] = arg

    ptype = Options['PLOTTYPE']
    displ = Options['MESSAGE']


    print('\ncalculating.....\n\ncross power spectra')

    data = detrend(ID['data'], axis=0)
    ndat, szd = np.shape(ID['data'])

    #get resolution of FFT - if not specified, calculate a sensible value
    if 'nfft' not in EP or not EP['nfft']:
        nfft = int(2 ** (8 + np.round(np.log2(ID['fs']))))
        EP['nfft'] = nfft
    else:
        nfft = int(EP['nfft'])
    if nfft > ndat:
        raise Exception('Data length of {} too small'.format(ndat))

    #calculate the cross-power spectra
    xps = np.empty((szd, szd, int(nfft / 2)), 'complex128')
    for m in range(szd):
        for n in range(szd):
            xpstmp, Ftmp = diwasp_csd(data[:, m], data[:, n],
                                      nfft, ID['fs'], flag=2)
            xps[m, n, :] = xpstmp[1:int(nfft / 2) + 1]
    F = Ftmp[1:int(nfft / 2) + 1]
    nf = int(nfft / 2)
    print('wavenumbers')
    wns = wavenumber(2  * np.pi * F, ID['depth'] * np.ones(np.shape(F)))
    pidirs = np.linspace(-np.pi, np.pi - 2 * np.pi / EP['dres'],
        num=EP['dres'])

    #calculate transfer parameters
    print('transfer parameters\n')
    trm = np.empty((szd, nf, len(pidirs)))
    kx = np.empty((szd, szd, nf, len(pidirs)))
    for m in range(szd):
        trm[m, :, :] = eval(ID['datatypes'][m])(2 * np.pi * F, pidirs, wns,
            ID['layout'][2, m], ID['depth'])
        for n in range(szd):
            kx[m, n, :, :] = wns[:, np.newaxis] * ((ID['layout'][0, n] -
                ID['layout'][0, m]) * np.cos(pidirs) + (ID['layout'][1, n] -
                ID['layout'][1, m]) * np.sin(pidirs))

    Ss = np.empty((szd, nf), dtype='complex128')
    for m in range(szd):
        tfn = trm[m, :, :]
        Sxps = xps[m, m, :]
        Ss[m, :] = Sxps / (np.max(tfn, axis=1) * np.conj(np.max(tfn, axis=1)))

    ffs = np.logical_and(F >= np.min(SM['freqs']), F <= np.max(SM['freqs']))
    SM1 = dict()
    SM1['freqs'] = F[ffs]
    SM1['funit'] = 'Hz'
    SM1['dirs'] = pidirs
    SM1['dunit'] = 'rad'

    # call appropriate estimation function
    print('directional spectra using {} method'.format(EP['method']))
    SM1['S'] = eval(EP['method'])(xps[:, :, ffs], trm[:, ffs, :],
        kx[:, :, ffs, :], Ss[:, ffs], pidirs, EP['iter'], displ)
    SM1['S'][np.logical_or(np.isnan(SM1['S']), SM1['S'] < 0)] = 0

    #Interpolate onto user specified matrix
    print('\ninterpolating onto specified matrix...\n')
    SMout = interpspec(SM1, SM, method='linear')

    #smooth spectrum
    if EP['smooth'].upper() == 'ON':
        print('\nsmoothing spectrum...\n')
        SMout = smoothspec(SMout, [[1, 0.5, 0.25], [1, 0.5, 0.25]])

    infospec(SMout)

    #write out spectrum matrix in DIWASP format
    filename = Options['FILEOUT']
    if len(filename) > 0:
        print('writing out spectrum matrix to file')
        writespec(SMout,filename)

    #plot spectrum
    if ptype > 0:
        print('finished...plotting spectrum')
        plotspec(SMout, ptype)
        T = 'Directional spectrum estimate using {} method'.format(EP['method'])
        plt.title(T)
        plt.show()

    return SMout, EP

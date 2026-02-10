import numpy as np
from .private.hsig import hsig

def infospec(SM):
    """
    Calculate and display wave statistics from a directional spectrum.
    
    This function computes key wave parameters from a directional spectrum,
    including significant wave height, peak period, and dominant directions.
    Results are printed to the console.
    
    Parameters
    ----------
    SM : dict
        Spectral matrix structure containing the directional spectrum.
        Required fields:
        
        * 'freqs' : ndarray
            Frequency values (Hz or rad/s).
        * 'dirs' : ndarray
            Direction values (radians or degrees).
        * 'S' : ndarray, shape (nfreqs, ndirs)
            Spectral density values.
            
        Optional fields:
        
        * 'xaxisdir' : float, optional
            Direction of x-axis in compass degrees (default: 90 = East).
            Used for converting to compass bearings.
    
    Returns
    -------
    Hsig : float
        Significant wave height in meters. Defined as 4 times the standard
        deviation of the sea surface elevation, calculated from the integrated
        spectrum: Hsig = 4 * sqrt(m0), where m0 is the zeroth moment.
        
    Tp : float
        Peak period in seconds. The period corresponding to the frequency with
        the maximum energy in the frequency spectrum (1D spectrum integrated
        over all directions).
        
    DTp : float
        Direction of the spectral peak in the units specified by SM['dunit'].
        The direction at which the 2D spectrum has its maximum value.
        This is the direction of waves at the peak frequency.
        
    Dp : float
        Dominant direction in the units specified by SM['dunit'].
        The direction with the highest integrated energy across all frequencies.
        This represents the overall dominant wave propagation direction.
    
    Examples
    --------
    Calculate wave statistics from a computed spectrum:
    
    >>> from pydiwasp import dirspec, infospec
    >>> 
    >>> # After computing spectrum with dirspec
    >>> SMout, EPout = dirspec(ID, SM, EP)
    >>> 
    >>> # Get wave statistics
    >>> Hsig, Tp, DTp, Dp = infospec(SMout)
    Infospec::
    Significant wave height: 2.5
    Peak period: 10.0
    Direction of peak period: 45.0 axis angle / 45.0 compass bearing
    Dominant direction: 50.0 axis angle / 40.0 compass bearing
    >>> 
    >>> print(f"Wave height: {Hsig:.2f} m")
    Wave height: 2.50 m
    >>> print(f"Peak period: {Tp:.1f} s")
    Peak period: 10.0 s
    
    Notes
    -----
    The function prints results to stdout with both axis angles and compass
    bearings. The conversion between these depends on the 'xaxisdir' field
    in the SM structure.
    
    Axis angles are measured counter-clockwise from the x-axis.
    Compass bearings are measured clockwise from North (0°).
    
    The significant wave height Hsig is approximately equal to the average
    height of the highest one-third of waves in a wave record.
    
    See Also
    --------
    dirspec : Compute directional spectrum
    compangle : Convert between axis angles and compass bearings
    
    References
    ----------
    Original MATLAB version: Copyright (C) 2002 Coastal Oceanography Group,
    CWR, UWA, Perth
    """

    H = hsig(SM)

    S = np.sum(np.real(SM['S']), 1)

    I = np.argmax(S)
    Tp = 1 / (SM['freqs'][I])
    I = np.argmax(np.real(SM['S'][I, :]))
    DTp = SM['dirs'][I]
    I = np.argmax(np.real(np.sum(SM['S'], 0)))
    Dp = SM['dirs'][I]

    print('Infospec::')
    print('Significant wave height: {}'.format(H))
    print('Peak period: {}'.format(Tp))
    print('Direction of peak period: {} axis angle / {} ' 
        'compass bearing'.format(DTp, compangle(DTp, SM['xaxisdir'])))
    print('Dominant direction: {} axis angle / {} ' 
        'compass bearing'.format(Dp, compangle(Dp, SM['xaxisdir'])))
    
    return H, Tp, DTp, Dp

def compangle(dirs, xaxisdir):
    """
    Convert between axis angles and compass bearings.
    
    Converts directional angles from a mathematical coordinate system
    (counter-clockwise from x-axis) to nautical compass bearings
    (clockwise from North).
    
    Parameters
    ----------
    dirs : float or ndarray
        Direction(s) in degrees, measured counter-clockwise from the x-axis.
        
    xaxisdir : float
        Compass bearing of the x-axis in degrees. Typically 90 (East).
    
    Returns
    -------
    bearings : float or ndarray
        Compass bearing(s) in degrees (0-360), measured clockwise from North.
        
    Examples
    --------
    >>> from pydiwasp import compangle
    >>> 
    >>> # Convert 45° axis angle to compass bearing (x-axis points East)
    >>> bearing = compangle(45, 90)
    >>> print(bearing)
    45.0
    >>> 
    >>> # Convert multiple directions
    >>> import numpy as np
    >>> dirs = np.array([0, 45, 90, 180, 270])
    >>> bearings = compangle(dirs, 90)
    >>> print(bearings)
    [90. 45. 0. 270. 180.]
    
    Notes
    -----
    The conversion formula is: bearing = (180 + xaxisdir - dirs) mod 360
    
    This accounts for:
    - The 180° difference between "direction to" and "direction from"
    - The rotation from mathematical (CCW from x) to nautical (CW from N)
    - The orientation of the x-axis
    """
    return (180 + xaxisdir * np.ones(np.shape(dirs)) - dirs) % 360

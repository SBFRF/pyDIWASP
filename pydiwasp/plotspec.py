import matplotlib.pyplot as plt
import numpy as np
from .private.spectobasis import spectobasis

def plotspec(SM, ptype):
    """
    Plot directional wave spectrum in 3D or polar form.
    
    Creates visualizations of the directional spectrum showing how wave energy
    is distributed across frequencies and directions. Supports multiple plot
    types including 3D surface plots and polar contour plots.
    
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
            Used for plot types 3 and 4.
        * 'funit' : str, optional
            Frequency units: 'Hz' or 'rad/s'.
        * 'dunit' : str, optional
            Direction units: 'rad' or 'deg'.
            
    ptype : int
        Plot type selection:
        
        * 1 : 3D surface plot with mathematical angles
            - X-axis: frequency (Hz)
            - Y-axis: direction (degrees, -180 to 180)
            - Z-axis: spectral density
            - Directions measured counter-clockwise from x-axis
            
        * 2 : Polar contour plot with mathematical angles
            - Angle: direction (radians)
            - Radius: frequency (Hz)
            - Contours: spectral density levels
            - Directions measured counter-clockwise from x-axis
            
        * 3 : 3D surface plot with compass bearings
            - X-axis: frequency (Hz)
            - Y-axis: compass bearing (0-360°)
            - Z-axis: spectral density
            - Bearings are "direction from" (oceanographic convention)
            
        * 4 : Polar contour plot with compass bearings
            - Angle: compass bearing (radians)
            - Radius: frequency (Hz)
            - Contours: spectral density levels
            - Bearings are "direction from" (oceanographic convention)
    
    Returns
    -------
    None
        The function displays a matplotlib figure. Use plt.show() to display
        or plt.savefig() to save the figure.
    
    Examples
    --------
    Create different visualizations of a directional spectrum:
    
    >>> from pydiwasp import dirspec, plotspec
    >>> import matplotlib.pyplot as plt
    >>> 
    >>> # Compute spectrum
    >>> SMout, EPout = dirspec(ID, SM, EP)
    >>> 
    >>> # 3D surface plot (mathematical angles)
    >>> plotspec(SMout, 1)
    >>> plt.show()
    >>> 
    >>> # Polar contour plot (compass bearings)
    >>> plotspec(SMout, 4)
    >>> plt.show()
    >>> 
    >>> # Create multiple subplots
    >>> fig = plt.figure(figsize=(12, 5))
    >>> plt.subplot(121)
    >>> plotspec(SMout, 1)
    >>> plt.subplot(122)
    >>> plotspec(SMout, 2)
    >>> plt.tight_layout()
    >>> plt.show()
    
    Notes
    -----
    The 3D surface plots provide a clear view of the spectral shape and are
    good for presentations. The polar plots are more traditional in wave
    analysis and are compact for showing directional spreading.
    
    For plot types 1 and 2, directions are in mathematical convention
    (counter-clockwise from x-axis). For types 3 and 4, directions are
    nautical compass bearings representing "direction from" (where waves
    are coming from), which is the oceanographic convention.
    
    The spectral density units shown are m²s/deg for the 3D plots.
    
    See Also
    --------
    dirspec : Compute directional spectrum
    infospec : Calculate wave statistics
    
    References
    ----------
    Original MATLAB version: Copyright (C) 2002 Coastal Oceanography Group,
    CWR, UWA, Perth
    """

    fig = plt.figure(tight_layout=True)

    SM, sfac = spectobasis(SM) #Convert to basis matrix
    dirs = SM['dirs']
    ffreqs = SM['freqs'] / (2 * np.pi)
    S = 2 * np.pi ** 2 * np.real(SM['S'])/ 180

    #Convert directions to nautical
    if ptype == 3 or ptype == 4:
        if 'xaxisdir' in SM.keys():
            xaxisdir = SM['xaxisdir']
        else:
            xaxisdir = 90
        dirs = dirs + np.pi + np.pi * (90 - xaxisdir) / 180
    
    #Surface plots
    if ptype == 1 or ptype == 3:
        if ptype == 3: 
            dirs %= 2 * np.pi
        order = np.argsort(dirs)
        dirs = (180 * dirs / np.pi)[order]
        ddir, df = np.meshgrid(dirs, ffreqs)
        S = S[:, order]
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('frequency [Hz]')
        if ptype == 1:
            ax.set_ylabel('direction [degrees]')
            ax.set_xlim(0, np.max(ffreqs))
            ax.set_ylim(-180, 180)
            ax.set_zlim(0, np.max(S))
            S[:, dirs > 180] = np.nan
        else:
            ax.set_ylabel('direction [bearings]')
            ax.set_xlim(0, np.max(ffreqs))
            ax.set_ylim(0, 360)
            ax.set_zlim(0, np.max(S))
        ax.plot_surface(df, ddir, np.real(S))
        ax.set_zlabel('m^2s / deg')
        ax.view_init(30, -135)

    #Polar plots
    elif ptype == 2 or ptype == 4:
        ddir, df = np.meshgrid(dirs, ffreqs)
        ax = fig.add_subplot(111, projection='polar')
        ax.set_rlim(0, 0.8 * np.max(ffreqs))
        c = ax.contour(ddir, df, np.real(S), 20)
        fig.colorbar(c)
        if ptype == 2:
            ax.set_ylabel('direction [degrees] / frequency [Hz]')
        else:
            ax.set_ylabel('direction [bearing] / frequency [Hz]')
        ax.set_xlabel('m^2 s / deg')

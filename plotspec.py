import matplotlib.pyplot as plt
import numpy as np
from private.spectobasis import spectobasis
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def plotspec(SM, ptype):
    """
    DIWASP V1.4 function
    plotspec: plots the spectral matrix in 3D or polar form
    
    plotspec(SM,ptype)
    
    Inputs:
     SM   		A spectral matrix structure
     ptype		plot type:
       1	3D surface plot
       2	polar type plot 
       3	3D surface plot (compass bearing angles direction from)
       4	polar type plot (compass bearing angles direction from)
    
    The 3D surface plot type is a MATLAB surface plot with SM.freqs on the x axis, SM.dirs on the y axis and the spectral density, SM.S as the z value. 
    The polar type plot is a MATLAB polar plot with the direction showing values in SM.dirs, the radius showing values in SM.freqs 
    and contours representing the spectral density, SM.S. An example of the polar type plot is shown on the front cover of the manual.
    For plot types 1 and 2, the direction is the direction of propagation relative to the Cartesian axis. 
    For options 3 and 4 the direction is coming from as a true compass bearing (this has changed from previous versions). 
    Directions are corrected internally from the SM.xaxisdir and SM.dunit
    fields that define the orientation of the axes and directional units in the spectral matrix. 
    
    "help data_structures" for information on the DIWASP data structures

    Copyright (C) 2002 Coastal Oceanography Group, CWR, UWA, Perth
    """

    fig = plt.figure(tight_layout=True)

    SM, sfac = spectobasis(SM) #Convert to basis matrix
    dirs = SM['dirs']; ffreqs = SM['freqs'] / (2 * np.pi)
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
        if ptype == 3: dirs %= 2 * np.pi
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
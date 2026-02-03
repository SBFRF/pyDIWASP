import numpy as np
from private.hsig import hsig

def infospec(SM):
    """
    DIWASP V1.4 function
    infospec: calculates and displays information about a directional spectrum
    
    [Hsig,Tp,DTp,Dp]=infospec(SM)
    
    Outputs:
    Hsig		Signficant wave height
    Tp			Peak period
    DTp		Direction of spectral peak
    Dp			Dominant direction
    
    Inputs:
    SM   		A spectral matrix structure containing the file data
    
    Hsig is the significant wave height. Tp is the peak frequency, the highest point in the one dimensional spectrum. 
    DTp is the main direction of the peak period (i.e the highest point in the two-dimensional directional spectrum). 
    Dp is the dominant direction defined as the direction with the highest energy integrated over all frequencies.
    
    "help data_structures" for information on the DIWASP data structures

    Copyright (C) 2002 Coastal Oceanography Group, CWR, UWA, Perth
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
    return (180 + xaxisdir * np.ones(np.shape(dirs)) - dirs) % 360

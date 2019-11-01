import numpy as np

def hsig(argin):
    """
    DIWASP function to calculate significant wave height
    
    Hs=Hsig(SM)
    
    Hs is significant wave height of spectral matrix SM
    
    "help data_structures" for information on the DIWASP data structures

    Copyright (C) 2002 Coastal Oceanography Group, CWR, UWA, Perth
    """

    SM = argin
    df = SM['freqs'][1] - SM['freqs'][0]
    ddir = SM['dirs'][1] - SM['dirs'][0]
    S = SM['S']

    Hs = 4 * np.sqrt(np.sum(np.sum(np.real(S))) * df * ddir)

    return Hs
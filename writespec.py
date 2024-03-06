import numpy as np

def writespec(SM, filename):
    """
    DIWASP V1.4 function
    writespec: writes spectrum matrix to file using DIWASP format
    
    writespec(SM,filename)
    
    Inputs:
    SM   		A spectral matrix structure
    filename	String containing the filename including file extension if required
    
    All inputs required
    
    "help data_structures" for information on the DIWASP data structures

    Copyright (C) 2002 Coastal Oceanography Group, CWR, UWA, Perth
    """

    nf = np.max(SM['freqs'].shape)
    nd = np.max(SM['dirs'].shape)

    streamout = np.empty((nf + nd + 4 + nf * nd))

    streamout[0] = SM['xaxisdir']
    streamout[1] = nf
    streamout[2] = nd
    streamout[3:nf + 3] = SM['freqs']
    streamout[nf + 3:nf + nd + 3] = SM['dirs']
    streamout[nf + nd + 3] = 999
    streamout[nf + nd + 4:nf + nd + 4 + nf * nd] = np.reshape(np.real(SM['S']),
        (nf * nd))

    streamout = streamout.T

    np.savetxt(filename, streamout)

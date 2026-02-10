import numpy as np

def writespec(SM, filename):
    """
    Write directional spectrum to file in DIWASP format.
    
    Exports a spectral matrix structure to a text file using the standard
    DIWASP format. This format can be read by other DIWASP tools and is
    useful for archiving results or sharing data.
    
    Parameters
    ----------
    SM : dict
        Spectral matrix structure to write. Required fields:
        
        * 'freqs' : ndarray
            Frequency values (Hz or rad/s).
        * 'dirs' : ndarray
            Direction values (radians or degrees).
        * 'S' : ndarray, shape (nfreqs, ndirs)
            Spectral density values.
        * 'xaxisdir' : float
            Direction of x-axis in compass degrees (typically 90 = East).
            
    filename : str
        Output filename including path and extension if desired.
        Common extensions are .txt or .spc.
    
    Returns
    -------
    None
        The function writes to a file and returns nothing.
    
    File Format
    -----------
    The DIWASP file format is a simple text format with the following structure::
    
        xaxisdir
        nfreqs
        ndirs
        freq1
        freq2
        ...
        freqN
        dir1
        dir2
        ...
        dirM
        999 (separator)
        S[0,0]
        S[0,1]
        ...
        S[N-1,M-1]
    
    All values are written as floating point numbers, one per line.
    The spectral density values S are flattened using NumPy's default C-order,
    where the last axis (direction) varies fastest and the first axis (frequency)
    varies slowest.
    
    Examples
    --------
    Save a computed spectrum to file:
    
    >>> from pydiwasp import dirspec, writespec
    >>> 
    >>> # Compute spectrum
    >>> SMout, EPout = dirspec(ID, SM, EP)
    >>> 
    >>> # Write to file
    >>> writespec(SMout, 'output_spectrum.txt')
    >>> 
    >>> # Or with full path
    >>> import os
    >>> output_dir = '/path/to/results'
    >>> filename = os.path.join(output_dir, 'spectrum_20240101.spc')
    >>> writespec(SMout, filename)
    
    Save multiple spectra from a time series:
    
    >>> import numpy as np
    >>> 
    >>> # Process multiple time windows
    >>> for i, data_window in enumerate(time_windows):
    ...     ID['data'] = data_window
    ...     SMout, EPout = dirspec(ID, SM, EP)
    ...     writespec(SMout, f'spectrum_{i:03d}.txt')
    
    Notes
    -----
    The file format is plain text and can be inspected with any text editor.
    The separator value 999 marks the transition from metadata to spectral data.
    
    Only the real part of the spectral density is written. Any imaginary
    components are discarded.
    
    The saved file can be read back using custom parsing or by other DIWASP-
    compatible software.
    
    See Also
    --------
    dirspec : Compute directional spectrum
    
    References
    ----------
    Original MATLAB version: Copyright (C) 2002 Coastal Oceanography Group,
    CWR, UWA, Perth
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

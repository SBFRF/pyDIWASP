# pyDiwasp
conversion of diwasp package (DIWASP: DIrectional WAve SPectrum analysis Version 1.4) for python
converted from https://github.com/metocean/diwasp

I would lOVE help making this into a more pythonic representation of the original diwasp tool.  check issues for needed functionality adds.  

## Toolbox contents:
### Main functions:
- dirspec.m           Main function for directional wave analysis
- readspec.m          Reads in DIWASP format spectrum files
- writespec.m         Writes DIWASP format spectrum files
- plotspec.m          Plots DIWASP spectrums
- testspec.m          Testing function for the estimation methods
- makespec.m          Makes a fake spectrum and generates fake data for testing dirspec.m
- infospec.m          Returns information about a directional spectrum
- data_structures.m   is a help file describing the new Version 1.1 data structures

## Private functions (some can be used as stand alone functions):
### The transfer functions
- /private/elev.m
- /private/pres.m
- /private/velx.m
- /private/vely.m
- /private/velz.m
- /private/slpx.m
- /private/slpy.m
- /private/vels.m
- /private/accs.m

### The estimation functions
- /private/DFTM.m
- /private/EMLM.m
- /private/IMLM.m
- /private/EMEP.m
- /private/BDM.m

### Miscellaneous functions
- /private/smoothspec.m
- /private/wavenumber.m
- /private/makerandomsea.m
- /private/makewavedata.m
- /private/Hsig.m
- /private/gsamp.m
- /private/check_data.m
  

carying original license agreement and copyright

## License agreement
DIWASP, is free software; you can redistribute it and/or modify it under the terms of the 
GNU General Public License as published by the Free Software Foundation. 
However, the DIWASP license includes the following addendum concerning its usage:
This software and any derivatives of it shall only be used for educational purposes or 
scientific research without the intention of any financial gain. 
Use of this software or derivatives for any purpose that results in financial gain 
for a person or organization without written consent from the author is a breach of the license agreement.
This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
In addition the author is not liable in any way for consequences arising from the application of 
software output for any design or decision-making process.
The GNU General Public License forms the main part of the license agreement included in the package. 

Copyright (C) 2002 David Johnson   Coastal Oceanography Group, CWR, UWA, Perth


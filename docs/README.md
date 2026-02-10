# pyDIWASP Documentation

This directory contains the source files for pyDIWASP's documentation, built using [Sphinx](https://www.sphinx-doc.org/).

## Building the Documentation

### Prerequisites

Install the documentation dependencies:

```bash
pip install -r requirements.txt
```

Or install with the main package:

```bash
cd ..
pip install -e .
cd docs
pip install -r requirements.txt
```

### Building HTML

To build the HTML documentation:

```bash
make html
```

The generated documentation will be in `_build/html/`. Open `_build/html/index.html` in your browser to view it.

### Other Formats

You can build the documentation in other formats:

```bash
make latexpdf  # PDF (requires LaTeX)
make epub      # ePub
make man       # Man pages
```

### Cleaning

To remove all built documentation:

```bash
make clean
```

## Documentation Structure

```
docs/
├── conf.py                          # Sphinx configuration
├── index.rst                        # Main documentation index
├── installation.rst                 # Installation guide
├── quickstart.rst                   # Quick start guide
├── examples.rst                     # Usage examples
├── api/                            # API reference
│   ├── index.rst                   # API index
│   ├── dirspec.rst                 # dirspec function
│   ├── infospec.rst                # infospec function
│   ├── plotspec.rst                # plotspec function
│   ├── interpspec.rst              # interpspec function
│   └── writespec.rst               # writespec function
├── user_guide/                     # User guide
│   ├── index.rst                   # User guide index
│   ├── understanding_spectra.rst   # Theory and concepts
│   ├── instrument_types.rst        # Instrument configuration
│   ├── estimation_methods.rst      # Methods comparison
│   └── troubleshooting.rst         # Common issues
├── developer/                      # Developer documentation
│   ├── contributing.rst            # Contribution guide
│   └── structure.rst               # Code structure
├── references.rst                  # References and citations
├── license.rst                     # License information
├── requirements.txt                # Documentation dependencies
├── Makefile                        # Build script (Unix)
├── make.bat                        # Build script (Windows)
└── README.md                       # This file
```

## Contributing to Documentation

We welcome contributions to improve the documentation! Here's how:

### Adding New Pages

1. Create a new `.rst` file in the appropriate directory
2. Add it to the `toctree` in the parent `index.rst`
3. Build and check for errors
4. Submit a pull request

### Editing Existing Pages

1. Edit the `.rst` file directly
2. Build locally to verify changes
3. Check for formatting issues
4. Submit a pull request

### Writing reStructuredText

The documentation uses reStructuredText (reST) format. Here are some basics:

#### Headers

```rst
Main Title
==========

Section
-------

Subsection
~~~~~~~~~~

Subsubsection
^^^^^^^^^^^^^
```

#### Code Blocks

```rst
.. code-block:: python

    import numpy as np
    from pydiwasp import dirspec
    
    # Your code here
```

#### Links

```rst
`Link text <https://example.com>`_
:doc:`other_page`
:ref:`section-label`
```

#### Lists

```rst
* Bullet point 1
* Bullet point 2

1. Numbered item 1
2. Numbered item 2
```

#### Notes and Warnings

```rst
.. note::
   This is a note.

.. warning::
   This is a warning.

.. seealso::
   See also this related topic.
```

#### Math

```rst
.. math::

   E = mc^2

Inline math: :math:`\\alpha = \\beta + \\gamma`
```

### Docstring Documentation

API documentation is automatically generated from docstrings in the code. Follow NumPy docstring style:

```python
def function_name(param1, param2):
    """
    Brief description.
    
    Longer description explaining what the function does.
    
    Parameters
    ----------
    param1 : type
        Description of param1.
    param2 : type
        Description of param2.
        
    Returns
    -------
    result : type
        Description of return value.
        
    Examples
    --------
    >>> result = function_name(1, 2)
    >>> print(result)
    3
    
    See Also
    --------
    related_function : Related functionality
    
    Notes
    -----
    Any additional notes or caveats.
    
    References
    ----------
    .. [1] Author. "Title". Journal. Year.
    """
    return param1 + param2
```

### Building and Checking

Before submitting documentation changes:

1. **Build locally**: `make html`
2. **Check for warnings**: Sphinx will report any issues
3. **View in browser**: Open `_build/html/index.html`
4. **Check links**: Verify all internal and external links work
5. **Proofread**: Check for typos and formatting

### Style Guidelines

- Use clear, concise language
- Provide practical examples
- Include expected output when relevant
- Use consistent terminology
- Link to related documentation
- Keep code examples simple and focused
- Test all code examples to ensure they work

## Documentation TODO

Areas where documentation could be expanded:

- [ ] More detailed mathematical background
- [ ] Additional examples for edge cases
- [ ] Performance optimization guide
- [ ] Comparison with other wave analysis tools
- [ ] Video tutorials or animated examples
- [ ] FAQ section
- [ ] Glossary of terms
- [ ] Case studies from real deployments

## Questions?

If you have questions about the documentation:

- Open an issue on GitHub
- Check the [Contributing Guide](developer/contributing.rst)
- Contact the maintainers

Thank you for helping improve pyDIWASP's documentation!

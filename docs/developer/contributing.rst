Contributing to pyDIWASP
=========================

We welcome contributions to pyDIWASP! This guide explains how to contribute.

Types of Contributions
-----------------------

We appreciate all types of contributions:

* **Bug reports**: Help us identify and fix issues
* **Feature requests**: Suggest new functionality
* **Documentation**: Improve or expand documentation
* **Code contributions**: Bug fixes, new features, optimizations
* **Examples**: Add new example notebooks or scripts

Getting Started
---------------

1. **Fork the repository** on GitHub

2. **Clone your fork**::

    git clone https://github.com/YOUR-USERNAME/pyDIWASP.git
    cd pyDIWASP

3. **Create a development environment**::

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate
    pip install -e .
    pip install pytest pytest-cov flake8

4. **Create a branch** for your changes::

    git checkout -b feature/my-new-feature
    # or
    git checkout -b fix/issue-123

Development Workflow
--------------------

1. **Make your changes** in your feature branch

2. **Write tests** for new functionality::

    # Add tests to tests/test_*.py
    def test_my_feature():
        # Test code here
        assert result == expected

3. **Run tests** to ensure everything works::

    pytest tests/

4. **Check code style**::

    flake8 pydiwasp tests

5. **Commit your changes**::

    git add .
    git commit -m "Add: Brief description of changes"

6. **Push to your fork**::

    git push origin feature/my-new-feature

7. **Create a Pull Request** on GitHub

Code Guidelines
---------------

Style
~~~~~

* Follow PEP 8 style guidelines
* Use meaningful variable names
* Add docstrings to all public functions
* Keep functions focused and modular

Docstrings
~~~~~~~~~~

Use NumPy-style docstrings:

.. code-block:: python

    def my_function(param1, param2):
        """
        Brief description of function.
        
        Longer description if needed, explaining what the function does
        and any important details.
        
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
        >>> result = my_function(1, 2)
        >>> print(result)
        3
        """
        return param1 + param2

Testing
~~~~~~~

* Write tests for all new functions
* Aim for high test coverage (>80%)
* Test edge cases and error conditions
* Use descriptive test names

.. code-block:: python

    def test_dirspec_with_pressure_sensors():
        """Test dirspec with a simple pressure sensor array."""
        # Setup
        ID = {...}
        SM = {...}
        EP = {...}
        
        # Execute
        SMout, EPout = dirspec(ID, SM, EP)
        
        # Assert
        assert SMout is not None
        assert 'S' in SMout
        assert SMout['S'].shape == (len(SM['freqs']), len(SM['dirs']))

Documentation
~~~~~~~~~~~~~

* Update documentation for any API changes
* Add examples for new features
* Keep README.md up to date

Reporting Bugs
--------------

When reporting bugs, please include:

1. **Description**: Clear description of the problem

2. **Minimal example**: Code that reproduces the issue::

    import numpy as np
    from pydiwasp import dirspec
    
    # Minimal code that shows the bug
    ID = {...}
    SMout, EPout = dirspec(ID, SM, EP)
    # Error occurs here

3. **Error message**: Full traceback if applicable

4. **Environment**:
   * Python version
   * pyDIWASP version
   * Operating system
   * Package versions: ``pip list``

5. **Expected behavior**: What you expected to happen

6. **Actual behavior**: What actually happened

Requesting Features
-------------------

For feature requests, please:

1. **Check existing issues** to avoid duplicates

2. **Describe the feature** clearly

3. **Explain the use case**: Why is this feature needed?

4. **Provide examples**: Show how you'd use the feature

5. **Consider implementation**: If possible, suggest how it might work

Adding New Estimation Methods
------------------------------

To add a new spectrum estimation method:

1. **Create the method file**::

    # pydiwasp/private/MYMETHOD.py
    
    def MYMETHOD(xps, trm, kx, Ss, pidirs, miter, displ):
        """
        My new estimation method.
        
        Parameters
        ----------
        xps : ndarray
            Cross-spectral density matrix
        trm : ndarray
            Transfer function matrix
        kx : ndarray
            Wavenumber separation matrix
        Ss : ndarray
            Auto-spectra
        pidirs : ndarray
            Direction array
        miter : int
            Number of iterations
        displ : int
            Display level
            
        Returns
        -------
        S : ndarray
            Estimated directional spectrum
        """
        # Implementation here
        return S

2. **Import in dirspec.py**::

    from .private.MYMETHOD import MYMETHOD

3. **Add to method call**:
   
   The method is called via ``eval(EP['method'])`` in dirspec.py

4. **Write tests**::

    # tests/test_methods.py
    
    def test_MYMETHOD():
        # Test your method
        pass

5. **Update documentation**:
   
   * Add to README.md
   * Add to docs/user_guide/estimation_methods.rst
   * Add docstring examples

6. **Add citation**: Include reference paper/algorithm description

Release Process
---------------

For maintainers:

1. Update version in ``pyproject.toml`` and ``setup.py``

2. Update CHANGES_SUMMARY.md

3. Create git tag::

    git tag -a v0.2.0 -m "Release version 0.2.0"
    git push origin v0.2.0

4. Build distribution::

    python -m build

5. Upload to PyPI::

    twine upload dist/*

Code of Conduct
---------------

* Be respectful and inclusive
* Welcome newcomers
* Focus on constructive feedback
* Assume good intentions

License
-------

By contributing, you agree that your contributions will be licensed under the
GNU General Public License v3.0 with the same addendum as the original DIWASP:

* Use for educational purposes or scientific research without financial gain
* Written consent required for commercial use
* No warranties provided

Questions?
----------

If you have questions about contributing:

* Open a GitHub issue with the "question" label
* Check existing documentation
* Contact the maintainers

Thank you for contributing to pyDIWASP!

Installation
============

pyDIWASP can be installed from source or via pip (once published to PyPI).

Requirements
------------

pyDIWASP requires:

* Python 3.8 or later
* NumPy
* SciPy
* Matplotlib

From PyPI
---------

Once published, you can install pyDIWASP using pip::

    pip install pyDIWASP

From Source
-----------

To install from source:

1. Clone the repository::

    git clone https://github.com/SBFRF/pyDIWASP.git
    cd pyDIWASP

2. Install in development mode::

    pip install -e .

This installs the package in "editable" mode, so changes to the source code are immediately reflected without reinstalling.

For Contributors
----------------

If you plan to contribute to pyDIWASP, install the development dependencies::

    pip install -e .
    pip install pytest pytest-cov flake8

This includes testing and linting tools.

Verifying Installation
----------------------

To verify that pyDIWASP is correctly installed, run:

.. code-block:: python

    import pydiwasp
    print(pydiwasp.__version__)

You should see the version number printed without any errors.

You can also run the test suite::

    pytest tests/

Troubleshooting
---------------

**Import errors**

If you get import errors, make sure all dependencies are installed::

    pip install numpy scipy matplotlib

**Module not found**

If Python cannot find the pydiwasp module, ensure you're running Python from the correct environment where you installed the package.

Check your Python path::

    python -c "import sys; print(sys.path)"

The directory containing pydiwasp should be in this list.

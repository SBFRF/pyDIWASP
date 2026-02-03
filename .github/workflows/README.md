# GitHub Actions Workflows

This directory contains the CI/CD workflows for pyDIWASP.

## Workflows

### CI - Tests and Linting (`ci.yml`)

This workflow runs automatically on:
- Push to `main`, `master`, or `develop` branches
- Pull requests targeting `main`, `master`, or `develop` branches
- Manual trigger via workflow_dispatch

**What it does:**
- Tests the code on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- Runs flake8 linting to check code quality
- Runs the full test suite with pytest
- Generates code coverage reports
- Uploads coverage to Codecov (optional)

### Publish to PyPI (`publish.yml`)

This workflow can be triggered:
- Automatically when a new release is published on GitHub
- Manually via the Actions tab (workflow_dispatch)

**What it does:**
- Builds the Python distribution (sdist and wheel)
- Validates the distribution with twine
- Publishes to Test PyPI (if manually triggered with test_pypi=true)
- Publishes to PyPI (on release or manual trigger with test_pypi=false)

**Setup Required:**
To use the PyPI publishing workflow, you need to:
1. Create an API token on PyPI (https://pypi.org/manage/account/token/)
2. Add the token as a secret named `PYPI_API_TOKEN` in your repository settings
3. (Optional) Create a Test PyPI token and add as `TEST_PYPI_API_TOKEN` for testing

## Running Tests Locally

To run the tests locally:

```bash
# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov flake8

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=. --cov-report=term

# Run linting
flake8 . --exclude=.git,__pycache__,.pytest_cache,build,dist,*.egg-info
```

## Test Suite

The test suite includes:

1. **Core Tests** (`tests/test_core.py`):
   - Wavenumber calculations
   - Significant wave height calculations
   - Data validation functions
   - Transfer functions (elevation, pressure)

2. **API Tests** (`tests/test_api.py`):
   - Spectrum information extraction (infospec)
   - Spectrum interpolation (interpspec)
   - Spectrum file writing (writespec)

3. **Integration Tests** (`tests/test_integration.py`):
   - Full directional spectrum analysis workflow
   - Multiple estimation methods (IMLM, EMEP)
   - File I/O operations
   - Peak frequency detection
   - Data validation integration

**Total: 25 tests** documenting the existing capabilities of pyDIWASP.

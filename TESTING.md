# Test Suite and CI/CD Documentation

## Overview

This document describes the comprehensive test suite and CI/CD infrastructure added to the pyDIWASP project to document existing capabilities and ensure code quality.

## Test Suite

### Structure

The test suite is organized into three main test modules in the `tests/` directory:

#### 1. Core Tests (`tests/test_core.py`)
Tests for low-level utility functions and core calculations:

- **TestWavenumber**: Tests for wavenumber calculations
  - `test_wavenumber_basic`: Basic scalar input test
  - `test_wavenumber_array`: Array input handling
  - `test_wavenumber_deep_water`: Deep water approximation validation

- **TestHsig**: Tests for significant wave height calculations
  - `test_hsig_basic`: Basic Hsig calculation with synthetic spectrum
  - `test_hsig_zero_spectrum`: Edge case with zero energy

- **TestCheckData**: Tests for data validation functions
  - `test_check_instrument_data_valid`: Valid instrument data structure
  - `test_check_instrument_data_invalid_depth`: Invalid depth detection
  - `test_check_spectral_matrix_valid`: Valid spectral matrix structure
  - `test_check_estimation_parameters_defaults`: Default parameter setting
  - `test_check_estimation_parameters_invalid_method`: Invalid method detection

- **TestTransferFunctions**: Tests for wave transfer functions
  - `test_elev_transfer_function`: Surface elevation transfer function
  - `test_pres_transfer_function`: Pressure transfer function

**Total: 12 tests**

#### 2. API Tests (`tests/test_api.py`)
Tests for high-level API functions:

- **TestInfospec**: Tests for spectrum information extraction
  - `test_infospec_basic`: Basic information extraction (Hsig, Tp, DTp, Dp)
  - `test_infospec_returns_four_values`: Return value validation

- **TestInterpspec**: Tests for spectrum interpolation
  - `test_interpspec_basic`: Basic interpolation functionality
  - `test_interpspec_preserves_energy`: Energy conservation validation
  - `test_interpspec_no_interpolation_needed`: Same-grid handling

- **TestWritespec**: Tests for spectrum file output
  - `test_writespec_creates_file`: File creation and format validation
  - `test_writespec_handles_complex_spectrum`: Complex spectral values handling

**Total: 7 tests**

#### 3. Integration Tests (`tests/test_integration.py`)
Tests for complete workflow scenarios:

- **TestDirspecIntegration**: Full directional spectrum analysis
  - `test_dirspec_basic_run`: Basic end-to-end analysis
  - `test_dirspec_output_structure`: Output structure validation
  - `test_dirspec_with_different_methods`: Multiple estimation methods (IMLM, EMEP)
  - `test_dirspec_file_output`: File output functionality
  - `test_dirspec_detects_peak_frequency`: Peak frequency detection

- **TestDataValidationIntegration**: Data validation in workflow
  - `test_invalid_instrument_data_rejected`: Invalid data rejection

**Total: 6 tests**

### Test Coverage Summary

- **Total Tests**: 25
- **Coverage Areas**:
  - Wave physics calculations (wavenumber, wave height)
  - Data validation and error handling
  - Transfer functions (elevation, pressure)
  - Spectrum operations (interpolation, information extraction)
  - File I/O operations
  - Complete directional analysis workflow
  - Multiple estimation methods

### Running Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run specific test module
pytest tests/test_core.py -v

# Run with coverage
pytest tests/ -v --cov=. --cov-report=term --cov-report=html

# Run specific test
pytest tests/test_core.py::TestWavenumber::test_wavenumber_basic -v
```

## CI/CD Infrastructure

### GitHub Actions Workflows

#### 1. CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- Push to main/master/develop branches
- Pull requests to main/master/develop branches
- Manual trigger (workflow_dispatch)

**Jobs:**
- Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12 (matrix strategy)
- Code linting with flake8
- Test execution with pytest
- Code coverage generation
- Optional coverage upload to Codecov

**Steps:**
1. Checkout code
2. Set up Python environment
3. Install dependencies
4. Run flake8 linting
5. Run pytest test suite
6. Upload coverage (Python 3.11 only)

#### 2. PyPI Publishing Workflow (`.github/workflows/publish.yml`)

**Triggers:**
- GitHub release publication
- Manual trigger with Test PyPI option

**Jobs:**
- Build source distribution and wheel
- Validate distribution with twine
- Publish to Test PyPI (manual, optional)
- Publish to PyPI (on release or manual)

**Setup Required:**
- `PYPI_API_TOKEN`: PyPI API token (required for production)
- `TEST_PYPI_API_TOKEN`: Test PyPI token (optional, for testing)

**Steps:**
1. Checkout code
2. Set up Python
3. Install build tools
4. Build distribution packages
5. Check package validity
6. Publish to PyPI/Test PyPI

### Configuration Files

#### `pytest.ini`
- Defines test discovery patterns
- Configures test output format
- Sets up coverage exclusions

#### `setup.py`
- Package metadata and configuration
- Dependency specifications
- Entry points and classifiers
- Supports Python 3.7+

#### `requirements.txt`
- Runtime dependencies (numpy, scipy, matplotlib)
- Version constraints for compatibility

#### `.gitignore`
- Excludes build artifacts
- Excludes Python cache files
- Excludes virtual environments
- Excludes test artifacts

## Integration with GitHub

### Status Badges

The CI workflow provides a status badge that can be added to the README:

```markdown
[![CI](https://github.com/SBFRF/pyDIWASP/actions/workflows/ci.yml/badge.svg)](https://github.com/SBFRF/pyDIWASP/actions/workflows/ci.yml)
```

### Automated Quality Checks

Every pull request will automatically:
1. Run the full test suite on all supported Python versions
2. Check code quality with flake8
3. Report test results in the PR
4. Block merge if tests fail (optional)

### Release Process

To publish a new version to PyPI:

1. Update version in `setup.py`
2. Create a new release on GitHub with a tag (e.g., `v0.1.0`)
3. Workflow automatically builds and publishes to PyPI
4. Monitor the Actions tab for deployment status

## Benefits

### Documentation
- Tests serve as executable documentation of capabilities
- Clear examples of how to use each function
- Validation of expected behavior

### Quality Assurance
- Catch regressions early
- Ensure compatibility across Python versions
- Validate code quality standards

### Development Workflow
- Confidence in making changes
- Fast feedback on code modifications
- Automated testing on all contributions

### Distribution
- Streamlined release process
- Consistent package builds
- Easy publishing to PyPI

## Future Enhancements

Potential improvements to the test suite and CI/CD:

1. **Test Coverage**:
   - Add tests for remaining estimation methods (DFTM, EMLM, BDM)
   - Add tests for velocity transfer functions (velx, vely)
   - Add tests for plotspec function

2. **CI Enhancements**:
   - Add code coverage requirements (e.g., minimum 80%)
   - Add documentation generation and deployment
   - Add performance benchmarks
   - Add security scanning (e.g., bandit, safety)

3. **Quality Tools**:
   - Add type checking with mypy
   - Add code formatting with black
   - Add import sorting with isort
   - Add docstring validation

4. **Documentation**:
   - Generate API documentation with Sphinx
   - Add usage examples and tutorials
   - Create contribution guidelines

## Troubleshooting

### Common Issues

**Tests fail locally but pass in CI (or vice versa):**
- Ensure you have the same dependency versions
- Check Python version differences
- Verify environment variables

**Linting errors:**
- Run `flake8 .` locally to see all issues
- Use `--exclude` to ignore directories
- Fix critical errors (E9, F63, F7, F82) first

**PyPI publishing fails:**
- Verify API token is set correctly
- Check package name availability on PyPI
- Ensure version number is incremented
- Validate package with `twine check dist/*`

## Contact

For questions or issues with the test suite or CI/CD setup, please open an issue on GitHub.

# Contributing to pyDIWASP

Thank you for your interest in contributing to pyDIWASP! This guide will help you get started.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pyDIWASP.git
   cd pyDIWASP
   ```

2. **Create a Virtual Environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8
   ```

## Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new functionality

3. **Run Tests**
   ```bash
   # Run all tests
   pytest tests/ -v
   
   # Run specific test file
   pytest tests/test_core.py -v
   
   # Run with coverage
   pytest tests/ -v --cov=. --cov-report=term
   ```

4. **Check Code Quality**
   ```bash
   # Check for critical errors
   flake8 . --select=E9,F63,F7,F82 --exclude=.git,__pycache__,.pytest_cache
   
   # Check all style issues
   flake8 . --exclude=.git,__pycache__,.pytest_cache
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Clear description of your changes"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

## Testing Guidelines

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names: `test_<what>_<scenario>`
- Group related tests in classes: `TestFeatureName`
- Include docstrings explaining what is being tested

Example:
```python
class TestNewFeature:
    """Tests for the new feature."""
    
    def test_new_feature_basic(self):
        """Test basic functionality of new feature."""
        result = new_feature(input_data)
        assert result == expected_output
```

### Test Categories

- **Unit Tests**: Test individual functions in isolation
- **API Tests**: Test high-level interfaces
- **Integration Tests**: Test complete workflows

## Code Style

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add tests for new features
4. Describe your changes clearly in the PR description
5. Link to any related issues

## Continuous Integration

All pull requests will automatically:
- Run tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
- Check code quality with flake8
- Report test coverage

Make sure your changes pass all checks before requesting review.

## Questions?

- Open an issue for bugs or feature requests
- Check existing issues for similar problems
- Read the [TESTING.md](TESTING.md) for detailed test documentation

Thank you for contributing!

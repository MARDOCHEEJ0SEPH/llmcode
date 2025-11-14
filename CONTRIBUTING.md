# Contributing to LLMCode

Thank you for your interest in contributing to LLMCode! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/llmcode.git
   cd llmcode
   ```

2. **Set up development environment**
   ```bash
   bash setup.sh
   # or
   make setup
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Follow the project's code style
   - Add tests for new functionality

3. **Test your changes**
   ```bash
   make test
   ```

4. **Format and lint**
   ```bash
   make format
   make lint
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- **Formatting**: Use Black with 100 character line length
- **Linting**: Pass Ruff checks
- **Type Hints**: Add type hints to all functions
- **Docstrings**: Use Google-style docstrings

### Example

```python
def example_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    Brief description of what the function does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When something is wrong
    """
    pass
```

## Adding New Tools

To add a new tool:

1. Create a new class in `llmcode/tools/` that inherits from `Tool`
2. Implement required methods: `name`, `description`, `input_schema`, `execute`
3. Add comprehensive docstrings
4. Register the tool in `LLMCodeCLI._register_tools()`
5. Add tests in `tests/test_tools.py`
6. Update documentation in `README.md` and `CLAUDE.md`

See `examples/custom_tool.py` for a complete example.

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=llmcode

# Run specific test file
pytest tests/test_tools.py

# Run specific test
pytest tests/test_tools.py::TestReadTool::test_read_existing_file
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Use fixtures for common setup

## Documentation

When adding features:

1. Update `README.md` with user-facing documentation
2. Update `CLAUDE.md` with technical details for AI assistants
3. Add docstrings to all new code
4. Include examples in `examples/` directory if appropriate

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted with Black
- [ ] Code passes Ruff linting
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive

### PR Description

Include:
- What changes were made
- Why the changes were made
- Any breaking changes
- How to test the changes

## Code Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, a maintainer will merge your PR

## Reporting Issues

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)
- Error messages or logs

### Feature Requests

Include:
- Description of the feature
- Use case / motivation
- Proposed implementation (if applicable)
- Any alternatives considered

## Community Guidelines

- Be respectful and constructive
- Follow the code of conduct
- Help others when you can
- Give credit where it's due

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

If you have questions, feel free to:
- Open an issue
- Start a discussion
- Reach out to the maintainers

Thank you for contributing to LLMCode!

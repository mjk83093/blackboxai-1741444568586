# Contributing to Work Production AI Agent

We love your input! We want to make contributing to Work Production AI Agent as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/work-production-ai.git
cd work-production-ai
```

2. Run the setup script:
```bash
./scripts/setup.sh
```

3. Create a branch:
```bash
git checkout -b feature/your-feature-name
```

## Code Style

We use several tools to maintain code quality:

- `black` for Python code formatting
- `flake8` for Python code linting
- `isort` for import sorting
- `mypy` for type checking

Run the following before committing:
```bash
# Format code
black .

# Sort imports
isort .

# Run linter
flake8 .

# Type checking
mypy .
```

## Testing

We use `pytest` for testing. To run tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_specific.py
```

### Writing Tests

- Place tests in the `tests` directory
- Name test files with `test_` prefix
- Use descriptive test names
- Include both positive and negative test cases
- Mock external services

Example test:
```python
def test_document_creation():
    """Test document creation with valid data."""
    document = DocumentService.create(
        title="Test Doc",
        content="Test Content"
    )
    assert document.title == "Test Doc"
    assert document.content == "Test Content"
```

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the docs/ with any new information
3. The PR will be merged once you have the sign-off of two other developers
4. PR titles should follow [Conventional Commits](https://www.conventionalcommits.org/)

### PR Title Format
```
type(scope): description

Examples:
feat(auth): add Microsoft OAuth support
fix(docs): correct API endpoint documentation
chore(deps): update dependencies
```

## Issue Reporting

### Bug Reports
When filing an issue, make sure to answer these questions:

1. What version of the software are you using?
2. What operating system and processor architecture are you using?
3. What did you do?
4. What did you expect to see?
5. What did you see instead?

### Feature Requests
Feature requests are welcome! Provide the following information:

1. Clear use case
2. Proposed solution
3. Alternative solutions considered
4. Additional context

## Documentation

### API Documentation
- Update API_REFERENCE.md for endpoint changes
- Include request/response examples
- Document all parameters
- Note any breaking changes

### Code Documentation
- Use docstrings for functions and classes
- Include type hints
- Document exceptions
- Add inline comments for complex logic

Example:
```python
def process_document(
    content: str,
    format: str = "text"
) -> Dict[str, Any]:
    """
    Process document content with AI analysis.

    Args:
        content: Document content to process
        format: Content format ('text' or 'html')

    Returns:
        Dict containing processed content and metadata

    Raises:
        ValueError: If format is not supported
    """
    ...
```

## Community

### Code of Conduct
This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

### Communication
- GitHub Issues: Bug reports and feature requests
- Discussions: General questions and discussions
- Pull Requests: Code review and submission
- Email: security@workproduction.ai for security issues

## License
By contributing, you agree that your contributions will be licensed under the project's MIT License.

## Questions?
Don't hesitate to ask questions by opening an issue or starting a discussion.

Thank you for contributing to Work Production AI Agent! 🚀

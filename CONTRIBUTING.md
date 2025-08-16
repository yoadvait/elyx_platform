# Contributing to Elyx Platform

We love your input! We want to make contributing to Elyx Platform as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with GitHub

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [GitHub Flow](https://guides.github.com/introduction/flow/index.html)

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

1. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/elyx_platform.git
   cd elyx_platform
   ```

2. **Set up the backend**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the frontend**:
   ```bash
   cd frontend
   npm install
   ```

4. **Set up environment variables**:
   ```bash
   cp env.template .env
   # Edit .env with your API keys
   ```

5. **Run tests**:
   ```bash
   pytest tests/
   cd frontend && npm test
   ```

## Code Style

### Python
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where possible
- Add docstrings to all public functions and classes
- Maximum line length: 100 characters

### TypeScript/JavaScript
- Follow the existing ESLint configuration
- Use TypeScript for all new code
- Prefer functional components with hooks
- Use meaningful variable and function names

### Commit Messages
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=agents --cov=backend --cov=data
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Documentation

- Update the README.md if you change functionality
- Add docstrings to new functions and classes
- Update API documentation for endpoint changes
- Include examples for new features

## Issue and Feature Request Process

### Bug Reports
Use the bug report template and include:
- A quick summary and/or background
- Steps to reproduce (be specific!)
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening)

### Feature Requests
Use the feature request template and include:
- A clear and concise description of what the problem is
- A clear and concise description of what you want to happen
- Describe alternatives you've considered
- Any additional context or screenshots

## Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
Examples of behavior that contributes to creating a positive environment include:
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue with the "question" label or reach out to the maintainers directly.

Thank you for contributing to Elyx Platform! 🚀

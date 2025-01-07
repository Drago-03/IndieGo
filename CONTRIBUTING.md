# Contributing to DevAssist Bot

First off, thank you for considering contributing to DevAssist Bot! It's people like you that make DevAssist Bot such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/your-username/devassist-bot/issues)
2. If not, create a new issue using the bug report template
3. Include as much relevant information as possible:
   - Python version
   - Operating system
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Error messages

### Suggesting Enhancements

1. Check existing [Issues](https://github.com/your-username/devassist-bot/issues) for similar suggestions
2. Create a new issue using the feature request template
3. Describe the feature in detail:
   - Use cases
   - Expected behavior
   - Potential implementation approach

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Update documentation
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

1. Clone your fork:

   ```bash
   git clone https://github.com/your-username/devassist-bot.git
   cd devassist-bot
   ```

2. Create virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. Set up pre-commit hooks:

   ```bash
   pre-commit install
   ```

## Coding Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints
- Write docstrings for functions and classes
- Add tests for new features
- Keep functions small and focused
- Use meaningful variable names

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Maintain test coverage above 80%
- Use pytest for testing

## Documentation

- Update relevant documentation
- Add docstrings to new functions/classes
- Update README if needed
- Add examples for new features

## Git Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Reference issues and pull requests
- Keep first line under 72 characters
- Describe what and why, not how

## Review Process

1. Automated checks must pass
2. Code review by maintainers
3. Documentation review
4. Test coverage verification
5. Final approval

## Community

- Join our [Discord server](https://discord.gg/your-invite)
- Follow our [Twitter](https://twitter.com/your-handle)
- Read our [blog](https://your-blog.com)

## Recognition

Contributors will be:

- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given special Discord roles

Thank you for contributing!

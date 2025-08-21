# Contributing to Automated Marketing Agent

Thank you for your interest in contributing to the Automated Marketing Agent! 🎉

## 🚀 Quick Start

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch
4. **Make** your changes
5. **Test** your changes
6. **Submit** a pull request

## 📋 Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/automated-marketing-agent.git
cd automated-marketing-agent

# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
alembic upgrade head
python -m app.core.init_db

# Run tests
pytest
```

## 🎯 Contributing Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use type hints for all functions
- Write comprehensive docstrings
- Keep functions and classes focused and small

### Testing
- Write tests for new features
- Ensure existing tests pass
- Aim for 80%+ test coverage
- Test both success and error cases

### Documentation
- Update README.md for new features
- Add docstrings to all functions/classes
- Update API documentation if needed
- Include examples where helpful

### Commit Messages
Use conventional commit format:
```
feat: add new social media platform integration
fix: resolve authentication token refresh issue
docs: update API documentation
test: add tests for content generation
```

## 🐛 Reporting Issues

When reporting issues, please include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Error messages and logs

## 💡 Feature Requests

We welcome feature requests! Please:
- Check existing issues first
- Describe the use case
- Explain why it would be valuable
- Consider implementation complexity

## 📝 Pull Request Process

1. **Update** documentation as needed
2. **Add** tests for new functionality
3. **Ensure** all tests pass
4. **Update** the changelog if applicable
5. **Request** review from maintainers

## 🏆 Recognition

Contributors will be:
- Listed in the README contributors section
- Mentioned in release notes
- Invited to our contributor Discord channel

## 📞 Getting Help

- 💬 [GitHub Discussions](https://github.com/yourusername/automated-marketing-agent/discussions)
- 📧 Email: contributors@yourcompany.com
- 💻 Discord: [Join our server](https://discord.gg/yourserver)

## 📜 Code of Conduct

Please be respectful and inclusive. We're building a welcoming community for everyone.

Thank you for contributing! 🙏

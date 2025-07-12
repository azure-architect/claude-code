# Python Project Template

A comprehensive, production-ready Python project template with best practices, automated tooling, and Claude Code integration.

## ✨ Features

- **🏗️ Modern Project Structure**: Standard `src/` layout with proper packaging
- **🔧 Complete Tooling Setup**: Black, isort, mypy, pylint, pytest, pre-commit
- **🤖 Claude Code Integration**: Advanced hooks and command templates
- **📦 Dependency Management**: pyproject.toml with optional dependencies
- **🚀 One-Command Setup**: Automated project initialization script
- **🔒 Security Best Practices**: Bandit, secure coding patterns
- **📊 Test Coverage**: pytest with coverage reporting
- **🐳 Docker Ready**: Configuration for containerized development
- **⚡ CI/CD Ready**: GitHub Actions workflows included

## 🚀 Quick Start

### 1. Use This Template

```bash
# Clone or copy this template to your new project directory
cp -r /path/to/this/template /path/to/your/new/project
cd /path/to/your/new/project
```

### 2. Initialize Your Project

```bash
# Run the initialization script
python scripts/init_project.py \
    --project-name "my-awesome-project" \
    --author-name "Your Name" \
    --author-email "your.email@example.com"
```

This will:
- ✅ Customize project files with your information
- ✅ Initialize git repository with initial commit
- ✅ Create virtual environment (`.venv/`)
- ✅ Install all dependencies
- ✅ Setup pre-commit hooks
- ✅ Run initial validation

### 3. Start Developing

```bash
# Activate virtual environment
source .venv/bin/activate

# Start coding in src/
# Add tests in tests/
# Run development commands as needed
```

## 🛠️ Development Commands

### Code Quality
```bash
black .              # Format code
isort .              # Sort imports
mypy src             # Type checking
pylint src           # Linting
bandit -r src        # Security scanning
```

### Testing
```bash
pytest               # Run tests
pytest --cov=src     # Run tests with coverage
pytest -v            # Verbose test output
pytest -k "test_name" # Run specific tests
```

### Pre-commit
```bash
pre-commit install     # Install hooks
pre-commit run --all-files  # Run on all files
```

### Documentation
```bash
# If using Sphinx (optional)
cd docs
make html
```

## 📁 Project Structure

```
.
├── .claude/                 # Claude Code configuration
│   ├── commands/           # Reusable command templates
│   ├── hooks/              # Pre/post tool execution hooks
│   └── settings.json       # Claude Code settings
├── .github/                # GitHub Actions workflows
│   └── workflows/
├── docs/                   # Documentation
├── src/                    # Source code
│   └── __init__.py
├── tests/                  # Test files
│   ├── __init__.py
│   └── conftest.py
├── scripts/                # Utility scripts
│   └── init_project.py     # Project initialization
├── .gitignore             # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit configuration
├── docker-compose.yml     # Docker services
├── Dockerfile             # Docker image
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## 🔧 Configuration Details

### pyproject.toml
- **Build system**: setuptools with wheel
- **Dependencies**: Organized with optional groups (dev, docs, test)
- **Tool configuration**: Black, isort, mypy, pytest, coverage, pylint, bandit
- **Project metadata**: Author, license, classifiers

### Pre-commit Hooks
- **black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking
- **pylint**: Code linting
- **bandit**: Security scanning
- **trailing-whitespace**: Remove trailing spaces
- **end-of-file-fixer**: Ensure files end with newline

### Claude Code Integration
- **Validation hooks**: Enforce code quality before writing files
- **Command templates**: `/document`, `/implement`, `/test` commands
- **Security checks**: Block `os.system()`, require SSL for email clients
- **File length limits**: 500 lines maximum per file
- **Type annotation enforcement**: All functions must have return types

## 🐳 Docker Development

```bash
# Build development image
docker build -t my-project .

# Run development container
docker-compose up -d

# Execute commands in container
docker-compose exec app bash
```

## 🚀 CI/CD Pipeline

The included GitHub Actions workflow provides:
- ✅ Multi-Python version testing (3.9, 3.10, 3.11, 3.12)
- ✅ Code quality checks (black, isort, mypy, pylint)
- ✅ Security scanning (bandit)
- ✅ Test execution with coverage reporting
- ✅ Documentation building
- ✅ Artifact uploading

## 📋 Best Practices Enforced

### Code Quality
- **Type annotations**: All functions must have return type annotations
- **Line length**: 88 characters (Black standard)
- **Import organization**: isort with Black profile
- **Docstrings**: Required for all public functions and classes
- **Error handling**: Proper exception handling patterns

### Security
- **No `os.system()`**: Use subprocess instead
- **SSL required**: For email and network clients
- **Secret scanning**: Bandit security linting
- **Dependency scanning**: Via GitHub Actions (optional)

### Testing
- **90%+ coverage**: Enforced via pytest-cov
- **Test organization**: Unit, integration, and slow test markers
- **Fixtures**: Shared test fixtures in conftest.py
- **Mocking**: Proper dependency isolation

### Documentation
- **README**: Comprehensive project documentation
- **Docstrings**: All public APIs documented
- **Type hints**: Self-documenting code via types
- **CLAUDE.md**: Development guidance for Claude Code

## 🎯 Development Workflow

1. **Start feature**: Create branch, activate venv
2. **Write code**: In `src/` with proper types and docstrings
3. **Write tests**: In `tests/` with good coverage
4. **Pre-commit check**: Hooks run automatically
5. **Run tests**: `pytest` with coverage
6. **Code review**: CI checks pass automatically
7. **Deploy**: Merge to main triggers deployment

## 🔄 Template Updates

To update projects created from this template:

1. **Check CLAUDE.md**: Review any new development patterns
2. **Update pyproject.toml**: Compare tool configurations
3. **Update CI/CD**: Check for new GitHub Actions workflows
4. **Update hooks**: Check `.claude/hooks/` for improvements

## 📚 Documentation

### Usage Documentation
- **[Usage Guide](docs/usage.md)** - Complete step-by-step coding workflow
- **[Examples & Tutorials](docs/examples.md)** - Practical examples (REST API, Data Pipeline, CLI)
- **[Claude Code Workflow](docs/claude-code-workflow.md)** - Advanced Claude Code integration
- **[Development Guide](docs/development.md)** - Detailed development patterns
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

### External Resources
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pre-commit Documentation](https://pre-commit.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the full test suite
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy coding! 🎉**

This template provides everything you need for professional Python development with Claude Code integration.
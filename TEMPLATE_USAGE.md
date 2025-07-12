# 🚀 How to Use This Python Project Template

This repository is a comprehensive Python project template with Claude Code integration. Use it as the foundation for all your Python projects.

## 📦 Quick Start

### Option 1: GitHub Template (Recommended)
```bash
# 1. Click "Use this template" on GitHub
# 2. Create your new repository
# 3. Clone your new repository
git clone https://github.com/YOUR_USERNAME/YOUR_NEW_PROJECT.git
cd YOUR_NEW_PROJECT

# 4. Initialize the project
python scripts/init_project.py \
    --project-name "your-project-name" \
    --author-name "Your Name" \
    --author-email "your.email@example.com"
```

### Option 2: Direct Clone
```bash
# 1. Clone this template
git clone https://github.com/azure-architect/claude-code.git your-new-project
cd your-new-project

# 2. Remove original git history and start fresh
rm -rf .git
git init

# 3. Initialize the project
python scripts/init_project.py \
    --project-name "your-project-name" \
    --author-name "Your Name" \
    --author-email "your.email@example.com"
```

## 🎯 What the Initialization Script Does

The `init_project.py` script automatically:
- ✅ Customizes all template files with your project details
- ✅ Creates virtual environment (`.venv/`)
- ✅ Installs all development dependencies
- ✅ Sets up pre-commit hooks
- ✅ Initializes git repository with initial commit
- ✅ Runs quality validation

## 📁 Template Structure

```
your-new-project/
├── 📋 Project Configuration
│   ├── pyproject.toml           # Complete Python project config
│   ├── .pre-commit-config.yaml  # Code quality hooks
│   ├── .gitignore              # Comprehensive gitignore
│   └── LICENSE                 # MIT license
│
├── 🤖 Claude Code Integration
│   └── .claude/
│       ├── settings.json       # Claude Code configuration
│       ├── commands/           # Reusable command templates
│       └── hooks/             # Validation and formatting hooks
│
├── 🏗️ Project Structure
│   ├── src/                   # Your Python code goes here
│   ├── tests/                 # Your tests go here
│   ├── docs/                  # Documentation
│   └── scripts/               # Utility scripts
│
├── 🐳 Containerization
│   ├── Dockerfile             # Multi-stage Docker build
│   └── docker-compose.yml     # Development environment
│
├── 🚀 CI/CD
│   └── .github/workflows/ci.yml # GitHub Actions pipeline
│
└── 📚 Documentation
    ├── README.md              # Project documentation
    ├── docs/usage.md         # Complete coding workflow
    ├── docs/examples.md      # Practical tutorials
    └── docs/troubleshooting.md # Problem solving
```

## 🔄 Development Workflow

### 1. Daily Development
```bash
# Activate environment
source .venv/bin/activate

# Start coding in src/
# Add tests in tests/
# Use Claude Code commands for assistance
```

### 2. Quality Assurance
```bash
# Run complete quality check
./scripts/qa_check.sh

# Individual tools
black .                    # Format code
isort .                    # Sort imports
mypy src                   # Type checking
pylint src                 # Linting
pytest --cov=src          # Tests with coverage
```

### 3. Claude Code Integration
```bash
# Use powerful Claude Code commands:
/implement "Create user authentication with JWT"
/test "src/auth.py"
/document "Authentication system"
```

## 🎨 Customization

### Update Project Metadata
Edit these files after initialization:
- `pyproject.toml` - Project name, description, dependencies
- `README.md` - Project-specific documentation
- `src/__init__.py` - Package version and description

### Add Dependencies
```bash
# Add to pyproject.toml
dependencies = [
    "requests>=2.31.0",
    "fastapi>=0.104.0",
]

# Install
pip install -e .[dev,test,docs]
```

### Configure Tools
All tools are configured in `pyproject.toml`:
- **Black**: Code formatting
- **isort**: Import sorting
- **mypy**: Type checking
- **pylint**: Code linting
- **pytest**: Testing framework
- **coverage**: Test coverage

## 🚀 Deployment Options

### Local Development
```bash
# Run locally
python -m src.main

# Or with Docker
docker-compose up
```

### Production Deployment
```bash
# Build package
python -m build

# Build Docker image
docker build -t your-project .

# Deploy to cloud (AWS, GCP, Azure)
# Follow cloud-specific deployment guides
```

## 📊 Features Included

### ✅ Code Quality
- **Black** - Uncompromising code formatting
- **isort** - Import sorting
- **mypy** - Static type checking
- **pylint** - Code analysis
- **bandit** - Security linting
- **pre-commit** - Git hooks

### ✅ Testing
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **pytest-xdist** - Parallel testing
- **Test fixtures** - Reusable test components

### ✅ Documentation
- **Comprehensive guides** - Step-by-step workflows
- **Examples** - Real-world tutorials
- **API documentation** - Automatic generation
- **Troubleshooting** - Common issues and solutions

### ✅ DevOps
- **GitHub Actions** - CI/CD pipeline
- **Docker** - Containerization
- **Multi-platform** - Linux, macOS, Windows
- **Multi-Python** - 3.9, 3.10, 3.11, 3.12

### ✅ Claude Code Integration
- **Validation hooks** - Enforce quality standards
- **Command templates** - Structured development
- **Security patterns** - Best practices enforcement
- **Type annotation** - Automatic enforcement

## 🎯 Best Practices Enforced

### Code Quality
- **Type annotations required** - All functions must have return types
- **500-line file limit** - Enforced modularity
- **Security patterns** - No `os.system()`, SSL required
- **Documentation** - Comprehensive docstrings

### Development Workflow
- **Test-driven development** - Write tests first
- **Continuous integration** - Automated quality checks
- **Version control** - Meaningful commit messages
- **Code review** - Pull request workflow

## 🆘 Getting Help

### Documentation
- **[Usage Guide](docs/usage.md)** - Complete workflow
- **[Examples](docs/examples.md)** - Practical tutorials
- **[Troubleshooting](docs/troubleshooting.md)** - Problem solving

### Support
- **GitHub Issues** - Report bugs or request features
- **Claude Code docs** - https://docs.anthropic.com/claude-code
- **Python community** - Stack Overflow, Discord

## 🔄 Template Updates

Keep your projects updated with template improvements:

```bash
# Check for template updates
git remote add template https://github.com/azure-architect/claude-code.git
git fetch template

# Merge updates (carefully)
git merge template/main --allow-unrelated-histories
```

## 🎉 Success Stories

This template helps you:
- **Ship faster** - Skip boilerplate setup
- **Higher quality** - Automated quality enforcement
- **Consistent patterns** - Same structure across projects
- **Better documentation** - Built-in guides and examples
- **Team productivity** - Onboard developers quickly

---

## 🚀 Ready to Build Amazing Python Projects!

This template provides everything you need for professional Python development with Claude Code integration. Start building! 🎯
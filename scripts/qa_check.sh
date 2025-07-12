#!/bin/bash
# Complete quality assurance check script

set -e  # Exit on any error

echo "🔍 Running Quality Assurance Checks..."
echo "======================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Warning: Virtual environment not activated"
    echo "   Please run: source .venv/bin/activate"
    exit 1
fi

echo "📝 Checking code formatting..."
if black --check .; then
    echo "✅ Code formatting passed"
else
    echo "❌ Code formatting failed"
    echo "   Run: black ."
    exit 1
fi

echo ""
echo "📦 Checking import sorting..."
if isort --check-only .; then
    echo "✅ Import sorting passed"
else
    echo "❌ Import sorting failed"
    echo "   Run: isort ."
    exit 1
fi

echo ""
echo "🔍 Type checking..."
if mypy src; then
    echo "✅ Type checking passed"
else
    echo "❌ Type checking failed"
    echo "   Fix type annotations and try again"
    exit 1
fi

echo ""
echo "🔍 Linting code..."
if pylint src; then
    echo "✅ Code linting passed"
else
    echo "❌ Code linting failed"
    echo "   Fix linting issues and try again"
    exit 1
fi

echo ""
echo "🔒 Security scanning..."
if bandit -r src -q; then
    echo "✅ Security scanning passed"
else
    echo "❌ Security issues found"
    echo "   Review bandit output and fix security issues"
    exit 1
fi

echo ""
echo "🧪 Running tests with coverage..."
if pytest --cov=src --cov-report=term-missing --cov-fail-under=90 -q; then
    echo "✅ Tests and coverage passed"
else
    echo "❌ Tests failed or coverage below 90%"
    echo "   Fix failing tests or add more test coverage"
    exit 1
fi

echo ""
echo "🎉 All quality checks passed!"
echo "✅ Code is ready for commit/deployment"
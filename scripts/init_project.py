#!/usr/bin/env python3
"""Project initialization script for Python project template."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


def run_command(cmd: List[str], cwd: Optional[Path] = None) -> bool:
    """Run a shell command and return success status."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, check=True, capture_output=True, text=True
        )
        print(f"✓ {' '.join(cmd)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {' '.join(cmd)}")
        print(f"  Error: {e.stderr}")
        return False


def init_git_repo(project_path: Path) -> bool:
    """Initialize git repository."""
    print("🔧 Initializing git repository...")

    commands = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "Initial commit: Python project template setup"],
    ]

    for cmd in commands:
        if not run_command(cmd, cwd=project_path):
            return False

    print("✓ Git repository initialized")
    return True


def setup_virtual_environment(project_path: Path) -> bool:
    """Create and setup virtual environment."""
    print("🐍 Setting up virtual environment...")

    venv_path = project_path / ".venv"

    commands = [
        [sys.executable, "-m", "venv", str(venv_path)],
    ]

    for cmd in commands:
        if not run_command(cmd, cwd=project_path):
            return False

    # Determine activation script based on OS
    if os.name == "nt":  # Windows
        activate_script = venv_path / "Scripts" / "activate.bat"
        pip_cmd = [str(venv_path / "Scripts" / "pip")]
    else:  # Unix/macOS
        activate_script = venv_path / "bin" / "activate"
        pip_cmd = [str(venv_path / "bin" / "pip")]

    # Install development dependencies
    install_cmd = pip_cmd + ["install", "-e", ".[dev,docs,test]"]
    if not run_command(install_cmd, cwd=project_path):
        return False

    print("✓ Virtual environment created and dependencies installed")
    print(f"📍 Activate with: source {activate_script}")
    return True


def setup_pre_commit(project_path: Path) -> bool:
    """Setup pre-commit hooks."""
    print("🪝 Setting up pre-commit hooks...")

    venv_path = project_path / ".venv"
    if os.name == "nt":  # Windows
        pre_commit_cmd = [str(venv_path / "Scripts" / "pre-commit")]
    else:  # Unix/macOS
        pre_commit_cmd = [str(venv_path / "bin" / "pre-commit")]

    commands = [
        pre_commit_cmd + ["install"],
        pre_commit_cmd + ["run", "--all-files"],
    ]

    for cmd in commands:
        if not run_command(cmd, cwd=project_path):
            return False

    print("✓ Pre-commit hooks installed and configured")
    return True


def customize_project(
    project_path: Path, project_name: str, author_name: str, author_email: str
) -> bool:
    """Customize project files with user information."""
    print("📝 Customizing project files...")

    # Update pyproject.toml
    pyproject_file = project_path / "pyproject.toml"
    if pyproject_file.exists():
        content = pyproject_file.read_text()
        content = content.replace(
            'name = "python-project-template"', f'name = "{project_name}"'
        )
        content = content.replace('name = "Your Name"', f'name = "{author_name}"')
        content = content.replace(
            'email = "your.email@example.com"', f'email = "{author_email}"'
        )
        content = content.replace(
            "yourusername/python-project-template",
            f'{author_name.lower().replace(" ", "")}/{project_name}',
        )
        pyproject_file.write_text(content)

    # Update package __init__.py
    init_file = project_path / "src" / "__init__.py"
    if init_file.exists():
        content = init_file.read_text()
        content = content.replace(
            '"Python project template package."', f'"{project_name} package."'
        )
        init_file.write_text(content)

    print("✓ Project files customized")
    return True


def run_initial_tests(project_path: Path) -> bool:
    """Run initial tests to verify setup."""
    print("🧪 Running initial tests...")

    venv_path = project_path / ".venv"
    if os.name == "nt":  # Windows
        pytest_cmd = [str(venv_path / "Scripts" / "pytest")]
        black_cmd = [str(venv_path / "Scripts" / "black")]
        mypy_cmd = [str(venv_path / "Scripts" / "mypy")]
    else:  # Unix/macOS
        pytest_cmd = [str(venv_path / "bin" / "pytest")]
        black_cmd = [str(venv_path / "bin" / "black")]
        mypy_cmd = [str(venv_path / "bin" / "mypy")]

    commands = [
        black_cmd + ["--check", "."],
        mypy_cmd + ["src"],
        pytest_cmd + ["--version"],  # Just check pytest works
    ]

    for cmd in commands:
        if not run_command(cmd, cwd=project_path):
            print(f"⚠️  Warning: {' '.join(cmd)} failed, but continuing...")

    print("✓ Initial verification complete")
    return True


def main() -> None:
    """Main initialization function."""
    parser = argparse.ArgumentParser(description="Initialize a new Python project")
    parser.add_argument("--project-name", required=True, help="Name of the project")
    parser.add_argument("--author-name", required=True, help="Author name")
    parser.add_argument("--author-email", required=True, help="Author email")
    parser.add_argument(
        "--skip-git", action="store_true", help="Skip git initialization"
    )
    parser.add_argument(
        "--skip-venv", action="store_true", help="Skip virtual environment setup"
    )
    parser.add_argument(
        "--skip-pre-commit", action="store_true", help="Skip pre-commit setup"
    )

    args = parser.parse_args()

    project_path = Path.cwd()

    print(f"🚀 Initializing Python project: {args.project_name}")
    print(f"📁 Project path: {project_path}")

    # Customize project files
    if not customize_project(
        project_path, args.project_name, args.author_name, args.author_email
    ):
        sys.exit(1)

    # Initialize git repository
    if not args.skip_git:
        if not init_git_repo(project_path):
            print("⚠️  Git initialization failed, continuing...")

    # Setup virtual environment
    if not args.skip_venv:
        if not setup_virtual_environment(project_path):
            print("❌ Virtual environment setup failed")
            sys.exit(1)

    # Setup pre-commit hooks
    if not args.skip_pre_commit and not args.skip_venv:
        if not setup_pre_commit(project_path):
            print("⚠️  Pre-commit setup failed, continuing...")

    # Run initial tests
    if not args.skip_venv:
        run_initial_tests(project_path)

    print("\n🎉 Project initialization complete!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment: source .venv/bin/activate")
    print("2. Start coding in src/")
    print("3. Add tests in tests/")
    print("4. Run tests: pytest")
    print("5. Format code: black .")
    print("6. Type check: mypy src")
    print("7. Lint code: pylint src")


if __name__ == "__main__":
    main()

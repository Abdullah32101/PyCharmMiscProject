#!/usr/bin/env python3
"""
Development Environment Setup Script
Installs all required tools for local development and CI/CD compatibility.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Set up development environment"""
    print("🚀 Setting up development environment...")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    
    # Upgrade pip
    run_command("python -m pip install --upgrade pip", "Upgrading pip")
    
    # Install development dependencies
    dev_dependencies = [
        "flake8",
        "black", 
        "isort",
        "mypy",
        "pylint",
        "bandit",
        "pytest",
        "pytest-cov",
        "pytest-html",
        "pytest-timeout",
        "selenium",
        "webdriver-manager",
        "mysql-connector-python"
    ]
    
    print("\n📦 Installing development dependencies...")
    for dep in dev_dependencies:
        run_command(f"pip install {dep}", f"Installing {dep}")
    
    # Install project dependencies
    print("\n📦 Installing project dependencies...")
    run_command("pip install -r requirements.txt", "Installing project requirements")
    
    # Verify tools are installed
    print("\n🔍 Verifying tool installation...")
    tools = ["flake8", "black", "isort", "mypy", "pylint", "bandit"]
    
    for tool in tools:
        try:
            result = subprocess.run([tool, "--version"], capture_output=True, text=True)
            version = result.stdout.strip().split('\n')[0]
            print(f"✅ {tool}: {version}")
        except FileNotFoundError:
            print(f"❌ {tool}: Not found")
    
    print("\n🎉 Development environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Run: black .")
    print("2. Run: isort .")
    print("3. Run: flake8 .")
    print("4. Run: mypy . --ignore-missing-imports")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
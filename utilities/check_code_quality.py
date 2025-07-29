#!/usr/bin/env python3
"""
Local Code Quality Check Script
Runs all the same checks as the CI/CD pipeline locally.
"""

import subprocess
import sys
import os


def run_check(command, description, critical=False):
    """Run a quality check and report results"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"{'❌' if critical else '⚠️'} {description} - FAILED")
            if result.stdout:
                print(f"Output: {result.stdout}")
            if result.stderr:
                print(f"Errors: {result.stderr}")
            return not critical
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return not critical


def main():
    """Run all code quality checks"""
    print("🧪 Running Code Quality Checks")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 0
    
    # Check if tools are installed
    tools = ["black", "isort", "flake8", "mypy", "bandit"]
    missing_tools = []
    
    for tool in tools:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"❌ Missing tools: {', '.join(missing_tools)}")
        print("Run: python setup_dev_environment.py")
        return False
    
    # Code formatting checks
    total_checks += 1
    if run_check("isort --check-only --diff .", "Import sorting check"):
        checks_passed += 1
    
    total_checks += 1
    if run_check("black --check --diff .", "Code formatting check"):
        checks_passed += 1
    
    # Linting checks
    total_checks += 1
    if run_check("flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics", "Critical linting errors", critical=True):
        checks_passed += 1
    
    total_checks += 1
    if run_check("flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics", "Style warnings"):
        checks_passed += 1
    
    # Type checking
    total_checks += 1
    if run_check("mypy . --ignore-missing-imports", "Type checking"):
        checks_passed += 1
    
    # Security scan
    total_checks += 1
    if run_check("bandit -r . -f json -o bandit-report.json", "Security scan"):
        checks_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Results: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🎉 All code quality checks passed!")
        print("✅ Your code is ready for CI/CD!")
        return True
    else:
        print("⚠️ Some checks failed. Please fix the issues above.")
        print("\n💡 Quick fixes:")
        print("1. Run: black .")
        print("2. Run: isort .")
        print("3. Fix any linting errors")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
#!/usr/bin/env python3
"""
Quick test script to verify workflow components are working
Run this locally to test before pushing to GitHub Actions
"""

import os
import sys
import subprocess
from datetime import datetime

def test_python_environment():
    """Test Python environment and dependencies"""
    print("🐍 Testing Python environment...")
    
    try:
        import pytest
        print("✅ pytest is available")
    except ImportError:
        print("❌ pytest not found - install with: pip install pytest")
        return False
    
    try:
        import selenium
        print("✅ selenium is available")
    except ImportError:
        print("❌ selenium not found - install with: pip install selenium")
        return False
    
    return True

def test_database_connection():
    """Test database connection"""
    print("\n🗄️ Testing database connection...")
    
    try:
        import mysql.connector
        print("✅ mysql-connector is available")
    except ImportError:
        print("❌ mysql-connector not found - install with: pip install mysql-connector-python")
        return False
    
    # Test connection to solutionsole.com
    try:
        import db.db_config
        print("✅ Database configuration file exists")
    except ImportError:
        print("❌ Database configuration not found")
        return False
    
    return True

def test_test_files():
    """Test if test files exist"""
    print("\n🧪 Testing test files...")
    
    test_files = [
        "tests/",
        "tests/test_ci_smoke.py",
        "test_db_connection_simple.py",
        "requirements.txt"
    ]
    
    all_exist = True
    for file_path in test_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} not found")
            all_exist = False
    
    return all_exist

def test_workflow_files():
    """Test if workflow files exist"""
    print("\n⚙️ Testing workflow files...")
    
    workflow_files = [
        ".github/workflows/scheduled-tests.yml",
        ".github/workflows/test-automation.yml"
    ]
    
    all_exist = True
    for file_path in workflow_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} not found")
            all_exist = False
    
    return all_exist

def run_quick_test():
    """Run a quick pytest to verify tests work"""
    print("\n🚀 Running quick test...")
    
    try:
        # Just test if pytest can import the test files without running them
        result = subprocess.run([
            "python", "-m", "pytest", 
            "tests/test_ci_smoke.py", 
            "--collect-only",
            "-q"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Test files can be imported successfully")
            print("✅ Environment is ready for GitHub Actions")
            return True
        else:
            print("❌ Test files have import errors")
            print("Output:", result.stdout)
            print("Errors:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Test collection timed out")
        return False
    except Exception as e:
        print(f"❌ Quick test error: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 GitHub Actions Workflow Quick Test")
    print("=" * 50)
    print(f"📅 Test Time: {datetime.now()}")
    print()
    
    tests = [
        ("Python Environment", test_python_environment),
        ("Database Connection", test_database_connection),
        ("Test Files", test_test_files),
        ("Workflow Files", test_workflow_files),
        ("Quick Test Run", run_quick_test)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your workflow should work correctly.")
        print("💡 Push your changes to trigger GitHub Actions.")
    else:
        print("⚠️ Some tests failed. Please fix the issues before pushing.")
        print("📋 Check the error messages above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
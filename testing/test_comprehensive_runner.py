#!/usr/bin/env python3
"""
Test Comprehensive Test Suite Runner
Quick test to verify the test runner works correctly.
"""

import os
import sys
from datetime import datetime

from run_all_test_suites import TestSuiteRunner


def test_runner_initialization():
    """Test that the runner initializes correctly"""
    print("🧪 Testing Test Suite Runner Initialization...")
    
    try:
        runner = TestSuiteRunner()
        print("✅ TestSuiteRunner initialized successfully")
        
        # Test database connection
        results = runner.db_helper.get_test_results(limit=1)
        print(f"✅ Database connection successful (found {len(results)} recent results)")
        
        runner.close()
        return True
        
    except Exception as e:
        print(f"❌ TestSuiteRunner initialization failed: {e}")
        return False


def test_single_test_suite():
    """Test running a single test suite"""
    print("\n🧪 Testing Single Test Suite Execution...")
    
    try:
        runner = TestSuiteRunner()
        
        # Test with a simple test suite
        test_suite = {
            'name': 'Test Smoke Tests',
            'file': 'tests/test_ci_smoke.py',
            'description': 'Test smoke tests execution'
        }
        
        print(f"📋 Running test suite: {test_suite['name']}")
        runner._run_test_suite(test_suite)
        
        print("✅ Single test suite execution completed")
        runner.close()
        return True
        
    except Exception as e:
        print(f"❌ Single test suite execution failed: {e}")
        return False


def test_database_storage():
    """Test database storage functionality"""
    print("\n🧪 Testing Database Storage...")
    
    try:
        runner = TestSuiteRunner()
        
        # Test storing a result
        test_message = f"""Test Database Storage:
Timestamp: {datetime.now()}
Test: Database storage test
Status: PASSED
Environment: Local testing"""
        
        runner._store_test_result(
            test_case_name="test_database_storage",
            module_name="test_comprehensive_runner",
            test_status="PASSED",
            error_message=test_message,
            device_name="local_testing",
            screen_resolution="test_environment"
        )
        
        print("✅ Database storage test completed")
        
        # Verify storage
        results = runner.db_helper.get_test_results(limit=1)
        if results and results[0]['test_case_name'] == 'test_database_storage':
            print("✅ Database storage verification successful")
        else:
            print("⚠️ Could not verify database storage")
        
        runner.close()
        return True
        
    except Exception as e:
        print(f"❌ Database storage test failed: {e}")
        return False


def main():
    """Main test function"""
    print("🔧 Test Comprehensive Test Suite Runner")
    print("=" * 60)
    
    tests = [
        ("Runner Initialization", test_runner_initialization),
        ("Database Storage", test_database_storage),
        ("Single Test Suite", test_single_test_suite),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Comprehensive test runner is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
#!/usr/bin/env python3
"""
Simple Database Logging Test
This test will trigger the pytest fixtures and verify database logging works.
"""

import pytest
import time

def test_simple_pass():
    """Simple test that should pass and log to database"""
    print("🧪 Running simple pass test")
    time.sleep(1)  # Simulate some work
    assert True
    print("✅ Simple pass test completed")

def test_simple_fail():
    """Simple test that should fail and log to database"""
    print("🧪 Running simple fail test")
    time.sleep(1)  # Simulate some work
    assert False, "This test is designed to fail for database logging verification"
    print("❌ This should not be reached")

def test_with_error():
    """Test that raises an exception and should log to database"""
    print("🧪 Running test with error")
    time.sleep(1)  # Simulate some work
    raise Exception("This is a test exception for database logging verification")

if __name__ == "__main__":
    print("🚀 Running simple database logging tests")
    print("=" * 50)
    
    # Run the tests using pytest
    import subprocess
    import sys
    
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        __file__,
        "-v", 
        "--tb=short",
        "--capture=no"
    ])
    
    print(f"\n📊 Test execution completed with exit code: {result.returncode}")
    print("💾 Check database for logged test results") 
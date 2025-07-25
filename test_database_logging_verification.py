#!/usr/bin/env python3
"""
Database Logging Verification Test
This script verifies that test results are being stored in the database during test execution.
"""

import pytest
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.db_helper import MySQLHelper


def test_database_logging_verification():
    """Test that verifies database logging is working"""
    print("🧪 Testing Database Logging Verification")
    print("=" * 50)
    
    try:
        # Initialize database helper
        db_helper = MySQLHelper()
        
        # Get current test count
        initial_results = db_helper.get_test_results(limit=100)
        initial_count = len(initial_results)
        print(f"📊 Initial test count in database: {initial_count}")
        
        # Store a test verification entry
        test_message = f"""
Database Logging Verification Test
Timestamp: {datetime.now()}
Purpose: Verify that test results are being stored in database
Status: PASSED
Environment: Local verification
        """
        
        db_helper.store_test_result_in_tables(
            test_case_name="database_logging_verification",
            module_name="test_database_logging_verification",
            test_status="PASSED",
            error_message=test_message,
            device_name="local_verification",
            screen_resolution="test_environment"
        )
        
        # Get updated test count
        updated_results = db_helper.get_test_results(limit=100)
        updated_count = len(updated_results)
        print(f"📊 Updated test count in database: {updated_count}")
        
        # Verify the entry was added
        if updated_count > initial_count:
            print("✅ Database logging verification PASSED!")
            print(f"   - Added {updated_count - initial_count} new test result(s)")
            
            # Show the latest entry
            latest_result = updated_results[0] if updated_results else None
            if latest_result:
                print(f"   - Latest test: {latest_result['test_case_name']} ({latest_result['test_status']})")
            
            db_helper.close()
            return True
        else:
            print("❌ Database logging verification FAILED!")
            print("   - No new test results were added to database")
            db_helper.close()
            return False
            
    except Exception as e:
        print(f"❌ Database logging verification ERROR: {e}")
        return False


def test_pytest_integration():
    """Test that pytest fixtures are working with database"""
    print("\n🧪 Testing Pytest Database Integration")
    print("=" * 50)
    
    try:
        # This test should trigger the conftest.py fixtures
        # and automatically log to database
        db_helper = MySQLHelper()
        
        # Get current count
        initial_results = db_helper.get_test_results(limit=100)
        initial_count = len(initial_results)
        
        print(f"📊 Tests in database before pytest integration test: {initial_count}")
        
        # Run a simple pytest test that should trigger database logging
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "test_database_logging_verification.py::test_database_logging_verification",
            "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print(f"📋 Pytest exit code: {result.returncode}")
        print(f"📋 Pytest output: {result.stdout[:500]}...")
        
        # Check if new results were added
        updated_results = db_helper.get_test_results(limit=100)
        updated_count = len(updated_results)
        
        print(f"📊 Tests in database after pytest integration test: {updated_count}")
        
        if updated_count > initial_count:
            print("✅ Pytest database integration working!")
            db_helper.close()
            return True
        else:
            print("❌ Pytest database integration not working!")
            print("   - No new test results from pytest execution")
            db_helper.close()
            return False
            
    except Exception as e:
        print(f"❌ Pytest integration test ERROR: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Database Logging Verification Suite")
    print("=" * 60)
    
    # Test 1: Direct database logging
    test1_passed = test_database_logging_verification()
    
    # Test 2: Pytest integration
    test2_passed = test_pytest_integration()
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION RESULTS:")
    print(f"   Direct Database Logging: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"   Pytest Integration: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All database logging verification tests PASSED!")
        print("   Your database integration is working correctly.")
    else:
        print("\n⚠️ Some database logging verification tests FAILED!")
        print("   Please check your database configuration and pytest setup.")
    
    sys.exit(0 if (test1_passed and test2_passed) else 1) 
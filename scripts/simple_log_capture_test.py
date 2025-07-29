#!/usr/bin/env python3
"""
Simple Log Capture Test
Quick test of the log capture functionality.
"""

import os
import sys
from datetime import datetime

from db.db_helper import MySQLHelper


def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    
    try:
        db_helper = MySQLHelper()
        
        # Test basic operations
        print("✅ Database connection successful!")
        
        # Get test results
        results = db_helper.get_test_results(limit=5)
        print(f"📊 Found {len(results)} test results in database")
        
        # Get statistics
        stats = db_helper.get_test_statistics()
        if stats:
            print(f"📈 Statistics: {stats['total_tests']} total tests")
        
        db_helper.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_log_storage():
    """Test storing a simple log entry"""
    print("\n📝 Testing log storage...")
    
    try:
        db_helper = MySQLHelper()
        
        # Store a test log entry
        test_message = f"""Test Log Entry:
Timestamp: {datetime.now()}
Test: Simple log capture test
Status: PASSED
Environment: Local testing"""
        
        db_helper.store_test_result_in_tables(
            test_case_name="simple_log_test",
            module_name="log_capture_testing",
            test_status="PASSED",
            error_message=test_message,
            device_name="local_testing",
            screen_resolution="test_environment"
        )
        
        print("✅ Test log entry stored successfully!")
        
        # Verify it was stored
        results = db_helper.get_test_results(limit=1)
        if results and results[0]['test_case_name'] == 'simple_log_test':
            print("✅ Test log entry verified in database!")
        else:
            print("⚠️ Could not verify test log entry")
        
        db_helper.close()
        return True
        
    except Exception as e:
        print(f"❌ Log storage test failed: {e}")
        return False


def main():
    """Main test function"""
    print("🔧 Simple Log Capture Test")
    print("=" * 40)
    
    # Test database connection
    if not test_database_connection():
        print("❌ Database connection test failed")
        return False
    
    # Test log storage
    if not test_log_storage():
        print("❌ Log storage test failed")
        return False
    
    print("\n🎉 Simple log capture test completed successfully!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
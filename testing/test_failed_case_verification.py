#!/usr/bin/env python3
"""
Test to verify that failed test cases are stored in database
This test will intentionally fail to demonstrate the storage functionality
"""

import os
import sys
from datetime import datetime

def test_failed_case_storage():
    """Test function that will fail to verify failed test storage"""
    print(f"🔧 Failed Test Case Storage Verification")
    print(f"📅 Test Time: {datetime.now()}")
    print(f"❌ This test will intentionally fail to verify storage")
    
    # Add the current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from db.db_helper import MySQLHelper
        
        # Test database connection
        helper = MySQLHelper()
        print("✅ Database connection successful")
        
        # Test inserting a FAILED record
        test_name = "failed_test_case_verification"
        module_name = "test_failed_case_verification"
        test_status = "FAILED"
        error_message = "Intentional test failure to verify database storage functionality"
        
        helper.insert_test_result(
            test_case_name=test_name,
            module_name=module_name,
            test_status=test_status,
            error_message=error_message,
            total_time_duration=2.1,
            device_name="desktop",
            screen_resolution="1920x1080",
            error_link="file:///test/path/failed_test_screenshot.png"
        )
        
        print("✅ Failed test result successfully stored in database")
        print("✅ Failed test storage verification completed")
        
        helper.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed test storage verification failed: {e}")
        return False

if __name__ == "__main__":
    success = test_failed_case_storage()
    sys.exit(0 if success else 1) 
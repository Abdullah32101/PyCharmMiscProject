#!/usr/bin/env python3
"""
Test trigger file to verify database storage functionality
This file will be used to trigger CI/CD pipeline and verify test results storage
"""

import os
import sys
from datetime import datetime

def test_database_storage_verification():
    """Test function to verify database storage is working"""
    print(f"🔧 Database Storage Verification Test")
    print(f"📅 Test Time: {datetime.now()}")
    print(f"✅ This test will verify that results are stored in database")
    
    # Add the current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from db.db_helper import MySQLHelper
        
        # Test database connection
        helper = MySQLHelper()
        print("✅ Database connection successful")
        
        # Test inserting a verification record
        test_name = "database_storage_verification_test"
        module_name = "trigger_test_verification"
        test_status = "PASSED"
        
        helper.insert_test_result(
            test_case_name=test_name,
            module_name=module_name,
            test_status=test_status,
            error_message=None,
            total_time_duration=1.5,
            device_name="desktop",
            screen_resolution="1920x1080",
            error_link=None
        )
        
        print("✅ Test result successfully stored in database")
        print("✅ Database storage verification completed")
        
        helper.close()
        return True
        
    except Exception as e:
        print(f"❌ Database storage verification failed: {e}")
        return False

if __name__ == "__main__":
    success = test_database_storage_verification()
    sys.exit(0 if success else 1) 
#!/usr/bin/env python3
"""
Trigger file to execute full test suite in GitHub Actions
This file will trigger the complete test automation workflow
"""

import os
import sys
from datetime import datetime

def trigger_full_test_suite():
    """Function to trigger full test suite execution"""
    print(f"🚀 Triggering Full Test Suite Execution")
    print(f"📅 Trigger Time: {datetime.now()}")
    print(f"✅ This will execute all test cases in GitHub Actions")
    print(f"📊 Tests will be stored in database for verification")
    
    # Add the current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from db.db_helper import MySQLHelper
        
        # Test database connection
        helper = MySQLHelper()
        print("✅ Database connection verified")
        
        # Insert a trigger record
        test_name = "full_test_suite_trigger"
        module_name = "trigger_full_test_suite"
        test_status = "PASSED"
        
        helper.insert_test_result(
            test_case_name=test_name,
            module_name=module_name,
            test_status=test_status,
            error_message=None,
            total_time_duration=0.5,
            device_name="desktop",
            screen_resolution="1920x1080",
            error_link=None
        )
        
        print("✅ Trigger record stored in database")
        print("✅ Full test suite execution triggered")
        print("🔍 Check GitHub Actions tab for execution status")
        
        helper.close()
        return True
        
    except Exception as e:
        print(f"❌ Trigger failed: {e}")
        return False

if __name__ == "__main__":
    success = trigger_full_test_suite()
    sys.exit(0 if success else 1) 
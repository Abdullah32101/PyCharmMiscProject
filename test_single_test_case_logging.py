#!/usr/bin/env python3
"""
Single Test Case Logging Verification
This script runs a single test case and verifies that logs are generated in the database.
"""

import sys
import os
import subprocess
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_database_before():
    """Check database state before running test"""
    print("🔍 Checking Database Before Test")
    print("=" * 40)
    
    try:
        from db.db_helper import MySQLHelper
        
        db_helper = MySQLHelper()
        db_helper.create_test_results_table()
        
        # Get current test count
        initial_results = db_helper.get_test_results(limit=10)
        initial_count = len(initial_results)
        print(f"📊 Test results in database: {initial_count}")
        
        db_helper.close()
        return initial_count
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return 0

def run_single_test():
    """Run a single test case"""
    print("\n🧪 Running Single Test Case")
    print("=" * 40)
    
    # Try to run a simple test first
    test_options = [
        "tests/test_ci_smoke.py::test_page_loads",
        "tests/test_ci_smoke.py",
        "test_db_connection_simple.py",
        "test_simple_database_logging.py::test_simple_pass"
    ]
    
    for test_option in test_options:
        if os.path.exists(test_option.split("::")[0]):
            print(f"📋 Running: {test_option}")
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pytest", 
                    test_option,
                    "-v", 
                    "--tb=short",
                    "--capture=no"
                ], capture_output=True, text=True, timeout=300)
                
                print(f"   Exit code: {result.returncode}")
                print(f"   Output: {result.stdout[:300]}...")
                
                if result.stderr:
                    print(f"   Errors: {result.stderr[:200]}...")
                
                return True
                
            except subprocess.TimeoutExpired:
                print(f"   ⏰ Timeout running {test_option}")
                continue
            except Exception as e:
                print(f"   ❌ Error running {test_option}: {e}")
                continue
    
    print("❌ No test cases could be run")
    return False

def check_database_after():
    """Check database state after running test"""
    print("\n💾 Checking Database After Test")
    print("=" * 40)
    
    try:
        from db.db_helper import MySQLHelper
        
        db_helper = MySQLHelper()
        
        # Get updated test count
        updated_results = db_helper.get_test_results(limit=20)
        updated_count = len(updated_results)
        print(f"📊 Test results in database: {updated_count}")
        
        # Show recent test results
        if updated_results:
            print("\n📋 Recent test results:")
            for i, result in enumerate(updated_results[:5]):
                print(f"   {i+1}. {result['test_case_name']} - {result['test_status']} - {result['test_datetime']}")
        
        db_helper.close()
        return updated_count
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return 0

def main():
    """Main function"""
    print("🚀 Single Test Case Logging Verification")
    print("=" * 50)
    print(f"📅 Time: {datetime.now()}")
    print("=" * 50)
    
    # Check database before
    before_count = check_database_before()
    
    # Run single test
    test_run = run_single_test()
    
    # Check database after
    after_count = check_database_after()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"   Before: {before_count} test results")
    print(f"   After: {after_count} test results")
    print(f"   Added: {after_count - before_count} new results")
    print(f"   Test Run: {'✅ YES' if test_run else '❌ NO'}")
    
    # Result
    logs_generated = after_count > before_count
    
    if logs_generated:
        print("\n🎉 SUCCESS! Test case generated logs in database!")
        print(f"   Added {after_count - before_count} new test result(s)")
    else:
        print("\n❌ FAILED! No logs generated in database!")
        print("   Database logging is not working")
    
    return logs_generated

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
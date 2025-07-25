#!/usr/bin/env python3
"""
Database Logging Verification Script
This script verifies that database logging is working correctly.
"""

import sys
import os
import subprocess
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_database_connection():
    """Check if database connection is working"""
    print("🔧 Step 1: Checking Database Connection")
    print("=" * 50)
    
    try:
        from db.db_helper import MySQLHelper
        
        # Test connection
        db_helper = MySQLHelper()
        db_helper.create_test_results_table()
        
        # Get current test count
        initial_results = db_helper.get_test_results(limit=10)
        initial_count = len(initial_results)
        print(f"📊 Current test results in database: {initial_count}")
        
        db_helper.close()
        return True, initial_count
        
    except Exception as e:
        print(f"❌ Database connection failed: {type(e).__name__} - {e}")
        return False, 0

def run_simple_tests():
    """Run simple tests to trigger database logging"""
    print("\n🧪 Step 2: Running Simple Tests")
    print("=" * 50)
    
    try:
        # Run the simple database logging test
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "test_simple_database_logging.py",
            "-v", 
            "--tb=short",
            "--capture=no"
        ], capture_output=True, text=True)
        
        print(f"📋 Test execution exit code: {result.returncode}")
        print(f"📋 Test output: {result.stdout[:500]}...")
        
        if result.stderr:
            print(f"📋 Test errors: {result.stderr[:300]}...")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def verify_database_logging():
    """Verify that test results were logged to database"""
    print("\n💾 Step 3: Verifying Database Logging")
    print("=" * 50)
    
    try:
        from db.db_helper import MySQLHelper
        
        db_helper = MySQLHelper()
        
        # Get updated test count
        updated_results = db_helper.get_test_results(limit=20)
        updated_count = len(updated_results)
        print(f"📊 Updated test results in database: {updated_count}")
        
        # Show recent test results
        if updated_results:
            print("\n📋 Recent test results:")
            for i, result in enumerate(updated_results[:5]):
                print(f"   {i+1}. {result['test_case_name']} - {result['test_status']} - {result['test_datetime']}")
        
        db_helper.close()
        return updated_count
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return 0

def run_database_connection_test():
    """Run the database connection test"""
    print("\n🔗 Step 4: Running Database Connection Test")
    print("=" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, 
            "test_db_connection_simple.py"
        ], capture_output=True, text=True)
        
        print(f"📋 Connection test exit code: {result.returncode}")
        print(f"📋 Connection test output: {result.stdout}")
        
        if result.stderr:
            print(f"📋 Connection test errors: {result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🚀 Database Logging Verification Suite")
    print("=" * 60)
    print(f"📅 Verification Time: {datetime.now()}")
    print(f"🖥️ Environment: {'GitHub Actions' if os.getenv('GITHUB_ACTIONS') else 'Local'}")
    print("=" * 60)
    
    # Step 1: Check database connection
    connection_ok, initial_count = check_database_connection()
    
    if not connection_ok:
        print("\n❌ Database connection failed. Cannot proceed with verification.")
        return False
    
    # Step 2: Run simple tests
    tests_ok = run_simple_tests()
    
    # Step 3: Verify database logging
    final_count = verify_database_logging()
    
    # Step 4: Run database connection test
    connection_test_ok = run_database_connection_test()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY:")
    print(f"   Database Connection: {'✅ WORKING' if connection_ok else '❌ FAILED'}")
    print(f"   Test Execution: {'✅ WORKING' if tests_ok else '❌ FAILED'}")
    print(f"   Database Logging: {'✅ WORKING' if final_count > initial_count else '❌ FAILED'}")
    print(f"   Connection Test: {'✅ WORKING' if connection_test_ok else '❌ FAILED'}")
    print(f"   Test Results Added: {final_count - initial_count}")
    
    # Overall result
    all_working = connection_ok and tests_ok and (final_count > initial_count) and connection_test_ok
    
    if all_working:
        print("\n🎉 ALL VERIFICATIONS PASSED!")
        print("   Your database logging system is working correctly.")
        print("   Test results are being stored in the database.")
    else:
        print("\n⚠️ SOME VERIFICATIONS FAILED!")
        print("   Please check the database configuration and pytest setup.")
    
    return all_working

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
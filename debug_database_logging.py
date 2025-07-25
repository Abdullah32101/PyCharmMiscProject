#!/usr/bin/env python3
"""
Database Logging Debug Script
This script helps debug why test results are not being stored in the database.
"""

import os
import sys
import traceback
from datetime import datetime

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.db_helper import MySQLHelper


def check_database_connection():
    """Check if database connection is working"""
    print("🔍 Checking database connection...")
    
    try:
        db_helper = MySQLHelper()
        print("✅ Database connection successful!")
        
        # Test basic operations
        results = db_helper.get_test_results(limit=1)
        print(f"✅ Database query successful - Found {len(results)} results")
        
        db_helper.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        traceback.print_exc()
        return False


def check_environment_variables():
    """Check if required environment variables are set"""
    print("\n🔍 Checking environment variables...")
    
    env_vars = [
        'GITHUB_ACTIONS',
        'GITHUB_WORKFLOW',
        'GITHUB_RUN_ID',
        'PYTHONPATH'
    ]
    
    for var in env_vars:
        value = os.getenv(var, 'NOT_SET')
        print(f"   {var}: {value}")
    
    # Check database config
    print("\n🔍 Checking database configuration...")
    try:
        from db.db_config import DB_CONFIG
        print(f"   Host: {DB_CONFIG.get('host', 'NOT_SET')}")
        print(f"   Database: {DB_CONFIG.get('database', 'NOT_SET')}")
        print(f"   User: {DB_CONFIG.get('user', 'NOT_SET')}")
        print(f"   Password: {'SET' if DB_CONFIG.get('password') else 'NOT_SET'}")
    except Exception as e:
        print(f"   ❌ Could not load database config: {e}")


def test_database_logging():
    """Test if database logging is working"""
    print("\n🔍 Testing database logging...")
    
    try:
        db_helper = MySQLHelper()
        
        # Get initial count
        initial_results = db_helper.get_test_results(limit=100)
        initial_count = len(initial_results)
        print(f"📊 Initial test count: {initial_count}")
        
        # Try to insert a test result
        test_message = f"""
Database Logging Debug Test
Timestamp: {datetime.now()}
Purpose: Debug database logging issues
Environment: {'GitHub Actions' if os.getenv('GITHUB_ACTIONS') else 'Local'}
Status: PASSED
        """
        
        db_helper.store_test_result_in_tables(
            test_case_name="debug_database_logging_test",
            module_name="debug_database_logging",
            test_status="PASSED",
            error_message=test_message,
            device_name="debug_environment",
            screen_resolution="debug_system"
        )
        
        # Check if it was inserted
        updated_results = db_helper.get_test_results(limit=100)
        updated_count = len(updated_results)
        
        print(f"📊 Updated test count: {updated_count}")
        
        if updated_count > initial_count:
            print("✅ Database logging test PASSED!")
            print(f"   - Added {updated_count - initial_count} new test result(s)")
            
            # Show the latest entry
            latest_result = updated_results[0] if updated_results else None
            if latest_result:
                print(f"   - Latest test: {latest_result['test_case_name']} ({latest_result['test_status']})")
            
            db_helper.close()
            return True
        else:
            print("❌ Database logging test FAILED!")
            print("   - No new test results were added")
            db_helper.close()
            return False
            
    except Exception as e:
        print(f"❌ Database logging test ERROR: {e}")
        traceback.print_exc()
        return False


def check_pytest_fixtures():
    """Check if pytest fixtures are available"""
    print("\n🔍 Checking pytest fixtures...")
    
    try:
        import pytest
        print("✅ Pytest is available")
        
        # Check if conftest.py exists
        if os.path.exists("conftest.py"):
            print("✅ conftest.py exists")
            
            # Try to import conftest
            import conftest
            print("✅ conftest.py can be imported")
            
            # Check for specific fixtures
            if hasattr(conftest, 'capture_test_results'):
                print("✅ capture_test_results fixture exists")
            else:
                print("❌ capture_test_results fixture not found")
                
            if hasattr(conftest, 'get_db_helper'):
                print("✅ get_db_helper function exists")
            else:
                print("❌ get_db_helper function not found")
                
        else:
            print("❌ conftest.py not found")
            
    except Exception as e:
        print(f"❌ Error checking pytest fixtures: {e}")
        traceback.print_exc()


def run_pytest_test():
    """Run a simple pytest test to see if fixtures are triggered"""
    print("\n🔍 Running pytest test to check fixtures...")
    
    try:
        import subprocess
        import pytest
        
        # Create a simple test file
        test_content = '''
def test_debug_fixture():
    """Test that should trigger database logging fixtures"""
    print("🧪 Running debug fixture test...")
    assert True
'''
        
        with open("test_debug_fixture.py", "w") as f:
            f.write(test_content)
        
        # Run the test
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "test_debug_fixture.py::test_debug_fixture",
            "-v", "--tb=short", "-s"
        ], capture_output=True, text=True)
        
        print(f"📋 Pytest exit code: {result.returncode}")
        print(f"📋 Pytest stdout: {result.stdout}")
        print(f"📋 Pytest stderr: {result.stderr}")
        
        # Clean up
        if os.path.exists("test_debug_fixture.py"):
            os.remove("test_debug_fixture.py")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running pytest test: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all debug checks"""
    print("🚀 Database Logging Debug Suite")
    print("=" * 60)
    
    checks = [
        ("Database Connection", check_database_connection),
        ("Environment Variables", check_environment_variables),
        ("Database Logging", test_database_logging),
        ("Pytest Fixtures", check_pytest_fixtures),
        ("Pytest Test Execution", run_pytest_test),
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        print(f"\n{'='*20} {check_name} {'='*20}")
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ {check_name} failed with exception: {e}")
            results[check_name] = False
    
    print("\n" + "=" * 60)
    print("📊 DEBUG RESULTS:")
    
    passed = 0
    total = len(results)
    
    for check_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {check_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Summary: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All debug checks passed!")
        print("   Database logging should be working correctly.")
    else:
        print("\n⚠️ Some debug checks failed!")
        print("   Please review the issues above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
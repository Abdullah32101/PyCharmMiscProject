#!/usr/bin/env python3
"""
Real Test Cases Logging Verification
This script runs actual test cases and verifies that logs are generated in the database.
"""

import sys
import os
import subprocess
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_initial_database_state():
    """Check initial state of database before running tests"""
    print("🔍 Step 1: Checking Initial Database State")
    print("=" * 50)
    
    try:
        from db.db_helper import MySQLHelper
        
        db_helper = MySQLHelper()
        db_helper.create_test_results_table()
        
        # Get current test count
        initial_results = db_helper.get_test_results(limit=50)
        initial_count = len(initial_results)
        print(f"📊 Current test results in database: {initial_count}")
        
        # Show recent test results
        if initial_results:
            print("\n📋 Recent test results:")
            for i, result in enumerate(initial_results[:5]):
                print(f"   {i+1}. {result['test_case_name']} - {result['test_status']} - {result['test_datetime']}")
        
        db_helper.close()
        return initial_count
        
    except Exception as e:
        print(f"❌ Database check failed: {type(e).__name__} - {e}")
        return 0

def run_real_test_cases():
    """Run actual test cases from the project"""
    print("\n🧪 Step 2: Running Real Test Cases")
    print("=" * 50)
    
    # List of real test files to run
    test_files = [
        "tests/test_ci_smoke.py",
        "tests/test_one_time_book_purchase.py", 
        "tests/test_purchase_membership_question_by_monthly_plan.py",
        "tests/test_purchase_membership_question_by_one_time_plan.py",
        "tests/test_purchase_membership_question_by_three_month_popular_plan.py",
        "tests/test_purchase_membership_questions_by_six_month_plan.py"
    ]
    
    # Check which test files exist
    existing_tests = []
    for test_file in test_files:
        if os.path.exists(test_file):
            existing_tests.append(test_file)
            print(f"✅ Found test file: {test_file}")
        else:
            print(f"⚠️ Test file not found: {test_file}")
    
    if not existing_tests:
        print("❌ No test files found!")
        return False
    
    print(f"\n🚀 Running {len(existing_tests)} test files...")
    
    # Run each test file
    for test_file in existing_tests:
        print(f"\n📋 Running: {test_file}")
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_file,
                "-v", 
                "--tb=short",
                "--capture=no",
                "--timeout=300"  # 5 minute timeout per test file
            ], capture_output=True, text=True, timeout=600)  # 10 minute total timeout
            
            print(f"   Exit code: {result.returncode}")
            print(f"   Output: {result.stdout[:200]}...")
            
            if result.stderr:
                print(f"   Errors: {result.stderr[:200]}...")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timeout running {test_file}")
        except Exception as e:
            print(f"   ❌ Error running {test_file}: {e}")
    
    return True

def verify_database_logging():
    """Verify that test results were logged to database"""
    print("\n💾 Step 3: Verifying Database Logging")
    print("=" * 50)
    
    try:
        from db.db_helper import MySQLHelper
        
        db_helper = MySQLHelper()
        
        # Get updated test count
        updated_results = db_helper.get_test_results(limit=100)
        updated_count = len(updated_results)
        print(f"📊 Updated test results in database: {updated_count}")
        
        # Show recent test results
        if updated_results:
            print("\n📋 Recent test results:")
            for i, result in enumerate(updated_results[:10]):
                print(f"   {i+1}. {result['test_case_name']} - {result['test_status']} - {result['test_datetime']}")
                if result['error_message']:
                    print(f"      Error: {result['error_message'][:100]}...")
        
        db_helper.close()
        return updated_count
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return 0

def run_comprehensive_test_suite():
    """Run the comprehensive test suite runner"""
    print("\n🚀 Step 4: Running Comprehensive Test Suite")
    print("=" * 50)
    
    try:
        # Check if the comprehensive test suite runner exists
        if os.path.exists("run_all_test_suites.py"):
            print("📋 Running comprehensive test suite...")
            result = subprocess.run([
                sys.executable, 
                "run_all_test_suites.py"
            ], capture_output=True, text=True, timeout=900)  # 15 minute timeout
            
            print(f"📋 Comprehensive test exit code: {result.returncode}")
            print(f"📋 Output: {result.stdout[:500]}...")
            
            if result.stderr:
                print(f"📋 Errors: {result.stderr[:300]}...")
            
            return result.returncode == 0
        else:
            print("⚠️ Comprehensive test suite runner not found")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Comprehensive test suite timed out")
        return False
    except Exception as e:
        print(f"❌ Comprehensive test suite failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🚀 Real Test Cases Logging Verification")
    print("=" * 60)
    print(f"📅 Verification Time: {datetime.now()}")
    print(f"🖥️ Environment: {'GitHub Actions' if os.getenv('GITHUB_ACTIONS') else 'Local'}")
    print("=" * 60)
    
    # Step 1: Check initial database state
    initial_count = check_initial_database_state()
    
    # Step 2: Run real test cases
    tests_run = run_real_test_cases()
    
    # Step 3: Verify database logging
    final_count = verify_database_logging()
    
    # Step 4: Run comprehensive test suite
    comprehensive_ok = run_comprehensive_test_suite()
    
    # Final verification
    final_final_count = verify_database_logging()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY:")
    print(f"   Initial Test Count: {initial_count}")
    print(f"   Final Test Count: {final_final_count}")
    print(f"   Test Results Added: {final_final_count - initial_count}")
    print(f"   Real Tests Run: {'✅ YES' if tests_run else '❌ NO'}")
    print(f"   Comprehensive Suite: {'✅ RUN' if comprehensive_ok else '❌ FAILED'}")
    
    # Overall result
    logs_generated = final_final_count > initial_count
    
    if logs_generated:
        print("\n🎉 SUCCESS! Test case logs are being generated in database!")
        print(f"   Added {final_final_count - initial_count} new test results")
        print("   Your database logging system is working correctly.")
    else:
        print("\n❌ FAILED! No test case logs were generated in database!")
        print("   Please check:")
        print("   - Database connection configuration")
        print("   - Pytest fixtures in conftest.py")
        print("   - Test case execution")
    
    return logs_generated

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
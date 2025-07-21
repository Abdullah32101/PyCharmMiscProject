#!/usr/bin/env python3
"""
Comprehensive Membership Plan Test Runner with Mobile Support
This script runs all membership plan tests on multiple devices with database integration.
"""

import pytest
import sys
import os
import time
from datetime import datetime

def run_all_membership_plan_tests():
    """Run all membership plan tests on multiple devices using pytest for database integration"""
    
    print("[📱] Starting comprehensive membership plan tests with mobile support and database integration...")
    
    # Set environment variable to indicate mobile testing
    os.environ["MOBILE_TEST"] = "true"
    
    # List of all membership plan test files
    test_files = [
        "tests/test_purchase_membership_question_by_monthly_plan.py",
        "tests/test_purchase_membership_question_by_one_time_plan.py", 
        "tests/test_purchase_membership_questions_by_six_month_plan.py",
        "tests/test_purchase_membership_question_by_three_month_popular_plan.py"
    ]
    
    total_passed = 0
    total_failed = 0
    
    for test_file in test_files:
        print(f"\n{'='*60}")
        print(f"Running tests from: {test_file}")
        print(f"{'='*60}")
        
        # Run pytest for each test file
        pytest_args = [
            test_file,
            "-v",  # Verbose output
            "--tb=short",  # Short traceback format
            "--capture=no",  # Show print statements
            "-s",  # Don't capture stdout/stderr
            f"--html={os.path.basename(test_file).replace('.py', '')}_report.html",
            "--self-contained-html"
        ]
        
        # Run pytest and capture the exit code
        exit_code = pytest.main(pytest_args)
        
        if exit_code == 0:
            print(f"[✅] {test_file} completed successfully!")
            total_passed += 1
        else:
            print(f"[❌] {test_file} failed with exit code: {exit_code}")
            total_failed += 1
    
    return total_passed, total_failed

def run_mobile_membership_plan_tests():
    """Run all membership plan tests specifically on mobile devices"""
    
    print("[📱] Starting mobile-specific membership plan tests...")
    
    # Set environment variable to force mobile testing
    os.environ["MOBILE_TEST"] = "true"
    os.environ["TEST_DEVICES"] = "iPhone X,iPad Pro"
    
    # List of all membership plan test files
    test_files = [
        "tests/test_purchase_membership_question_by_monthly_plan.py",
        "tests/test_purchase_membership_question_by_one_time_plan.py", 
        "tests/test_purchase_membership_questions_by_six_month_plan.py",
        "tests/test_purchase_membership_question_by_three_month_popular_plan.py"
    ]
    
    total_passed = 0
    total_failed = 0
    
    for test_file in test_files:
        print(f"\n{'='*60}")
        print(f"Running mobile tests from: {test_file}")
        print(f"{'='*60}")
        
        # Run pytest for each test file
        pytest_args = [
            test_file,
            "-v",
            "--tb=short",
            "--capture=no",
            "-s",
            f"--html=mobile_{os.path.basename(test_file).replace('.py', '')}_report.html",
            "--self-contained-html"
        ]
        
        # Run pytest and capture the exit code
        exit_code = pytest.main(pytest_args)
        
        if exit_code == 0:
            print(f"[✅] Mobile {test_file} completed successfully!")
            total_passed += 1
        else:
            print(f"[❌] Mobile {test_file} failed with exit code: {exit_code}")
            total_failed += 1
    
    return total_passed, total_failed

def run_specific_membership_plan_test(test_type):
    """Run a specific membership plan test type"""
    
    test_mapping = {
        "monthly": "tests/test_purchase_membership_question_by_monthly_plan.py",
        "onetime": "tests/test_purchase_membership_question_by_one_time_plan.py",
        "one-time": "tests/test_purchase_membership_question_by_one_time_plan.py",
        "sixmonth": "tests/test_purchase_membership_questions_by_six_month_plan.py",
        "six-month": "tests/test_purchase_membership_questions_by_six_month_plan.py",
        "popular": "tests/test_purchase_membership_question_by_three_month_popular_plan.py",
        "three-month": "tests/test_purchase_membership_question_by_three_month_popular_plan.py"
    }
    
    if test_type not in test_mapping:
        print(f"[❌] Unknown test type: {test_type}")
        print(f"Available types: {', '.join(test_mapping.keys())}")
        return False
    
    test_file = test_mapping[test_type]
    print(f"[📱] Running {test_type} membership plan test...")
    
    # Set environment variable to indicate mobile testing
    os.environ["MOBILE_TEST"] = "true"
    
    # Run pytest for the specific test file
    pytest_args = [
        test_file,
        "-v",
        "--tb=short",
        "--capture=no",
        "-s",
        f"--html={test_type}_membership_plan_report.html",
        "--self-contained-html"
    ]
    
    # Run pytest and capture the exit code
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print(f"[✅] {test_type} membership plan test completed successfully!")
        return True
    else:
        print(f"[❌] {test_type} membership plan test failed with exit code: {exit_code}")
        return False

def print_summary(total_passed, total_failed, test_type="all"):
    """Print test summary"""
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY - {test_type.upper()} MEMBERSHIP PLANS")
    print(f"{'='*60}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"📊 Total: {total_passed + total_failed}")
    
    if total_failed == 0:
        print(f"\n[🎉] All {test_type} membership plan tests passed!")
        print("[💾] Test results have been logged to the database.")
    else:
        print(f"\n[⚠️] {total_failed} {test_type} membership plan test(s) failed!")
        print("[📸] Check for screenshot files in the current directory")

if __name__ == "__main__":
    print("=" * 60)
    print("COMPREHENSIVE MEMBERSHIP PLAN TEST RUNNER")
    print("=" * 60)
    print("Available options:")
    print("  - No arguments: Run all membership plan tests")
    print("  - mobile: Run all membership plan tests on mobile devices only")
    print("  - monthly: Run monthly membership plan tests only")
    print("  - onetime/one-time: Run one-time membership plan tests only")
    print("  - sixmonth/six-month: Run six-month membership plan tests only")
    print("  - popular/three-month: Run three-month popular membership plan tests only")
    print("=" * 60)
    
    start_time = time.time()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == "mobile":
            total_passed, total_failed = run_mobile_membership_plan_tests()
            print_summary(total_passed, total_failed, "mobile")
        elif arg in ["monthly", "onetime", "one-time", "sixmonth", "six-month", "popular", "three-month"]:
            success = run_specific_membership_plan_test(arg)
            if success:
                print_summary(1, 0, arg)
            else:
                print_summary(0, 1, arg)
        else:
            print(f"[❌] Unknown argument: {arg}")
            print("Available arguments: mobile, monthly, onetime, one-time, sixmonth, six-month, popular, three-month")
            sys.exit(1)
    else:
        # Run all tests
        total_passed, total_failed = run_all_membership_plan_tests()
        print_summary(total_passed, total_failed, "all")
    
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    print(f"\n⏱️ Total execution time: {duration} seconds")
    
    # Exit with appropriate code
    if len(sys.argv) > 1 and sys.argv[1].lower() in ["monthly", "onetime", "one-time", "sixmonth", "six-month", "popular", "three-month"]:
        # For specific tests, check if it was successful
        if "success" in locals() and success:
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        # For all tests, check if any failed
        if total_failed == 0:
            sys.exit(0)
        else:
            sys.exit(1) 
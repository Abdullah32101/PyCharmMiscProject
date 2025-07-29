#!/usr/bin/env python3
"""
Three Month Popular Plan Test Runner
This script runs the three-month popular plan test on all devices with proper configuration.
"""

import os
import sys
import time

import pytest


def run_three_month_popular_test():
    """Run the three-month popular plan test on all devices"""
    
    print("=" * 80)
    print("🚀 THREE MONTH POPULAR PLAN TEST - ALL DEVICES")
    print("=" * 80)
    print("📱 Devices: Desktop → iPhone X → iPad Pro → Samsung Galaxy S21")
    print("⏱️  Browser will stay open for 10 seconds after each test")
    print("=" * 80)
    
    # Clear any existing environment variables that might interfere
    if "MOBILE_TEST" in os.environ:
        del os.environ["MOBILE_TEST"]
    if "TEST_DEVICES" in os.environ:
        del os.environ["TEST_DEVICES"]
    
    # Set environment to ensure all devices are tested
    os.environ["TEST_DEVICES"] = "desktop,iPhone X,iPad Pro,Samsung Galaxy S21"
    
    # Run pytest with proper configuration
    pytest_args = [
        "tests/test_purchase_membership_question_by_three_month_popular_plan.py",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--capture=no",  # Show print statements
        "-s",  # Don't capture stdout/stderr
        "--html=three_month_popular_test_report.html",
        "--self-contained-html",
        "--timeout=300",  # 5 minute timeout per test
        "--timeout-method=thread",  # Use thread method for timeout
    ]
    
    print(f"[🔧] Running pytest with args: {' '.join(pytest_args)}")
    print(f"[📱] Testing devices: {os.environ['TEST_DEVICES']}")
    
    # Run pytest and capture the exit code
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print("\n" + "=" * 80)
        print("✅ THREE MONTH POPULAR PLAN TEST COMPLETED SUCCESSFULLY!")
        print("📊 Check three_month_popular_test_report.html for detailed results")
        print("=" * 80)
        return True
    else:
        print("\n" + "=" * 80)
        print(f"❌ THREE MONTH POPULAR PLAN TEST FAILED with exit code: {exit_code}")
        print("📊 Check three_month_popular_test_report.html for detailed results")
        print("=" * 80)
        return False


def run_mobile_only_test():
    """Run the three-month popular plan test on mobile devices only"""
    
    print("=" * 80)
    print("📱 THREE MONTH POPULAR PLAN TEST - MOBILE DEVICES ONLY")
    print("=" * 80)
    print("📱 Devices: iPhone X → iPad Pro → Samsung Galaxy S21")
    print("⏱️  Browser will stay open for 10 seconds after each test")
    print("=" * 80)
    
    # Set environment to force mobile testing only
    os.environ["MOBILE_TEST"] = "true"
    
    # Run pytest with mobile-only configuration
    pytest_args = [
        "tests/test_purchase_membership_question_by_three_month_popular_plan.py",
        "-v",
        "--tb=short",
        "--capture=no",
        "-s",
        "--html=mobile_three_month_popular_test_report.html",
        "--self-contained-html",
        "--timeout=300",
        "--timeout-method=thread",
    ]
    
    print(f"[🔧] Running pytest with mobile-only configuration")
    print(f"[📱] Testing mobile devices only")
    
    # Run pytest and capture the exit code
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print("\n" + "=" * 80)
        print("✅ MOBILE THREE MONTH POPULAR PLAN TEST COMPLETED SUCCESSFULLY!")
        print("📊 Check mobile_three_month_popular_test_report.html for detailed results")
        print("=" * 80)
        return True
    else:
        print("\n" + "=" * 80)
        print(f"❌ MOBILE THREE MONTH POPULAR PLAN TEST FAILED with exit code: {exit_code}")
        print("📊 Check mobile_three_month_popular_test_report.html for detailed results")
        print("=" * 80)
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "mobile":
        success = run_mobile_only_test()
    else:
        success = run_three_month_popular_test()
    
    sys.exit(0 if success else 1) 
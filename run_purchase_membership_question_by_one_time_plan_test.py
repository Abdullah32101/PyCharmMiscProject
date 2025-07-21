#!/usr/bin/env python3
"""
Purchase Membership Question by One-Time Plan Test Runner with Mobile Support
This script runs the one-time plan test on multiple devices with database integration.
"""

import pytest
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def run_onetime_test():
    """Run the one-time plan test on multiple devices using pytest for database integration"""
    
    print("[📱] Starting one-time plan test with mobile support and database integration...")
    
    # Set environment variable to indicate mobile testing
    os.environ["MOBILE_TEST"] = "true"
    
    # Run pytest with mobile-specific configuration
    # This will use the conftest.py fixtures for database integration
    pytest_args = [
        "tests/test_purchase_membership_question_by_one_time_plan.py::test_purchase_membership_question_by_one_time_plan",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--capture=no",  # Show print statements
        "-s",  # Don't capture stdout/stderr
        "--html=onetime_test_report.html",
        "--self-contained-html"
    ]
    
    # Run pytest and capture the exit code
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print("[✅] One-time plan test completed successfully with database logging!")
        return True
    else:
        print(f"[❌] One-time plan test failed with exit code: {exit_code}")
        return False

def run_mobile_onetime_test():
    """Run the one-time plan test specifically on mobile devices"""
    
    print("[📱] Starting mobile-specific one-time plan test...")
    
    # Set environment variable to force mobile testing
    os.environ["MOBILE_TEST"] = "true"
    os.environ["TEST_DEVICES"] = "iPhone X,iPad Pro"
    
    # Run pytest with mobile devices only
    pytest_args = [
        "tests/test_purchase_membership_question_by_one_time_plan.py::test_purchase_membership_question_by_one_time_plan",
        "-v",
        "--tb=short",
        "--capture=no",
        "-s",
        "--html=mobile_onetime_test_report.html",
        "--self-contained-html"
    ]
    
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print("[✅] Mobile one-time plan test completed successfully!")
        return True
    else:
        print(f"[❌] Mobile one-time plan test failed with exit code: {exit_code}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("PURCHASE MEMBERSHIP QUESTION BY ONE-TIME PLAN TEST RUNNER")
    print("=" * 60)
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "mobile":
        success = run_mobile_onetime_test()
    else:
        success = run_onetime_test()
    
    if success:
        print("\n[🎉] All tests passed!")
        print("[💾] Test results have been logged to the database.")
        print("[📄] HTML reports generated:")
        if len(sys.argv) > 1 and sys.argv[1] == "mobile":
            print("   - mobile_onetime_test_report.html")
        else:
            print("   - onetime_test_report.html")
        sys.exit(0)
    else:
        print("\n[❌] Tests failed!")
        print("[📸] Check for screenshot files in the current directory")
        sys.exit(1) 
#!/usr/bin/env python3
"""
Purchase Membership Question by Three Month Popular Plan Test Runner with Mobile Support
This script runs the popular plan test on multiple devices with database integration.
"""

import os
import sys
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def run_popular_test():
    """Run the popular plan test sequentially: desktop first, then mobile devices one by one"""

    print("[🚀] Starting popular plan test sequentially...")
    print("[📋] Order: Desktop → iPhone X → iPad Pro → Samsung Galaxy S21")

    # Define devices in order: desktop first, then mobile
    devices = ["desktop", "iPhone X", "iPad Pro", "Samsung Galaxy S21"]
    
    all_passed = True
    
    for i, device in enumerate(devices):
        print(f"\n{'='*60}")
        print(f"🔄 [{i+1}/{len(devices)}] Testing on: {device}")
        print(f"{'='*60}")
        
        # Set environment variable for this specific device
        os.environ["TEST_DEVICES"] = device
        
        # Run pytest for this device only
        pytest_args = [
            "tests/test_purchase_membership_question_by_three_month_popular_plan.py::test_purchase_membership_question_by_three_month_popular_plan",
            "-v",  # Verbose output
            "--tb=short",  # Short traceback format
            "--capture=no",  # Show print statements
            "-s",  # Don't capture stdout/stderr
            f"--html=popular_test_{device.lower().replace(' ', '_')}_report.html",
            "--self-contained-html",
            "--timeout=300",  # 5 minute timeout per test
            "--timeout-method=thread",  # Use thread method for timeout
        ]

        # Run pytest for this device
        exit_code = pytest.main(pytest_args)
        
        if exit_code == 0:
            print(f"✅ {device} test PASSED")
        else:
            print(f"❌ {device} test FAILED")
            all_passed = False
        
        # Force cleanup after each test to prevent hanging
        print(f"🧹 Cleaning up {device} test resources...")
        
        # Kill any remaining Chrome processes for this test
        try:
            import subprocess
            if os.name == 'nt':  # Windows
                subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], 
                             capture_output=True, timeout=10)
                subprocess.run(['taskkill', '/f', '/im', 'chromedriver.exe'], 
                             capture_output=True, timeout=10)
            else:  # Linux/Mac
                subprocess.run(['pkill', '-f', 'chrome'], 
                             capture_output=True, timeout=10)
                subprocess.run(['pkill', '-f', 'chromedriver'], 
                             capture_output=True, timeout=10)
            print(f"✅ Cleaned up {device} processes")
        except Exception as cleanup_error:
            print(f"⚠️ Cleanup warning: {cleanup_error}")
        
        # Wait between devices (except after the last one)
        if i < len(devices) - 1:
            print("⏳ Waiting 5 seconds before next device...")
            time.sleep(5)
    
    if all_passed:
        print("\n🎉 ALL DEVICES PASSED!")
        return True
    else:
        print("\n⚠️ Some devices failed. Check individual reports.")
        return False


def run_mobile_popular_test():
    """Run the popular plan test specifically on mobile devices only"""

    print("[📱] Starting mobile-only popular plan test...")
    print("[📋] Order: iPhone X → iPad Pro → Samsung Galaxy S21")

    # Define mobile devices only
    devices = ["iPhone X", "iPad Pro", "Samsung Galaxy S21"]
    
    all_passed = True
    
    for i, device in enumerate(devices):
        print(f"\n{'='*60}")
        print(f"🔄 [{i+1}/{len(devices)}] Testing on: {device}")
        print(f"{'='*60}")
        
        # Set environment variable for this specific device
        os.environ["TEST_DEVICES"] = device
        
        # Run pytest for this device only
        pytest_args = [
            "tests/test_purchase_membership_question_by_three_month_popular_plan.py::test_purchase_membership_question_by_three_month_popular_plan",
            "-v",
            "--tb=short",
            "--capture=no",
            "-s",
            f"--html=mobile_popular_{device.lower().replace(' ', '_')}_report.html",
            "--self-contained-html",
            "--timeout=300",  # 5 minute timeout per test
            "--timeout-method=thread",  # Use thread method for timeout
        ]

        # Run pytest for this device
        exit_code = pytest.main(pytest_args)
        
        if exit_code == 0:
            print(f"✅ {device} test PASSED")
        else:
            print(f"❌ {device} test FAILED")
            all_passed = False
        
        # Force cleanup after each test to prevent hanging
        print(f"🧹 Cleaning up {device} test resources...")
        
        # Kill any remaining Chrome processes for this test
        try:
            import subprocess
            if os.name == 'nt':  # Windows
                subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], 
                             capture_output=True, timeout=10)
                subprocess.run(['taskkill', '/f', '/im', 'chromedriver.exe'], 
                             capture_output=True, timeout=10)
            else:  # Linux/Mac
                subprocess.run(['pkill', '-f', 'chrome'], 
                             capture_output=True, timeout=10)
                subprocess.run(['pkill', '-f', 'chromedriver'], 
                             capture_output=True, timeout=10)
            print(f"✅ Cleaned up {device} processes")
        except Exception as cleanup_error:
            print(f"⚠️ Cleanup warning: {cleanup_error}")
        
        # Wait between devices (except after the last one)
        if i < len(devices) - 1:
            print("⏳ Waiting 5 seconds before next device...")
            time.sleep(5)
    
    if all_passed:
        print("\n🎉 ALL MOBILE DEVICES PASSED!")
        return True
    else:
        print("\n⚠️ Some mobile devices failed. Check individual reports.")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("PURCHASE MEMBERSHIP QUESTION BY THREE MONTH POPULAR PLAN TEST RUNNER")
    print("=" * 60)

    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "mobile":
        success = run_mobile_popular_test()
    else:
        success = run_popular_test()

    if success:
        print("\n[🎉] All tests passed!")
        print("[💾] Test results have been logged to the database.")
        print("[📄] HTML reports generated:")
        if len(sys.argv) > 1 and sys.argv[1] == "mobile":
            print("   - mobile_popular_test_report.html")
        else:
            print("   - popular_test_report.html")
        sys.exit(0)
    else:
        print("\n[❌] Tests failed!")
        print("[📸] Check for screenshot files in the current directory")
        sys.exit(1)

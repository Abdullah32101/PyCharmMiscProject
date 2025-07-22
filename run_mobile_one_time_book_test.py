#!/usr/bin/env python3
"""
Mobile One-Time Book Purchase Test Runner
This script runs the one-time book purchase test specifically on mobile devices to verify the fixes.
"""

import os
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def run_mobile_book_test():
    """Run the one-time book purchase test on mobile devices using pytest for database integration"""

    print(
        "[📱] Starting mobile one-time book purchase test with database integration..."
    )

    # Set environment variable to indicate mobile testing
    os.environ["MOBILE_TEST"] = "true"

    # Run pytest with mobile-specific configuration
    # This will use the conftest.py fixtures for database integration
    pytest_args = [
        "tests/test_one_time_book_purchase.py::test_book_page_load_and_click",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--capture=no",  # Show print statements
        "-s",  # Don't capture stdout/stderr
    ]

    # Run pytest and capture the exit code
    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        print(
            "[✅] Mobile one-time book purchase test completed successfully with database logging!"
        )
        return True
    else:
        print(
            f"[❌] Mobile one-time book purchase test failed with exit code: {exit_code}"
        )
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("MOBILE ONE-TIME BOOK PURCHASE TEST RUNNER")
    print("=" * 60)

    success = run_mobile_book_test()

    if success:
        print("\n[🎉] All tests passed!")
        print("[💾] Test results have been logged to the database.")
        sys.exit(0)
    else:
        print("\n[❌] Tests failed!")
        sys.exit(1)

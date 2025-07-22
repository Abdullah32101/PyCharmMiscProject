#!/usr/bin/env python3
"""
Debug script to test error link capture logic
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from db.db_helper import MySQLHelper
from screenshot_utils import screenshot_manager


def test_error_link_debug():
    """Debug test to understand why error links are not being captured"""

    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    try:
        # Navigate to a page
        driver.get("https://www.google.com")

        # Test screenshot capture directly
        test_name = "debug_error_link_test"
        file_path, error_link = screenshot_manager.capture_screenshot(
            driver, test_name, stage="debug", error=True
        )

        print(f"[📸] Screenshot captured: {file_path}")
        print(f"[🔗] Error link generated: {error_link}")

        # Test database storage directly
        db_helper = MySQLHelper()

        # Store test result with error link
        db_helper.store_test_result_in_tables(
            test_name,
            "debug_test",
            "FAILED",
            "Debug test error message",
            None,  # test_data
            1.0,  # total_time_duration
            "desktop",
            "1920x1080",
            error_link,
        )

        print("[✅] Test result stored with error link")

        # Verify storage
        results = db_helper.get_test_results(limit=1)
        if results:
            latest_result = results[0]
            # Access the result as a dictionary
            stored_error_link = None
            if hasattr(latest_result, "__dict__"):
                stored_error_link = getattr(latest_result, "error_link", None)
            elif isinstance(latest_result, dict):
                stored_error_link = latest_result.get("error_link")
            else:
                # Try to access as tuple/list
                stored_error_link = (
                    latest_result[10] if len(latest_result) > 10 else None
                )

            print(f"[🔍] Stored error link: {stored_error_link}")

            if stored_error_link == error_link:
                print("[✅] Error link storage verification passed!")
            else:
                print(
                    f"[❌] Error link mismatch: expected {error_link}, got {stored_error_link}"
                )

        db_helper.close()

    except Exception as e:
        print(f"[❌] Debug test failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        driver.quit()


if __name__ == "__main__":
    print("🔍 Debug Error Link Capture")
    print("=" * 50)
    test_error_link_debug()

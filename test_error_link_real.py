#!/usr/bin/env python3
"""
Test to verify error link capture with real test failure
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from db.db_helper import MySQLHelper
from screenshot_utils import screenshot_manager


@pytest.fixture
def driver():
    """Setup Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )
    yield driver
    driver.quit()


def test_error_link_capture_real_failure(driver):
    """Test that intentionally fails to capture error link"""

    # Navigate to a page
    driver.get("https://www.google.com")

    # This will intentionally fail to trigger error link capture
    assert False, "Intentional test failure to test error link capture"


def test_error_link_capture_success(driver):
    """Test that passes to verify no error link is captured"""

    # Navigate to a page
    driver.get("https://www.google.com")

    # This should pass
    assert "Google" in driver.title


if __name__ == "__main__":
    print("🧪 Testing Error Link Capture with Real Test")
    print("=" * 50)

    # This will run the tests and show the results
    pytest.main([__file__, "-v"])

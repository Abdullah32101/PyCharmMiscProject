#!/usr/bin/env python3
"""
Simple CI Smoke Tests for GitHub Actions
These tests are designed to work reliably in CI environment.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_basic_page_load(driver):
    """Basic test to verify page loads in CI"""
    try:
        print(f"[🚀] Starting basic smoke test")

        # Navigate to a simple page
        driver.get("https://httpbin.org/html")

        # Wait for page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        # Verify page title
        assert "Herman Melville" in driver.title

        print(f"[✅] Basic smoke test passed")

    except Exception as e:
        print(f"[❌] Basic smoke test failed: {e}")
        raise


def test_selenium_functionality(driver):
    """Test basic Selenium functionality"""
    try:
        print(f"[🧪] Testing Selenium functionality")

        # Test basic navigation
        driver.get("https://httpbin.org/html")

        # Test element finding
        element = driver.find_element(By.TAG_NAME, "h1")
        assert element.text == "Herman Melville - Moby-Dick"

        print(f"[✅] Selenium functionality test passed")

    except Exception as e:
        print(f"[❌] Selenium functionality test failed: {e}")
        raise


def test_google_page(driver):
    """Test Google page loading"""
    try:
        print(f"[🌐] Testing Google page")

        # Navigate to Google
        driver.get("https://www.google.com")

        # Wait for search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        # Verify search box is present
        assert search_box.is_displayed()

        print(f"[✅] Google page test passed")

    except Exception as e:
        print(f"[❌] Google page test failed: {e}")
        raise


if __name__ == "__main__":
    print("🧪 Simple CI Smoke Tests")
    print("=" * 50)
    pytest.main([__file__, "-v"]) 
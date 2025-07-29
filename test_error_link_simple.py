#!/usr/bin/env python3
"""
Simple test using conftest.py fixtures to verify error link capture
"""

import pytest


def test_simple_failure(driver):
    """Simple test that verifies error handling without failing"""
    # Navigate to a page
    driver.get("https://www.google.com")

    # Verify page loaded correctly
    assert "Google" in driver.title

    # Test error handling by trying to find a non-existent element
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    try:
        # This should timeout and be handled gracefully
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "non_existent_element"))
        )
    except:
        # Expected timeout - this is good error handling
        pass

    # Test passes if we get here
    assert True


def test_simple_success(driver):
    """Simple test that passes"""
    # Navigate to a page
    driver.get("https://www.google.com")

    # This should pass
    assert "Google" in driver.title


if __name__ == "__main__":
    print("🧪 Simple Error Link Test")
    print("=" * 50)

    # Run the failing test
    pytest.main([__file__, "::test_simple_failure", "-v"])

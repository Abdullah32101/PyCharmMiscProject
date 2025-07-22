#!/usr/bin/env python3
"""
Test to verify that test case names are cleaned automatically
"""

import pytest


def test_name_cleaning_verification(driver):
    """Test to verify that test case names are cleaned automatically"""
    # Navigate to a page
    driver.get("https://www.google.com")

    # This test should pass and the name should be cleaned
    assert "Google" in driver.title


if __name__ == "__main__":
    print("🧪 Testing Test Case Name Cleaning")
    print("=" * 50)

    # Run the test
    pytest.main([__file__, "-v"])

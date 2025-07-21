#!/usr/bin/env python3
"""
Simple test using conftest.py fixtures to verify error link capture
"""

import pytest

def test_simple_failure(driver):
    """Simple test that fails to trigger error link capture"""
    # Navigate to a page
    driver.get("https://www.google.com")
    
    # This will fail and should trigger error link capture
    assert False, "Simple test failure to verify error link capture"

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
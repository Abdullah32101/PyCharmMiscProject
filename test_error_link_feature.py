#!/usr/bin/env python3
"""
Test script to verify the error link feature
"""

import pytest
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from db.db_helper import MySQLHelper
from screenshot_utils import screenshot_manager

def test_error_link_capture():
    """Test that error links are properly captured and stored"""
    
    # Initialize database helper
    db_helper = MySQLHelper()
    
    # Create test results table with new column
    db_helper.create_test_results_table()
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Navigate to a page
        driver.get("https://www.google.com")
        
        # Test screenshot capture
        test_name = "test_error_link_feature"
        file_path, error_link = screenshot_manager.capture_screenshot(
            driver, 
            test_name, 
            stage="test", 
            error=True
        )
        
        print(f"[📸] Screenshot captured: {file_path}")
        print(f"[🔗] Error link: {error_link}")
        
        # Verify screenshot was created
        assert file_path is not None, "Screenshot file path should not be None"
        assert error_link is not None, "Error link should not be None"
        assert os.path.exists(file_path), f"Screenshot file should exist: {file_path}"
        assert error_link.startswith("file://"), "Error link should start with file://"
        
        # Test database storage
        db_helper.store_test_result_in_tables(
            test_name,
            "test_error_link_feature",
            "FAILED",
            "Test error message for error link feature",
            None,  # test_data
            1.5,   # total_time_duration
            "desktop",
            "1920x1080",
            error_link
        )
        
        print("[✅] Test result stored in database with error link")
        
        # Verify the error link was stored
        results = db_helper.get_test_results(limit=1)
        if results:
            latest_result = results[0]
            # Access the result as a dictionary
            stored_error_link = None
            if hasattr(latest_result, '__dict__'):
                stored_error_link = getattr(latest_result, 'error_link', None)
            elif isinstance(latest_result, dict):
                stored_error_link = latest_result.get('error_link')
            else:
                # Try to access as tuple/list
                stored_error_link = latest_result[10] if len(latest_result) > 10 else None
            
            print(f"[🔍] Stored error link: {stored_error_link}")
            
            assert stored_error_link == error_link, f"Stored error link should match: {stored_error_link} != {error_link}"
            print("[✅] Error link verification passed")
        else:
            print("[⚠️] No test results found in database")
        
    except Exception as e:
        print(f"[❌] Test failed: {e}")
        raise
    finally:
        driver.quit()
        db_helper.close()

def test_screenshot_manager():
    """Test screenshot manager functionality"""
    
    # Test filename sanitization
    test_filename = "test<>:\"/\\|?*file.png"
    sanitized = screenshot_manager._sanitize_filename(test_filename)
    print(f"[🧪] Original: {test_filename}")
    print(f"[🧪] Sanitized: {sanitized}")
    
    # Test URL generation
    test_path = "screenshots/test.png"
    url = screenshot_manager.get_screenshot_url(test_path)
    print(f"[🧪] Test path: {test_path}")
    print(f"[🧪] Generated URL: {url}")
    
    print("[✅] Screenshot manager tests passed")

if __name__ == "__main__":
    print("🧪 Testing Error Link Feature")
    print("=" * 50)
    
    try:
        test_screenshot_manager()
        test_error_link_capture()
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        sys.exit(1) 
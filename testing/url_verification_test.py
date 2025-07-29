#!/usr/bin/env python3
"""
URL Verification Test
Test to verify which URL is being used and check page content.
"""

import sys
import os
import time

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from core.constants import BOOK_URL


def verify_urls():
    """Verify which URLs are being used and their content"""
    print("🔍 URL Verification Test")
    print("=" * 40)
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Test the main book URL
        print(f"\n📋 Testing BOOK_URL: {BOOK_URL}")
        print("-" * 50)
        
        try:
            # Navigate to URL
            driver.get(BOOK_URL)
            time.sleep(3)
            
            # Get current URL after navigation
            current_url = driver.current_url
            page_title = driver.title
            
            print(f"📍 Current URL: {current_url}")
            print(f"📝 Page Title: {page_title}")
            
            # Check if redirected to membership page
            if "membership" in current_url.lower() or "membership" in page_title.lower():
                print("⚠️  REDIRECTED TO MEMBERSHIP PAGE!")
            elif "checkout" in current_url.lower():
                print("✅ Direct checkout page detected")
            elif "textbook" in current_url.lower():
                print("✅ Textbook page detected")
            else:
                print("❓ Unknown page type")
            
            # Check for specific elements
            try:
                # Look for book purchase elements
                book_elements = driver.find_elements(By.CSS_SELECTOR, "[id*='book'], [class*='book'], [id*='textbook'], [class*='textbook']")
                print(f"📚 Book-related elements found: {len(book_elements)}")
                
                # Look for membership elements
                membership_elements = driver.find_elements(By.CSS_SELECTOR, "[id*='membership'], [class*='membership'], [id*='plan'], [class*='plan']")
                print(f"💳 Membership-related elements found: {len(membership_elements)}")
                
                # Look for checkout elements
                checkout_elements = driver.find_elements(By.CSS_SELECTOR, "[id*='checkout'], [class*='checkout'], [id*='payment'], [class*='payment']")
                print(f"🛒 Checkout-related elements found: {len(checkout_elements)}")
                
            except Exception as e:
                print(f"❌ Error checking elements: {e}")
            
            # Take screenshot
            screenshot_name = f"url_test_BOOK_URL_{int(time.time())}.png"
            driver.save_screenshot(screenshot_name)
            print(f"📸 Screenshot saved: {screenshot_name}")
            
        except Exception as e:
            print(f"❌ Error testing BOOK_URL: {e}")
        
        print()
        
        # Test the actual book page method
        print("\n📋 Testing actual book page method")
        print("-" * 50)
        
        try:
            from pages.one_time_book_purchase_methods import OneTimeBookPurchasePage
            page = OneTimeBookPurchasePage(driver)
            page.open_book_page()
            
            current_url = driver.current_url
            page_title = driver.title
            
            print(f"📍 Final URL after open_book_page(): {current_url}")
            print(f"📝 Final Page Title: {page_title}")
            
            # Take final screenshot
            screenshot_name = f"final_book_page_{int(time.time())}.png"
            driver.save_screenshot(screenshot_name)
            print(f"📸 Final screenshot saved: {screenshot_name}")
            
        except Exception as e:
            print(f"❌ Error testing book page method: {e}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        driver.quit()


def main():
    """Main function"""
    verify_urls()


if __name__ == "__main__":
    main() 
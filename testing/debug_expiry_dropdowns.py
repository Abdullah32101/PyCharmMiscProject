#!/usr/bin/env python3
"""
Debug Expiry Dropdowns
This script helps identify why expiry date dropdowns are not being selected properly.
"""

import sys
import os
import time
from datetime import datetime

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.one_time_book_purchase_methods import OneTimeBookPurchasePage
from core.constants import BOOK_URL

def debug_expiry_dropdowns():
    """Debug script to inspect expiry dropdown elements on book purchase page"""
    print("🔍 Debugging Expiry Dropdowns on Book Purchase Page")
    print("=" * 60)
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to book purchase page
        print(f"[🌐] Loading book purchase page: {BOOK_URL}")
        driver.get(BOOK_URL)
        time.sleep(3)
        
        # Create page object
        page = OneTimeBookPurchasePage(driver)
        
        # Go through the purchase flow to reach payment section
        print("[📋] Following purchase flow to reach payment section...")
        
        # Step 1: Click 'Get Free Textbook'
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "submit_btn_checkout"))
            )
            page.click_get_free_textbook()
            print("[✅] Clicked 'Get Free Textbook'")
        except Exception as e:
            print(f"[❌] Failed to click 'Get Free Textbook': {e}")
            return
        
        # Step 2: Click 'Proceed to Checkout'
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn_checkout"))
            )
            page.click_proceed_to_checkout()
            print("[✅] Clicked 'Proceed to Checkout'")
        except Exception as e:
            print(f"[❌] Failed to click 'Proceed to Checkout': {e}")
            return
        
        # Step 3: Register a New User
        try:
            page.click_register_link()
            page.enter_email()
            page.enter_password()
            page.enter_university()
            page.click_signup_button()
            print("[✅] Completed user registration")
        except Exception as e:
            print(f"[❌] Failed user registration: {e}")
            return
        
        # Step 4: Fill Billing Details
        try:
            page.fill_billing_details()
            print("[✅] Filled billing details")
        except Exception as e:
            print(f"[❌] Failed to fill billing details: {e}")
            return
        
        # Step 5: Select Card Payment Method
        try:
            page.click_payment_toggle()
            print("[✅] Selected card payment method")
        except Exception as e:
            print(f"[❌] Failed to select card payment: {e}")
            return
        
        # Step 6: Wait for Card Input to Appear
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "cc_num"))
            )
            print("[✅] Card input form appeared")
        except Exception as e:
            print(f"[❌] Card input form did not appear: {e}")
            return
        
        # Step 7: Enter Card Details
        try:
            page.enter_card_details()
            print("[✅] Entered card details")
        except Exception as e:
            print(f"[❌] Failed to enter card details: {e}")
            return
        
        # Now inspect the dropdown elements
        print("\n🔍 INSPECTING DROPDOWN ELEMENTS:")
        print("-" * 40)
        
        # Check for month dropdown
        month_selectors = ["cc_expiry_month", "cc-exp-month", "cc_exp_month", "expiry_month", "month"]
        print("📅 Month Dropdown Elements:")
        for selector in month_selectors:
            try:
                element = driver.find_element(By.ID, selector)
                tag_name = element.tag_name
                element_type = element.get_attribute("type")
                element_class = element.get_attribute("class")
                print(f"  ✅ Found: {selector}")
                print(f"     Tag: {tag_name}, Type: {element_type}, Class: {element_class}")
                
                # If it's a select element, show options
                if tag_name.lower() == "select":
                    options = element.find_elements(By.TAG_NAME, "option")
                    print(f"     Options: {[opt.text for opt in options[:5]]}...")
                else:
                    print(f"     Not a select element")
                    
            except Exception as e:
                print(f"  ❌ Not found: {selector}")
        
        # Check for year dropdown
        year_selectors = ["cc_expiry_year", "cc-exp-year", "cc_exp_year", "expiry_year", "year"]
        print("\n📅 Year Dropdown Elements:")
        for selector in year_selectors:
            try:
                element = driver.find_element(By.ID, selector)
                tag_name = element.tag_name
                element_type = element.get_attribute("type")
                element_class = element.get_attribute("class")
                print(f"  ✅ Found: {selector}")
                print(f"     Tag: {tag_name}, Type: {element_type}, Class: {element_class}")
                
                # If it's a select element, show options
                if tag_name.lower() == "select":
                    options = element.find_elements(By.TAG_NAME, "option")
                    print(f"     Options: {[opt.text for opt in options[:5]]}...")
                else:
                    print(f"     Not a select element")
                    
            except Exception as e:
                print(f"  ❌ Not found: {selector}")
        
        # Check for any dropdown-like elements
        print("\n🔍 All Dropdown-like Elements:")
        dropdown_elements = driver.find_elements(By.CSS_SELECTOR, "select, [role='listbox'], [class*='dropdown'], [class*='select']")
        for i, element in enumerate(dropdown_elements[:10]):  # Show first 10
            element_id = element.get_attribute("id")
            element_name = element.get_attribute("name")
            element_class = element.get_attribute("class")
            print(f"  {i+1}. ID: {element_id}, Name: {element_name}, Class: {element_class}")
        
        # Take screenshot for visual inspection
        screenshot_name = f"debug_dropdowns_{int(time.time())}.png"
        driver.save_screenshot(screenshot_name)
        print(f"\n📸 Screenshot saved: {screenshot_name}")
        
        # Save page source for inspection
        with open(f"debug_page_source_{int(time.time())}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"📄 Page source saved for inspection")
        
    except Exception as e:
        print(f"[❌] Debug failed: {type(e).__name__} – {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_expiry_dropdowns() 
#!/usr/bin/env python3
"""
Quick Dropdown Test
Quick test to verify dropdown selection is working.
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
from pages.one_time_book_purchase_methods import OneTimeBookPurchasePage


def quick_dropdown_test():
    """Quick test for dropdown selection"""
    print("🚀 Quick Dropdown Test")
    print("=" * 30)
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        page = OneTimeBookPurchasePage(driver)
        
        # Step 1: Open the book page
        print("\n📋 Step 1: Opening book page...")
        page.open_book_page()
        
        # Step 2: Quick navigation to payment section
        print("\n📋 Step 2: Quick navigation to payment section...")
        
        # Click 'Get Free Textbook'
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "submit_btn_checkout"))
        )
        page.click_get_free_textbook()
        
        # Click 'Proceed to Checkout'
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "btn_checkout"))
        )
        page.click_proceed_to_checkout()
        
        # Quick registration
        page.click_register_link()
        page.enter_email()
        page.enter_password()
        page.enter_university()
        page.click_signup_button()
        
        # Quick billing
        page.fill_billing_details()
        
        # Quick payment toggle
        print("\n📋 Step 3: Quick payment toggle...")
        page.click_payment_toggle()
        
        # Wait for card input
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "cc_num"))
        )
        
        # Quick card details
        page.enter_card_details()
        
        # Step 4: Test dropdown selection
        print("\n📋 Step 4: Testing dropdown selection...")
        
        # Test month dropdown
        print("Testing month dropdown...")
        page.select_expiry_month("March (03)")
        
        # Test year dropdown
        print("Testing year dropdown...")
        page.select_expiry_year("2032")
        
        # Step 5: Verify dropdown values
        print("\n📋 Step 5: Verifying dropdown values...")
        
        month_value = driver.execute_script("""
            let dropdown = document.getElementById('cc_expiry_month');
            return dropdown ? dropdown.value : 'NOT_FOUND';
        """)
        
        year_value = driver.execute_script("""
            let dropdown = document.getElementById('cc_expiry_year');
            return dropdown ? dropdown.value : 'NOT_FOUND';
        """)
        
        print(f"Month dropdown value: {month_value}")
        print(f"Year dropdown value: {year_value}")
        
        if month_value == "03" and year_value == "2032":
            print("✅ Dropdown selection successful!")
        else:
            print("❌ Dropdown selection failed!")
        
        # Take screenshot
        screenshot_name = f"quick_dropdown_test_{int(time.time())}.png"
        driver.save_screenshot(screenshot_name)
        print(f"✅ Screenshot saved: {screenshot_name}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        try:
            screenshot_name = f"quick_dropdown_error_{int(time.time())}.png"
            driver.save_screenshot(screenshot_name)
            print(f"✅ Error screenshot saved: {screenshot_name}")
        except:
            pass
    finally:
        driver.quit()


def check_dropdowns_on_page(url, page_name):
    """Check what dropdown elements exist on a given page"""
    print(f"\n🔍 Checking dropdowns on {page_name}")
    print(f"URL: {url}")
    print("-" * 50)
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for speed
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to page
        driver.get(url)
        time.sleep(3)
        
        # Find all select elements
        select_elements = driver.find_elements(By.TAG_NAME, "select")
        print(f"📊 Found {len(select_elements)} select elements")
        
        for i, select in enumerate(select_elements):
            try:
                element_id = select.get_attribute("id") or "NO_ID"
                element_name = select.get_attribute("name") or "NO_NAME"
                element_class = select.get_attribute("class") or "NO_CLASS"
                
                print(f"\n📋 Select Element {i+1}:")
                print(f"   ID: {element_id}")
                print(f"   Name: {element_name}")
                print(f"   Class: {element_class}")
                
                # Get all options
                options = select.find_elements(By.TAG_NAME, "option")
                print(f"   Options count: {len(options)}")
                
                # Show first few options
                for j, option in enumerate(options[:3]):
                    option_value = option.get_attribute("value") or "NO_VALUE"
                    option_text = option.text or "NO_TEXT"
                    print(f"     Option {j+1}: value='{option_value}', text='{option_text}'")
                
                if len(options) > 3:
                    print(f"     ... and {len(options) - 3} more options")
                
                # Check if this looks like an expiry dropdown
                if any(keyword in element_id.lower() for keyword in ["month", "exp", "year"]):
                    print(f"   🎯 This looks like an expiry dropdown!")
                    
            except Exception as e:
                print(f"   ❌ Error analyzing select element {i+1}: {e}")
        
        # Also check for any input elements that might be dropdowns
        input_elements = driver.find_elements(By.CSS_SELECTOR, "input[list], input[type='text'][class*='dropdown'], input[class*='select']")
        print(f"\n📊 Found {len(input_elements)} input elements that might be dropdowns")
        
        for i, input_elem in enumerate(input_elements):
            try:
                element_id = input_elem.get_attribute("id") or "NO_ID"
                element_name = input_elem.get_attribute("name") or "NO_NAME"
                element_class = input_elem.get_attribute("class") or "NO_CLASS"
                element_type = input_elem.get_attribute("type") or "NO_TYPE"
                
                print(f"\n📋 Input Element {i+1}:")
                print(f"   ID: {element_id}")
                print(f"   Name: {element_name}")
                print(f"   Class: {element_class}")
                print(f"   Type: {element_type}")
                
                # Check if this looks like an expiry dropdown
                if any(keyword in element_id.lower() for keyword in ["month", "exp", "year"]):
                    print(f"   🎯 This looks like an expiry dropdown!")
                    
            except Exception as e:
                print(f"   ❌ Error analyzing input element {i+1}: {e}")
        
    except Exception as e:
        print(f"❌ Error checking {page_name}: {e}")
    finally:
        driver.quit()


def main():
    """Compare dropdowns between book purchase and membership question pages"""
    print("🔍 Comparing Dropdown Elements Between Pages")
    print("=" * 60)
    
    # Check book purchase page
    from core.constants import BOOK_URL
    check_dropdowns_on_page(BOOK_URL, "Book Purchase Page")
    
    # Check membership question page
    from core.constants import PRIMARY_URL
    check_dropdowns_on_page(PRIMARY_URL, "Membership Question Page")

if __name__ == "__main__":
    main() 
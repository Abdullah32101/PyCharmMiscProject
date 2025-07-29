#!/usr/bin/env python3
"""
Debug script to investigate the toggle button issue in monthly plan test
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from pages.purchase_membership_question_by_monthly_plan_methods import SolutionInnPrimaryPage
from core.constants import PRIMARY_URL

def debug_toggle_button_issue():
    """Debug the toggle button issue step by step"""
    
    print("🔍 Starting toggle button debug...")
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=chrome_options
    )
    
    try:
        page = SolutionInnPrimaryPage(driver)
        
        print("📄 Step 1: Opening primary page...")
        page.open()
        time.sleep(3)
        
        print("🔍 Step 2: Looking for View Solution button...")
        page.click_view_solution_button()
        time.sleep(3)
        
        print("📧 Step 3: Entering email...")
        page.enter_email()
        time.sleep(1)
        
        print("🔐 Step 4: Entering password...")
        page.enter_password()
        time.sleep(1)
        
        print("🏫 Step 5: Entering university...")
        page.enter_university()
        time.sleep(1)
        
        print("📝 Step 6: Clicking signup button...")
        page.click_signup_button()
        time.sleep(5)  # Wait longer for signup to complete
        
        print("🔍 Step 7: Looking for second View Solution button...")
        page.click_view_solution_button()
        time.sleep(3)
        
        print("📱 Step 8: Clicking Monthly Access button...")
        page.click_monthly_access_button()
        time.sleep(5)  # Wait longer for page to load
        
        print("🔍 Step 9: Debugging toggle button...")
        debug_toggle_button(driver)
        
    except Exception as e:
        print(f"❌ Error during debug: {type(e).__name__} - {e}")
        # Take screenshot
        try:
            driver.save_screenshot(f"debug_toggle_failed_{int(time.time())}.png")
            print("📸 Screenshot saved")
        except:
            pass
    finally:
        driver.quit()

def debug_toggle_button(driver):
    """Debug the toggle button specifically"""
    
    print("🔍 Looking for payment toggle elements...")
    
    # Check current URL
    current_url = driver.current_url
    print(f"📍 Current URL: {current_url}")
    
    # Check page title
    page_title = driver.title
    print(f"📄 Page title: {page_title}")
    
    # Look for various toggle-related elements
    toggle_selectors = [
        "//label[@for='radio7']",
        "//input[@id='radio7']",
        "//label[contains(text(), 'Credit Card')]",
        "//label[contains(text(), 'Card')]",
        "//input[@type='radio'][@name='payment_method']",
        "//input[@type='radio']",
        "//label[contains(@class, 'payment')]",
        "//div[contains(@class, 'payment')]//input[@type='radio']",
        "//input[@type='radio']",
        "//label[contains(text(), 'Credit')]",
        "//label[contains(text(), 'Debit')]",
        "//input[@name='payment_method']",
        "//input[@name='payment']",
    ]
    
    print("🔍 Checking for toggle elements...")
    for i, selector in enumerate(toggle_selectors):
        try:
            elements = driver.find_elements(By.XPATH, selector)
            if elements:
                print(f"✅ Found {len(elements)} element(s) with selector {i+1}: {selector}")
                for j, element in enumerate(elements):
                    try:
                        text = element.text if element.tag_name != 'input' else element.get_attribute('value')
                        print(f"   Element {j+1}: tag={element.tag_name}, text='{text}', visible={element.is_displayed()}")
                    except:
                        print(f"   Element {j+1}: tag={element.tag_name}, visible={element.is_displayed()}")
            else:
                print(f"❌ No elements found with selector {i+1}: {selector}")
        except Exception as e:
            print(f"⚠️ Error with selector {i+1}: {type(e).__name__}")
    
    # Check for any radio buttons or payment-related elements
    print("🔍 Looking for any radio buttons...")
    try:
        radio_buttons = driver.find_elements(By.XPATH, "//input[@type='radio']")
        print(f"📻 Found {len(radio_buttons)} radio buttons")
        for i, radio in enumerate(radio_buttons):
            try:
                name = radio.get_attribute('name')
                value = radio.get_attribute('value')
                id_attr = radio.get_attribute('id')
                print(f"   Radio {i+1}: name='{name}', value='{value}', id='{id_attr}', visible={radio.is_displayed()}")
            except:
                print(f"   Radio {i+1}: visible={radio.is_displayed()}")
    except Exception as e:
        print(f"⚠️ Error finding radio buttons: {e}")
    
    # Check for payment-related text
    print("🔍 Looking for payment-related text...")
    try:
        payment_texts = driver.find_elements(By.XPATH, "//*[contains(text(), 'Credit') or contains(text(), 'Card') or contains(text(), 'Payment') or contains(text(), 'Debit')]")
        print(f"💳 Found {len(payment_texts)} payment-related text elements")
        for i, element in enumerate(payment_texts[:10]):  # Limit to first 10
            try:
                text = element.text.strip()
                if text:
                    print(f"   Text {i+1}: '{text[:50]}...' (tag: {element.tag_name})")
            except:
                pass
    except Exception as e:
        print(f"⚠️ Error finding payment text: {e}")
    
    # Check page source for payment-related content
    print("🔍 Checking page source for payment content...")
    try:
        page_source = driver.page_source.lower()
        if 'credit' in page_source:
            print("✅ Found 'credit' in page source")
        if 'card' in page_source:
            print("✅ Found 'card' in page source")
        if 'payment' in page_source:
            print("✅ Found 'payment' in page source")
        if 'radio' in page_source:
            print("✅ Found 'radio' in page source")
        if 'toggle' in page_source:
            print("✅ Found 'toggle' in page source")
    except Exception as e:
        print(f"⚠️ Error checking page source: {e}")

if __name__ == "__main__":
    debug_toggle_button_issue() 
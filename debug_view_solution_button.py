#!/usr/bin/env python3
"""
Debug script to find the correct selector for the View Solution button
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from core.constants import PRIMARY_URL

def debug_view_solution_button():
    """Debug the View Solution button selector"""
    
    print("[DEBUG] Starting View Solution button debug...")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Initialize driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        # Navigate to the page
        print(f"[DEBUG] Navigating to: {PRIMARY_URL}")
        driver.get(PRIMARY_URL)
        time.sleep(3)
        
        # Wait for page to load
        print("[DEBUG] Waiting for page to load...")
        time.sleep(5)
        
        # Try to find the View Solution button with different selectors
        selectors_to_try = [
            ".view_solution_btn.step1PopupButton",
            ".view_solution_btn",
            "button.view_solution_btn",
            "[class*='view_solution']",
            "[class*='step1PopupButton']",
            "button[class*='view']",
            "button[class*='solution']",
            "//button[contains(text(), 'View Solution')]",
            "//button[contains(text(), 'view solution')]",
            "//a[contains(text(), 'View Solution')]",
            "//a[contains(text(), 'view solution')]",
            "//*[contains(text(), 'View Solution')]",
            "//*[contains(text(), 'view solution')]",
        ]
        
        print("[DEBUG] Trying different selectors...")
        
        for i, selector in enumerate(selectors_to_try):
            try:
                print(f"[DEBUG] Trying selector {i+1}: {selector}")
                
                if selector.startswith("//"):
                    # XPath selector
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    # CSS selector
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                if elements:
                    print(f"[SUCCESS] Found {len(elements)} element(s) with selector: {selector}")
                    for j, element in enumerate(elements):
                        try:
                            text = element.text.strip()
                            classes = element.get_attribute("class")
                            tag_name = element.tag_name
                            print(f"  Element {j+1}: tag={tag_name}, text='{text}', class='{classes}'")
                            
                            # Check if it's visible and clickable
                            if element.is_displayed():
                                print(f"    - Visible: Yes")
                                if element.is_enabled():
                                    print(f"    - Enabled: Yes")
                                    print(f"    - Clickable: Yes")
                                else:
                                    print(f"    - Enabled: No")
                            else:
                                print(f"    - Visible: No")
                                
                        except Exception as e:
                            print(f"    - Error getting element info: {e}")
                else:
                    print(f"[FAIL] No elements found with selector: {selector}")
                    
            except Exception as e:
                print(f"[ERROR] Error with selector {selector}: {e}")
        
        # Take a screenshot for manual inspection
        print("[DEBUG] Taking screenshot for manual inspection...")
        driver.save_screenshot("debug_view_solution_button.png")
        print("[DEBUG] Screenshot saved as: debug_view_solution_button.png")
        
        # Save page source for analysis
        print("[DEBUG] Saving page source...")
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("[DEBUG] Page source saved as: debug_page_source.html")
        
        # Look for any buttons with "view" or "solution" in their text or class
        print("[DEBUG] Searching for any buttons with 'view' or 'solution'...")
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        
        relevant_elements = []
        for element in all_buttons + all_links:
            try:
                text = element.text.lower()
                classes = element.get_attribute("class").lower()
                if "view" in text or "solution" in text or "view" in classes or "solution" in classes:
                    relevant_elements.append(element)
            except:
                continue
        
        print(f"[DEBUG] Found {len(relevant_elements)} potentially relevant elements:")
        for i, element in enumerate(relevant_elements[:10]):  # Show first 10
            try:
                text = element.text.strip()
                classes = element.get_attribute("class")
                tag_name = element.tag_name
                print(f"  {i+1}. {tag_name}: text='{text}', class='{classes}'")
            except:
                print(f"  {i+1}. Error getting element info")
        
    except Exception as e:
        print(f"[ERROR] Debug failed: {e}")
    finally:
        print("[DEBUG] Closing browser...")
        driver.quit()

if __name__ == "__main__":
    debug_view_solution_button() 
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.purchase_membership_question_by_monthly_plan_methods import SolutionInnPrimaryPage
from core.constants import PRIMARY_URL

def debug_monthly_plan_buttons():
    """Debug script to check what buttons are available on the monthly plan page"""
    print("🔍 Debugging Monthly Plan Buttons")
    print("=" * 50)
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to monthly plan page
        print(f"[🌐] Loading monthly plan page: {PRIMARY_URL}")
        driver.get(PRIMARY_URL)
        time.sleep(3)
        
        # Create page object
        page = SolutionInnPrimaryPage(driver)
        
        # Step 1: Open the page
        print("[📋] Step 1: Opening page...")
        page.open()
        time.sleep(2)
        
        # Step 2: Start registration
        print("[📋] Step 2: Starting registration...")
        page.click_view_solution_button()
        page.enter_email()
        page.enter_password()
        page.enter_university()
        page.click_signup_button()
        time.sleep(3)
        
        # Step 3: Click view solution again to get to plan selection
        print("[📋] Step 3: Clicking view solution again...")
        page.click_view_solution_button()
        time.sleep(3)
        
        # Now analyze what buttons are available
        print("\n🔍 ANALYZING AVAILABLE BUTTONS:")
        print("-" * 40)
        
        # Find all buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"📊 Found {len(buttons)} button elements:")
        
        for i, button in enumerate(buttons):
            try:
                button_text = button.text.strip()
                button_id = button.get_attribute("id") or "NO_ID"
                button_class = button.get_attribute("class") or "NO_CLASS"
                button_type = button.get_attribute("type") or "NO_TYPE"
                
                if button_text:  # Only show buttons with text
                    print(f"\n📋 Button {i+1}:")
                    print(f"   Text: '{button_text}'")
                    print(f"   ID: {button_id}")
                    print(f"   Class: {button_class}")
                    print(f"   Type: {button_type}")
                    
                    # Check if this looks like a plan button
                    if any(keyword in button_text.lower() for keyword in ["monthly", "plan", "access", "view", "solution"]):
                        print(f"   🎯 This looks like a plan button!")
                        
            except Exception as e:
                print(f"   ❌ Error analyzing button {i+1}: {e}")
        
        # Find all links that might be buttons
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"\n📊 Found {len(links)} link elements:")
        
        for i, link in enumerate(links):
            try:
                link_text = link.text.strip()
                link_id = link.get_attribute("id") or "NO_ID"
                link_class = link.get_attribute("class") or "NO_CLASS"
                link_href = link.get_attribute("href") or "NO_HREF"
                
                if link_text and any(keyword in link_text.lower() for keyword in ["monthly", "plan", "access", "view", "solution"]):
                    print(f"\n📋 Link {i+1}:")
                    print(f"   Text: '{link_text}'")
                    print(f"   ID: {link_id}")
                    print(f"   Class: {link_class}")
                    print(f"   Href: {link_href}")
                    print(f"   🎯 This looks like a plan link!")
                    
            except Exception as e:
                continue
        
        # Try to find elements with specific classes
        print(f"\n🔍 LOOKING FOR SPECIFIC ELEMENTS:")
        print("-" * 40)
        
        # Look for elements with plan-related classes
        plan_selectors = [
            "[class*='plan']",
            "[class*='monthly']",
            "[class*='access']",
            "[class*='solution']",
            "[class*='btn']",
            "[class*='button']"
        ]
        
        for selector in plan_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"\n📊 Found {len(elements)} elements with selector '{selector}':")
                    for j, element in enumerate(elements[:5]):  # Show first 5
                        element_text = element.text.strip()
                        element_class = element.get_attribute("class") or "NO_CLASS"
                        if element_text:
                            print(f"   {j+1}. Text: '{element_text}', Class: {element_class}")
            except Exception as e:
                print(f"   ❌ Error with selector '{selector}': {e}")
        
        # Take screenshot for visual inspection
        screenshot_name = f"monthly_plan_buttons_{int(time.time())}.png"
        driver.save_screenshot(screenshot_name)
        print(f"\n📸 Screenshot saved: {screenshot_name}")
        
        # Save page source for inspection
        with open(f"monthly_plan_buttons_{int(time.time())}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"📄 Page source saved for inspection")
        
    except Exception as e:
        print(f"[❌] Debug failed: {type(e).__name__} – {e}")
        # Take screenshot even if there's an error
        try:
            screenshot_name = f"monthly_plan_error_{int(time.time())}.png"
            driver.save_screenshot(screenshot_name)
            print(f"📸 Error screenshot saved: {screenshot_name}")
        except:
            pass
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_monthly_plan_buttons() 
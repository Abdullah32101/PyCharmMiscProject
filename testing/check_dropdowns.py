import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.one_time_book_purchase_methods import OneTimeBookPurchasePage
from core.constants import BOOK_URL

def check_dropdowns():
    """Check what dropdown elements exist on the book purchase page"""
    print("🔍 Checking dropdown elements on book purchase page")
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "submit_btn_checkout"))
        )
        page.click_get_free_textbook()
        print("[✅] Clicked 'Get Free Textbook'")
        
        # Step 2: Click 'Proceed to Checkout'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn_checkout"))
        )
        page.click_proceed_to_checkout()
        print("[✅] Clicked 'Proceed to Checkout'")
        
        # Step 3: Register a New User
        page.click_register_link()
        page.enter_email()
        page.enter_password()
        page.enter_university()
        page.click_signup_button()
        print("[✅] Completed user registration")
        
        # Step 4: Fill Billing Details
        page.fill_billing_details()
        print("[✅] Filled billing details")
        
        # Step 5: Select Card Payment Method
        page.click_payment_toggle()
        print("[✅] Selected card payment method")
        
        # Step 6: Wait for Card Input to Appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "cc_num"))
        )
        print("[✅] Card input form appeared")
        
        # Step 7: Enter Card Details
        page.enter_card_details()
        print("[✅] Entered card details")
        
        # Now check the dropdown elements
        print("\n🔍 ANALYZING DROPDOWN ELEMENTS:")
        print("-" * 40)
        
        # Check for all select elements
        select_elements = driver.find_elements(By.TAG_NAME, "select")
        print(f"📊 Found {len(select_elements)} select elements:")
        
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
                for j, option in enumerate(options[:5]):
                    option_value = option.get_attribute("value") or "NO_VALUE"
                    option_text = option.text or "NO_TEXT"
                    print(f"     Option {j+1}: value='{option_value}', text='{option_text}'")
                
                if len(options) > 5:
                    print(f"     ... and {len(options) - 5} more options")
                
                # Check if this looks like an expiry dropdown
                if any(keyword in element_id.lower() for keyword in ["month", "exp", "year"]):
                    print(f"   🎯 This looks like an expiry dropdown!")
                    
            except Exception as e:
                print(f"   ❌ Error analyzing select element {i+1}: {e}")
        
        # Check for any input elements that might be dropdowns
        input_elements = driver.find_elements(By.CSS_SELECTOR, "input[list], input[type='text'][class*='dropdown'], input[class*='select']")
        print(f"\n📊 Found {len(input_elements)} input elements that might be dropdowns:")
        
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
        
        # Try to manually select expiry month and year
        print("\n🔍 TRYING TO SELECT EXPIRY DROPDOWNS:")
        print("-" * 40)
        
        try:
            print("[📅] Attempting to select expiry month...")
            page.select_expiry_month("03")
            print("[✅] Month selection completed")
        except Exception as e:
            print(f"[❌] Month selection failed: {e}")
        
        try:
            print("[📅] Attempting to select expiry year...")
            page.select_expiry_year("2032")
            print("[✅] Year selection completed")
        except Exception as e:
            print(f"[❌] Year selection failed: {e}")
        
        # Take screenshot for visual inspection
        screenshot_name = f"dropdown_check_{int(time.time())}.png"
        driver.save_screenshot(screenshot_name)
        print(f"\n📸 Screenshot saved: {screenshot_name}")
        
        # Save page source for inspection
        with open(f"dropdown_check_{int(time.time())}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"📄 Page source saved for inspection")
        
    except Exception as e:
        print(f"[❌] Check failed: {type(e).__name__} – {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    check_dropdowns() 
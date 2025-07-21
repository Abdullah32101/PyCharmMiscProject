import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pages.one_time_book_purchase_methods import OneTimeBookPurchasePage

def test_book_page_load_and_click(driver):
    page = OneTimeBookPurchasePage(driver)
    is_mobile = driver.execute_script("return window.innerWidth < 768;")

    try:
        print(f"[🚀] Starting book purchase test on {'Mobile' if is_mobile else 'Desktop'}")

        # Step 1: Open the Book Page
        page.open_book_page()

        # Step 2: Click 'Get Free Textbook'
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "submit_btn_checkout"))
        )
        page.click_get_free_textbook()

        # Step 3: Click 'Proceed to Checkout'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn_checkout"))
        )
        page.click_proceed_to_checkout()

        # Step 4: Register a New User
        page.click_register_link()
        page.enter_email()
        page.enter_password()
        page.enter_university()
        page.click_signup_button()

        # Step 5: Fill Billing Details with mobile-specific handling
        if is_mobile:
            # Additional wait for mobile to ensure page is fully loaded
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
        
        page.fill_billing_details()

        # Step 6: Select Card Payment Method
        page.click_payment_toggle()

        # Step 7: Wait for Card Input to Appear with mobile-specific handling
        if is_mobile:
            # Wait longer on mobile for form to appear
            WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.ID, "cc_num"))
            )
            # Scroll to payment section
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(1)
        else:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "cc_num"))
            )

        # Step 8: Enter Card Details
        page.enter_card_details()

        # Step 9: Select Expiration Month and Year
        page.select_expiry_month("March (03)")
        page.select_expiry_year("2032")

        # Step 10: UI Stabilization Before Placing Order with mobile-specific handling
        if is_mobile:
            # More extensive stabilization for mobile
            driver.execute_script("document.activeElement.blur();")
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(1)
            # Scroll to bottom to find place order button
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        else:
            driver.execute_script("document.activeElement.blur();")
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.5)

        # Step 11: Place the Order
        page.click_place_order()

        # Step 12: Confirm Order Success with mobile-specific handling
        if is_mobile:
            # Wait longer on mobile for order processing
            confirmation_element = WebDriverWait(driver, 90).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//text()[contains(., 'Book Order #')]/ancestor::*[1]"
                ))
            )
        else:
            confirmation_element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//text()[contains(., 'Book Order #')]/ancestor::*[1]"
                ))
            )

        # Optional: Allow final UI animations to settle
        time.sleep(5)
        
        print(f"[🎉] Book purchase test completed successfully on {'Mobile' if is_mobile else 'Desktop'}")
        
    except Exception as e:
        print(f"[❌] Test failed on {'Mobile' if is_mobile else 'Desktop'}: {type(e).__name__} – {e}")
        driver.save_screenshot(f"book_purchase_error_{int(time.time())}.png")
        
        # Save page source for debugging
        with open(f"book_purchase_error_{int(time.time())}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        raise e
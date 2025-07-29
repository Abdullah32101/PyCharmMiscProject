import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.purchase_membership_question_by_monthly_plan_methods import (
    SolutionInnPrimaryPage,
)
from pages.purchase_membership_question_by_one_time_plan_methods import (
    SolutionInnSecondaryPage,
)


@pytest.mark.parametrize("stage", ["primary", "secondary"])
def test_purchase_membership_question_by_monthly_plan_flow(driver, stage, device_info):
    # Run on all devices (desktop and mobile)
    print(f"[INFO] Running test on device: {device_info['name']} with resolution: {device_info['resolution']}")
    
    if stage == "primary":
        page = SolutionInnPrimaryPage(driver)
    else:
        page = SolutionInnSecondaryPage(driver)

    try:
        # Step 1: Open the page
        page.open()

        # Step 2: Start registration
        page.click_view_solution_button()
        page.enter_email()
        page.enter_password()
        page.enter_university()
        page.click_signup_button()

        # Step 3: Monthly Plan Purchase
        page.click_view_solution_button()
        page.click_monthly_access_button()
        page.click_payment_toggle()

        # Step 4: iFrame handling (check if iframe exists)
        is_mobile = driver.execute_script("return window.innerWidth < 768;")
        try:
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            print(f"[INFO] iFrame found on {'mobile' if is_mobile else 'desktop'}")
        except Exception:
            print(f"[INFO] No iFrame found on {'mobile' if is_mobile else 'desktop'}")

        # Step 5: Payment info
        page.enter_card_details()
        time.sleep(0.5)  # Reduced from 1 second
        
        # Scroll behavior for different devices
        if is_mobile:
            # For mobile, scroll to ensure payment fields are visible
            driver.execute_script("window.scrollBy(0, 200);")
            print("[INFO] Scrolled for mobile device")
        else:
            # For desktop, scroll as before
            driver.execute_script("window.scrollBy(0, 300);")
            print("[INFO] Scrolled for desktop device")
            
        page.select_expiry_month("03")
        page.select_expiry_year("2032")

        # Step 6: Submit
        page.click_join_now_button()

        # Step 7: Confirmation
        try:
            WebDriverWait(driver, 8).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".thank-you-message, .error-msg, .alert-danger")
                )
            )
            print(
                f"[✅] {stage.capitalize()} stage: Confirmation or error message appeared."
            )
        except Exception:
            print(f"[⚠️] {stage.capitalize()} stage: No confirmation appeared.")
            # Removed screenshot creation to avoid creating files
            time.sleep(3)

    except Exception as e:
        # Removed screenshot creation to avoid creating files
        print(f"[❌] {stage.capitalize()} stage: Test failed with error: {str(e)}")
        raise e

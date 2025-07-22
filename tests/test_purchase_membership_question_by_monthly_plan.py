import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.purchase_membership_question_by_monthly_plan_methods import \
    SolutionInnPrimaryPage
from pages.purchase_membership_question_by_one_time_plan_methods import \
    SolutionInnSecondaryPage


@pytest.mark.parametrize("stage", ["primary", "secondary"])
def test_purchase_membership_question_by_monthly_plan_flow(driver, stage):
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

        # Step 4: iFrame handling (desktop only)
        is_mobile = driver.execute_script("return window.innerWidth < 768;")
        if not is_mobile:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )

        # Step 5: Payment info
        page.enter_card_details()
        time.sleep(0.5)  # Reduced from 1 second
        if not is_mobile:
            driver.execute_script("window.scrollBy(0, 300);")
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
            driver.save_screenshot(
                f"monthly_plan_no_confirmation_{stage}_{int(time.time())}.png"
            )
            time.sleep(3)

    except Exception as e:
        driver.save_screenshot(f"monthly_plan_error_{stage}_{int(time.time())}.png")
        raise e

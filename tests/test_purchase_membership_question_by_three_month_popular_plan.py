import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
def test_purchase_membership_question_by_three_month_popular_plan(driver, stage):
    if stage == "primary":
        page = SolutionInnPrimaryPage(driver)
    else:
        page = SolutionInnSecondaryPage(driver)

    try:
        # Get device information for logging
        is_mobile = driver.execute_script("return window.innerWidth < 768;")
        print(
            f"[🚀] Starting popular plan test for {stage} stage on {'Mobile' if is_mobile else 'Desktop'}"
        )

        # ✅ FIX: Open page for both
        page.open()
        print(f"[✅] Page opened successfully for {stage}")

        # -------------------- Begin Registration --------------------
        print(f"[📝] Starting registration process for {stage}")
        page.click_view_solution_button()
        page.enter_email()
        page.enter_password()
        page.enter_university()
        page.click_signup_button()
        print(f"[✅] Registration completed for {stage}")

        # -------------------- After Sign-Up --------------------
        print(f"[🔄] Starting post-registration flow for {stage}")
        page.click_view_solution_button()

        # Add explicit wait and logging for popular plan button
        print(f"[🔍] Looking for popular plan button on {stage}")
        page.click_popular_plan_button()
        print(f"[✅] Popular plan button clicked for {stage}")

        page.click_payment_toggle()
        print(f"[✅] Payment toggle clicked for {stage}")

        # -------------------- Handle iframe only for desktop --------------------
        if not is_mobile:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "iframe"))
                )
                print(f"[✅] iframe detected for {stage}")
            except Exception as e:
                print(f"[⚠️] iframe not found for {stage}, continuing...")

        # -------------------- Enter Payment Information --------------------
        print(f"[💳] Entering payment details for {stage}")
        page.enter_card_details()
        print(f"[✅] Payment details entered for {stage}")

        # -------------------- Select Expiry Month and Year --------------------
        time.sleep(0.5)  # Reduced from 1 second - Let dropdowns load fully
        if not is_mobile:
            driver.execute_script(
                "window.scrollBy(0, 300);"
            )  # Ensure dropdown is in view
        page.select_expiry_month("03")
        page.select_expiry_year("2032")
        print(f"[✅] Expiry details set for {stage}")

        # -------------------- Final Submission --------------------
        print(f"[🚀] Submitting order for {stage}")
        page.click_join_now_button()
        print(f"[✅] Join now button clicked for {stage}")

        # -------------------- Enhanced Confirmation Check --------------------
        print(f"[🔍] Checking for confirmation/error messages for {stage}")
        try:
            # Try multiple confirmation selectors
            confirmation_selectors = [
                ".thank-you-message",
                ".error-msg",
                ".alert-danger",
                ".success-message",
                ".order-confirmation",
                "[class*='success']",
                "[class*='error']",
                "[class*='alert']",
            ]

            confirmation_found = False
            for selector in confirmation_selectors:
                try:
                    element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(
                        f"[✅] ({stage}) Confirmation/error message found with selector: {selector}"
                    )
                    print(f"[📄] Message text: {element.text[:100]}...")
                    confirmation_found = True
                    break
                except Exception:
                    continue

            if not confirmation_found:
                # Check page title or URL changes
                current_url = driver.current_url
                page_title = driver.title
                print(
                    f"[ℹ️] ({stage}) No confirmation message found. Current URL: {current_url}"
                )
                print(f"[ℹ️] ({stage}) Page title: {page_title}")

                # Check if there's any text indicating success or error
                body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
                if any(
                    keyword in body_text
                    for keyword in ["success", "thank", "order", "confirmation"]
                ):
                    print(f"[✅] ({stage}) Success keywords found in page content")
                elif any(
                    keyword in body_text for keyword in ["error", "failed", "invalid"]
                ):
                    print(f"[❌] ({stage}) Error keywords found in page content")
                else:
                    print(f"[⚠️] ({stage}) No clear success/error indicators found")

        except Exception as e:
            print(
                f"[⚠️] ({stage}) Error during confirmation check: {type(e).__name__} – {e}"
            )

        # Always save screenshot for debugging
        driver.save_screenshot(f"popular_plan_final_{stage}_{int(time.time())}.png")
        print(f"[📸] Screenshot saved for {stage}")

    except Exception as e:
        print(f"[❌] Test failed for {stage}: {type(e).__name__} – {e}")
        driver.save_screenshot(f"popular_plan_error_{stage}_{int(time.time())}.png")
        # Save page source for debugging
        with open(
            f"popular_plan_error_{stage}_{int(time.time())}.html", "w", encoding="utf-8"
        ) as f:
            f.write(driver.page_source)
        raise e

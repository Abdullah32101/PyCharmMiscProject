import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.constants import (
    ADDRESS,
    CARD_HOLDER_NAME,
    CARD_NUMBER,
    CITY,
    COUNTRY,
    CVC,
    DEFAULT_PASSWORD,
    DEFAULT_UNIVERSITY,
    EMAIL_DOMAIN,
    EXPIRY_MONTH,
    EXPIRY_YEAR,
    POSTAL_CODE,
    PRIMARY_URL,
    SECONDARY_URL,
    VIEW_SOLUTION_BTN_CSS,
)


class SolutionInnPrimaryPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = PRIMARY_URL
        self.view_solution_btn_css = VIEW_SOLUTION_BTN_CSS

    def open(self):
        self.driver.get(self.url)

    def zoom_out(self, zoom_level=0.8):
        """Zoom out the page to make elements more visible"""
        try:
            self.driver.execute_script(f"document.body.style.zoom = '{zoom_level}'")
            print(f"[🔍] Zoomed out to {zoom_level * 100}%")
        except Exception as e:
            print(f"[⚠️] Zoom failed: {type(e).__name__} – {e}")

    def zoom_in(self, zoom_level=1.2):
        """Zoom in the page"""
        try:
            self.driver.execute_script(f"document.body.style.zoom = '{zoom_level}'")
            print(f"[🔍] Zoomed in to {zoom_level * 100}%")
        except Exception as e:
            print(f"[⚠️] Zoom failed: {type(e).__name__} – {e}")

    def reset_zoom(self):
        """Reset zoom to normal (100%)"""
        try:
            self.driver.execute_script("document.body.style.zoom = '1'")
            print("[🔍] Zoom reset to 100%")
        except Exception as e:
            print(f"[⚠️] Zoom reset failed: {type(e).__name__} – {e}")

    def open_custom_url(self, url):
        self.driver.get(url)

    def click_view_solution_button(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.view_solution_btn_css)
            )
        )
        button = self.driver.find_element(By.CSS_SELECTOR, self.view_solution_btn_css)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.view_solution_btn_css))
        ).click()

    def generate_fake_email(self):
        return f"testuser_{int(time.time())}@{EMAIL_DOMAIN}"

    def enter_email(self, email=None):
        email = email or self.generate_fake_email()
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "emailR"))
        )
        field.clear()
        field.send_keys(email)
        print(f"[INFO] Using email: {email}")

    def enter_password(self, password=DEFAULT_PASSWORD):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "passwordR"))
        )
        field.clear()
        field.send_keys(password)

    def enter_university(self, university=DEFAULT_UNIVERSITY):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "uni"))
        )
        field.clear()
        field.send_keys(university)

    def click_signup_button(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signup-button"))
        )
        btn.click()

    def click_six_month_plan_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking Six Month Plan button on {'Mobile' if is_mobile else 'Desktop'}")

            # Use the specific selector for Six Month Plan button
            selector = "//div[@class='new-month-day-trail-6 plans-card-header']//button[@type='button'][normalize-space()='View Solution']"
            
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )

            # Capture button text before clicking to avoid stale element issues
            button_text = button.text.strip()
            print(f"[🔍] Found Six Month Plan button: '{button_text}'")

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)

            # Try regular click first
            try:
                button.click()
                print(f"[✅] Six Month Plan button clicked successfully: '{button_text}'")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[✅] Six Month Plan button clicked with JavaScript: '{button_text}'")

        except Exception as e:
            print(f"[❌] Failed to click Six Month Plan button: {type(e).__name__} – {e}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot(f"six_month_plan_failed_{int(time.time())}.png")
                print("[📸] Screenshot saved for debugging")
            except:
                pass
            raise e

    def click_payment_toggle(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking payment toggle on {'Mobile' if is_mobile else 'Desktop'}")

            # Try multiple selectors for the payment toggle (same as working secondary)
            selectors = [
                "//input[@id='radio7']",
                "//label[@for='radio7']",
                "//input[@name='payment_method' and @value='card']",
                "//input[@type='radio' and contains(@class, 'payment')]",
                "//input[@type='radio' and contains(@class, 'card')]",
            ]

            toggle_found = False
            for i, selector in enumerate(selectors):
                try:
                    print(f"[🔍] Trying payment toggle selector {i+1}/{len(selectors)}: {selector}")
                    toggle = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )

                    # Scroll to element with better positioning
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                        toggle,
                    )
                    time.sleep(0.2)

                    # Try regular click first
                    try:
                        toggle.click()
                        print(f"[✓] Clicked payment toggle using selector: {selector}")
                        toggle_found = True
                        break
                    except Exception as click_error:
                        print(f"[⚠️] Regular click failed, trying JavaScript click: {type(click_error).__name__}")
                        # Try JavaScript click as fallback
                        self.driver.execute_script("arguments[0].click();", toggle)
                        print(f"[✓] Clicked payment toggle using JavaScript: {selector}")
                        break

                except Exception as e:
                    print(f"[⚠️] Payment toggle selector {i+1} failed: {type(e).__name__}")
                    continue

            if not toggle_found:
                print("[⚠️] Could not find payment toggle, continuing without it...")

        except Exception as e:
            print(f"[❌] Failed to click payment toggle: {type(e).__name__} – {e}")
            print("[⚠️] Continuing without payment toggle...")

    def enter_card_details(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Entering card details on {'Mobile' if is_mobile else 'Desktop'}")

            wait = WebDriverWait(self.driver, 10)

            # Fill card number
            self._fill_card_field_mobile(wait, "cc_num", CARD_NUMBER, delay_per_key=True)

            # Fill card holder name
            self._fill_field(wait, "cc_card_holder", CARD_HOLDER_NAME)

            # Fill CVC
            self._fill_field(wait, "cc-cvc", CVC)

            # Fill postal code
            self._fill_field(wait, "zipcode", POSTAL_CODE)

            print("[✅] Card details filled successfully.")

        except Exception as e:
            print(f"[❌] Error entering card details: {type(e).__name__} – {e}")

            # Enhanced JavaScript fallback for mobile
            try:
                if is_mobile:
                    # Scroll to top first
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(1)

                self._js_fallback_card_fields()
                print("[✅] Card details filled via enhanced JavaScript fallback.")

                # Verify the values were set correctly
                if is_mobile:
                    time.sleep(1)
                    fields_to_verify = [
                        ("cc_num", CARD_NUMBER),
                        ("cc_card_holder", CARD_HOLDER_NAME),
                        ("cc-cvc", CVC),
                        ("zipcode", POSTAL_CODE),
                    ]

                    for field_id, expected_value in fields_to_verify:
                        try:
                            field = self.driver.find_element(By.ID, field_id)
                            actual_value = field.get_attribute("value")
                            if actual_value != expected_value:
                                print(f"[⚠️] Card field {field_id} verification failed. Expected: {expected_value}, Got: {actual_value}")
                        except Exception as verify_error:
                            print(f"[❌] Could not verify field {field_id}: {verify_error}")

            except Exception as js_error:
                print(f"[❌] Enhanced JavaScript fallback also failed: {js_error}")
                raise e

    def _fill_card_field_mobile(self, wait, element_id, value, delay_per_key=False):
        """Special method for filling card fields on mobile devices"""
        try:
            # Wait for the field to be present
            field = wait.until(EC.presence_of_element_located((By.ID, element_id)))

            # Scroll to the field with smooth behavior
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                field,
            )
            time.sleep(1)  # Wait for scroll to complete

            # Clear the field first
            field.clear()
            time.sleep(0.3)

            # Fill the field
            if delay_per_key:
                for char in value:
                    field.send_keys(char)
                    time.sleep(0.03)
            else:
                field.send_keys(value)

            time.sleep(0.3)

            # Verify the value was entered correctly
            actual_value = field.get_attribute("value")
            if actual_value != value:
                print(f"[⚠️] Card field {element_id} verification failed. Expected: {value}, Got: {actual_value}")

                # Try JavaScript fallback
                self.driver.execute_script(
                    f"""
                    let field = document.getElementById('{element_id}');
                    if (field) {{
                        field.value = '{value}';
                        field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                """
                )
                print(f"[✅] Card field {element_id} filled via JavaScript fallback.")

                # Final verification
                time.sleep(0.3)
                final_value = field.get_attribute("value")
                if final_value != value:
                    print(f"[❌] Card field {element_id} still not correct after JavaScript fallback. Expected: {value}, Got: {final_value}")
                else:
                    print(f"[✅] Card field {element_id} filled successfully using JavaScript fallback.")
            else:
                print(f"[✅] Card field {element_id} filled successfully: {value}")

        except Exception as e:
            print(f"[❌] Error in _fill_card_field_mobile for {element_id}: {type(e).__name__} – {e}")
            raise e

    def _fill_field(self, wait, element_id, value, delay_per_key=False):
        """Generic method for filling form fields"""
        try:
            field = wait.until(EC.presence_of_element_located((By.ID, element_id)))

            # Scroll to the field
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", field
            )
            time.sleep(0.5)

            # Clear and fill the field
            field.clear()
            time.sleep(0.2)

            if delay_per_key:
                for char in value:
                    field.send_keys(char)
                    time.sleep(0.03)
            else:
                field.send_keys(value)

            time.sleep(0.2)

        except Exception as e:
            print(f"[❌] Error filling field {element_id}: {type(e).__name__} – {e}")
            raise e

    def _js_fallback_card_fields(self):
        """JavaScript fallback for filling card fields"""
        self.driver.execute_script(
            f"""
            // Fill card number
            let ccNum = document.getElementById('cc_num');
            if (ccNum) {{
                ccNum.value = '{CARD_NUMBER}';
                ccNum.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ccNum.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            // Fill card holder
            let ccHolder = document.getElementById('cc_card_holder');
            if (ccHolder) {{
                ccHolder.value = '{CARD_HOLDER_NAME}';
                ccHolder.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ccHolder.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            // Fill CVC
            let cvc = document.getElementById('cc-cvc');
            if (cvc) {{
                cvc.value = '{CVC}';
                cvc.dispatchEvent(new Event('input', {{ bubbles: true }}));
                cvc.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            // Fill zipcode
            let zipcode = document.getElementById('zipcode');
            if (zipcode) {{
                zipcode.value = '{POSTAL_CODE}';
                zipcode.dispatchEvent(new Event('input', {{ bubbles: true }}));
                zipcode.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        """
        )

    def select_expiry_month(self, month_value=EXPIRY_MONTH):
        try:
            # Try multiple possible element IDs for the month dropdown
            possible_ids = ["cc_expiry_month", "cc-exp-month", "cc_exp_month"]
            success = False

            for element_id in possible_ids:
                try:
                    self.driver.execute_script(
                        """
                        const select = document.getElementById(arguments[0]);
                        if (select) {
                            select.value = arguments[1];
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                            return true;
                        }
                        return false;
                    """,
                        element_id,
                        month_value,
                    )

                    # Verify the selection was successful
                    time.sleep(0.5)
                    element = self.driver.find_element(By.ID, element_id)
                    if element.get_attribute("value") == month_value:
                        print(f"[🌐] JS: Set expiry month to '{month_value}' using ID '{element_id}'")
                        success = True
                        break
                except Exception:
                    continue

            if not success:
                # Fallback to the original click-based approach
                dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "cc-exp-month"))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", dropdown
                )
                dropdown.click()
                time.sleep(1)
                option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//span[normalize-space()='{month_value}']")
                    )
                )
                option.click()
                print(f"[📅] Selected month: {month_value} using click method")

        except Exception as e:
            print(f"[❌] Failed selecting month: {type(e).__name__} – {e}")

    def select_expiry_year(self, year_value=EXPIRY_YEAR):
        try:
            # Try multiple possible element IDs for the year dropdown
            possible_ids = ["cc_expiry_year", "cc-exp-year", "cc_exp_year"]
            success = False

            for element_id in possible_ids:
                try:
                    self.driver.execute_script(
                        """
                        const select = document.getElementById(arguments[0]);
                        if (select) {
                            select.value = arguments[1];
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                            return true;
                        }
                        return false;
                    """,
                        element_id,
                        year_value,
                    )

                    # Verify the selection was successful
                    time.sleep(0.5)
                    element = self.driver.find_element(By.ID, element_id)
                    if element.get_attribute("value") == year_value:
                        print(f"[🌐] JS: Set expiry year to '{year_value}' using ID '{element_id}'")
                        success = True
                        break
                except Exception:
                    continue

            if not success:
                # Fallback to the original click-based approach
                dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "cc-exp-year"))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", dropdown
                )
                dropdown.click()
                time.sleep(1)
                option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//span[normalize-space()='{year_value}']")
                        )
                    )
                option.click()
                print(f"[📅] Selected year: {year_value} using click method")

        except Exception as e:
            print(f"[❌] Failed selecting year: {type(e).__name__} – {e}")

    def click_join_now_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking Join Now button on {'Mobile' if is_mobile else 'Desktop'}")

            # Try multiple possible selectors for the Join Now button
            possible_selectors = [
                (By.ID, "submit_btn_checkout"),  # Primary selector (like secondary page)
                (By.XPATH, "//button[contains(text(), 'Join Now')]"),  # Fallback XPath
                (By.XPATH, "//button[contains(text(), 'join now')]"),  # Case insensitive
                (By.XPATH, "//input[@value='Join Now']"),  # Input button
                (By.CSS_SELECTOR, "button[type='submit']"),  # Generic submit button
            ]

            button = None
            for selector_type, selector_value in possible_selectors:
                try:
                    button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    print(f"[🔍] Found Join Now button using: {selector_type} = '{selector_value}'")
                    break
                except Exception:
                    continue

            if not button:
                raise Exception("Could not find Join Now button with any selector")

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)  # Give time for scroll to complete

            # Try regular click first
            try:
                button.click()
                print("[✓] Clicked Join Now button")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript click: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print("[✓] Clicked Join Now button using JavaScript")

        except Exception as e:
            print(f"[❌] Failed to click Join Now button: {type(e).__name__} – {e}")
            raise e


class SolutionInnSecondaryPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = SECONDARY_URL
        self.view_solution_btn_css = VIEW_SOLUTION_BTN_CSS

    def open(self):
        self.driver.get(self.url)

    def open_custom_url(self, url):
        self.driver.get(url)

    def click_view_solution_button(self):
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.view_solution_btn_css)
            )
        )
        button = self.driver.find_element(By.CSS_SELECTOR, self.view_solution_btn_css)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, self.view_solution_btn_css))
        ).click()

    def generate_fake_email(self):
        return f"testuser_{int(time.time())}@{EMAIL_DOMAIN}"

    def enter_email(self, email=None):
        email = email or self.generate_fake_email()
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "emailR"))
        )
        field.clear()
        field.send_keys(email)
        print(f"[INFO] Using email: {email}")

    def enter_password(self, password=DEFAULT_PASSWORD):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "passwordR"))
        )
        field.clear()
        field.send_keys(password)

    def enter_university(self, university=DEFAULT_UNIVERSITY):
        field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "uni"))
        )
        field.clear()
        field.send_keys(university)

    def click_signup_button(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signup-button"))
        )
        btn.click()

    def click_popular_plan_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking Popular Plan button on {'Mobile' if is_mobile else 'Desktop'}")

            # Use the specific selector for Popular Plan button
            selector = "//button[contains(@class,'new-btn-blue-area activate_button')]"
            
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )

            # Capture button text before clicking to avoid stale element issues
            button_text = button.text.strip()
            print(f"[🔍] Found Popular Plan button: '{button_text}'")

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)

            # Try regular click first
            try:
                button.click()
                print(f"[✅] Popular Plan button clicked successfully: '{button_text}'")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[✅] Popular Plan button clicked with JavaScript: '{button_text}'")

        except Exception as e:
            print(f"[❌] Failed to click Popular Plan button: {type(e).__name__} – {e}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot(f"popular_plan_failed_{int(time.time())}.png")
                print("[📸] Screenshot saved for debugging")
            except:
                pass
            raise e

    def click_monthly_access_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking Monthly Access button on {'Mobile' if is_mobile else 'Desktop'}")

            # Use the specific selector for Monthly Access button
            selector = "//div[@class='new-month-day-trail-1 plans-card-header']//button[@type='button'][normalize-space()='View Solution']"
            
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )

            # Capture button text before clicking to avoid stale element issues
            button_text = button.text.strip()
            print(f"[🔍] Found Monthly Access button: '{button_text}'")

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)

            # Try regular click first
            try:
                button.click()
                print(f"[✅] Monthly Access button clicked successfully: '{button_text}'")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[✅] Monthly Access button clicked with JavaScript: '{button_text}'")

        except Exception as e:
            print(f"[❌] Failed to click Monthly Access button: {type(e).__name__} – {e}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot(f"monthly_access_failed_{int(time.time())}.png")
                print("[📸] Screenshot saved for debugging")
            except:
                pass
            raise e

    def click_six_month_plan_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking Six Month Plan button on {'Mobile' if is_mobile else 'Desktop'}")

            # Use the specific selector for Six Month Plan button
            selector = "//div[@class='new-month-day-trail-6 plans-card-header']//button[@type='button'][normalize-space()='View Solution']"
            
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )

            # Capture button text before clicking to avoid stale element issues
            button_text = button.text.strip()
            print(f"[🔍] Found Six Month Plan button: '{button_text}'")

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)

            # Try regular click first
            try:
                button.click()
                print(f"[✅] Six Month Plan button clicked successfully: '{button_text}'")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[✅] Six Month Plan button clicked with JavaScript: '{button_text}'")

        except Exception as e:
            print(f"[❌] Failed to click Six Month Plan button: {type(e).__name__} – {e}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot(f"six_month_plan_failed_{int(time.time())}.png")
                print("[📸] Screenshot saved for debugging")
            except:
                pass
            raise e

    def click_one_time_plan_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking One Time Plan button on {'Mobile' if is_mobile else 'Desktop'}")

            # Use the specific selector for One Time Plan button
            selector = "//button[normalize-space()='Buy solution']"
            
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, selector))
            )

            # Capture button text before clicking to avoid stale element issues
            button_text = button.text.strip()
            print(f"[🔍] Found One Time Plan button: '{button_text}'")

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)

            # Try regular click first
            try:
                button.click()
                print(f"[✅] One Time Plan button clicked successfully: '{button_text}'")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[✅] One Time Plan button clicked with JavaScript: '{button_text}'")

        except Exception as e:
            print(f"[❌] Failed to click One Time Plan button: {type(e).__name__} – {e}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot(f"one_time_plan_failed_{int(time.time())}.png")
                print("[📸] Screenshot saved for debugging")
            except:
                pass
            raise e

    def click_payment_toggle(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking payment toggle on {'Mobile' if is_mobile else 'Desktop'}")

            # Try multiple selectors for the payment toggle (enhanced selectors)
            selectors = [
                "//label[@for='radio7']",
                "//input[@id='radio7']",
                "//label[contains(text(), 'Credit Card')]",
                "//label[contains(text(), 'Card')]",
                "//input[@type='radio'][@name='payment_method']",
                "//input[@type='radio']",
                "//label[contains(@class, 'payment')]",
                "//div[contains(@class, 'payment')]//input[@type='radio']",
            ]

            toggle_found = False
            for i, selector in enumerate(selectors):
                try:
                    print(f"[🔍] Trying payment toggle selector {i+1}/{len(selectors)}: {selector}")
                    toggle = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )

                    # Enhanced scrolling for mobile
                    if is_mobile:
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                            toggle,
                        )
                        time.sleep(1)
                    else:
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center'});", toggle
                        )
                        time.sleep(0.5)

                    try:
                        toggle.click()
                        print(f"[✅] Clicked Payment Toggle using selector: {selector}")
                        toggle_found = True
                        break
                    except Exception as click_error:
                        print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                        self.driver.execute_script("arguments[0].click();", toggle)
                        print(f"[✅] Clicked Payment Toggle with JavaScript: {selector}")
                        toggle_found = True
                        break

                except Exception as e:
                    print(f"[⚠️] Payment toggle selector {i+1} failed: {type(e).__name__}")
                    continue

            if not toggle_found:
                print("[⚠️] Could not find payment toggle, continuing without it...")

        except Exception as e:
            print(f"[❌] Payment toggle failed: {type(e).__name__} – {e}")
            print("[⚠️] Continuing without payment toggle...")

    def enter_card_details(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Entering card details on {'Mobile' if is_mobile else 'Desktop'}")

            wait = WebDriverWait(self.driver, 10)

            # Fill card number
            self._fill_card_field_mobile(wait, "cc_num", CARD_NUMBER, delay_per_key=True)

            # Fill card holder name
            self._fill_field(wait, "cc_card_holder", CARD_HOLDER_NAME)

            # Fill CVC
            self._fill_field(wait, "cc-cvc", CVC)

            # Fill postal code
            self._fill_field(wait, "zipcode", POSTAL_CODE)

            print("[✅] Card details filled successfully.")

        except Exception as e:
            print(f"[❌] Error entering card details: {type(e).__name__} – {e}")

            # Enhanced JavaScript fallback for mobile
            try:
                if is_mobile:
                    # Scroll to top first
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(1)

                self._js_fallback_card_fields()
                print("[✅] Card details filled via enhanced JavaScript fallback.")

                # Verify the values were set correctly
                if is_mobile:
                    time.sleep(1)
                    fields_to_verify = [
                        ("cc_num", CARD_NUMBER),
                        ("cc_card_holder", CARD_HOLDER_NAME),
                        ("cc-cvc", CVC),
                        ("zipcode", POSTAL_CODE),
                    ]

                    for field_id, expected_value in fields_to_verify:
                        try:
                            field = self.driver.find_element(By.ID, field_id)
                            actual_value = field.get_attribute("value")
                            if actual_value != expected_value:
                                print(f"[⚠️] Card field {field_id} verification failed. Expected: {expected_value}, Got: {actual_value}")
                        except Exception as verify_error:
                            print(f"[❌] Could not verify field {field_id}: {verify_error}")

            except Exception as js_error:
                print(f"[❌] Enhanced JavaScript fallback also failed: {js_error}")
                raise e

    def _fill_card_field_mobile(self, wait, element_id, value, delay_per_key=False):
        """Special method for filling card fields on mobile devices"""
        try:
            # Wait for the field to be present
            field = wait.until(EC.presence_of_element_located((By.ID, element_id)))

            # Scroll to the field with smooth behavior
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                field,
            )
            time.sleep(1)  # Wait for scroll to complete

            # Clear the field first
            field.clear()
            time.sleep(0.3)

            # Fill the field
            if delay_per_key:
                for char in value:
                    field.send_keys(char)
                    time.sleep(0.03)
            else:
                field.send_keys(value)

            time.sleep(0.3)

            # Verify the value was entered correctly
            actual_value = field.get_attribute("value")
            if actual_value != value:
                print(f"[⚠️] Card field {element_id} verification failed. Expected: {value}, Got: {actual_value}")

                # Try JavaScript fallback
                self.driver.execute_script(
                    f"""
                    let field = document.getElementById('{element_id}');
                    if (field) {{
                        field.value = '{value}';
                        field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                """
                )
                print(f"[✅] Card field {element_id} filled via JavaScript fallback.")

                # Final verification
                time.sleep(0.3)
                final_value = field.get_attribute("value")
                if final_value != value:
                    print(f"[❌] Card field {element_id} still not correct after JavaScript fallback. Expected: {value}, Got: {final_value}")
                else:
                    print(f"[✅] Card field {element_id} filled successfully using JavaScript fallback.")
            else:
                print(f"[✅] Card field {element_id} filled successfully: {value}")

        except Exception as e:
            print(f"[❌] Error in _fill_card_field_mobile for {element_id}: {type(e).__name__} – {e}")
            raise e

    def _fill_field(self, wait, element_id, value, delay_per_key=False):
        """Generic method for filling form fields"""
        try:
            field = wait.until(EC.presence_of_element_located((By.ID, element_id)))

            # Scroll to the field
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", field
            )
            time.sleep(0.5)

            # Clear and fill the field
            field.clear()
            time.sleep(0.2)

            if delay_per_key:
                for char in value:
                    field.send_keys(char)
                    time.sleep(0.03)
            else:
                field.send_keys(value)

            time.sleep(0.2)

        except Exception as e:
            print(f"[❌] Error filling field {element_id}: {type(e).__name__} – {e}")
            raise e

    def _js_fallback_card_fields(self):
        """JavaScript fallback for filling card fields"""
        self.driver.execute_script(
            f"""
            // Fill card number
            let ccNum = document.getElementById('cc_num');
            if (ccNum) {{
                ccNum.value = '{CARD_NUMBER}';
                ccNum.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ccNum.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            // Fill card holder
            let ccHolder = document.getElementById('cc_card_holder');
            if (ccHolder) {{
                ccHolder.value = '{CARD_HOLDER_NAME}';
                ccHolder.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ccHolder.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            // Fill CVC
            let cvc = document.getElementById('cc-cvc');
            if (cvc) {{
                cvc.value = '{CVC}';
                cvc.dispatchEvent(new Event('input', {{ bubbles: true }}));
                cvc.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            // Fill zipcode
            let zipcode = document.getElementById('zipcode');
            if (zipcode) {{
                zipcode.value = '{POSTAL_CODE}';
                zipcode.dispatchEvent(new Event('input', {{ bubbles: true }}));
                zipcode.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        """
        )

    def select_expiry_month(self, month_value=EXPIRY_MONTH):
        try:
            # Try multiple possible element IDs for the month dropdown
            possible_ids = ["cc_expiry_month", "cc-exp-month", "cc_exp_month"]
            success = False

            for element_id in possible_ids:
                try:
                    self.driver.execute_script(
                        """
                        const select = document.getElementById(arguments[0]);
                        if (select) {
                            select.value = arguments[1];
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                            return true;
                        }
                        return false;
                    """,
                        element_id,
                        month_value,
                    )

                    # Verify the selection was successful
                    time.sleep(0.5)
                    element = self.driver.find_element(By.ID, element_id)
                    if element.get_attribute("value") == month_value:
                        print(f"[🌐] JS: Set expiry month to '{month_value}' using ID '{element_id}'")
                        success = True
                        break
                except Exception:
                    continue

            if not success:
                # Fallback to the original click-based approach
                dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "cc-exp-month"))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", dropdown
                )
                dropdown.click()
                time.sleep(1)
                option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//span[normalize-space()='{month_value}']")
                    )
                )
                option.click()
                print(f"[📅] Selected month: {month_value} using click method")

        except Exception as e:
            print(f"[❌] Failed selecting month: {type(e).__name__} – {e}")

    def select_expiry_year(self, year_value=EXPIRY_YEAR):
        try:
            # Try multiple possible element IDs for the year dropdown
            possible_ids = ["cc_expiry_year", "cc-exp-year", "cc_exp_year"]
            success = False

            for element_id in possible_ids:
                try:
                    self.driver.execute_script(
                        """
                        const select = document.getElementById(arguments[0]);
                        if (select) {
                            select.value = arguments[1];
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                            return true;
                        }
                        return false;
                    """,
                        element_id,
                        year_value,
                    )

                    # Verify the selection was successful
                    time.sleep(0.5)
                    element = self.driver.find_element(By.ID, element_id)
                    if element.get_attribute("value") == year_value:
                        print(f"[🌐] JS: Set expiry year to '{year_value}' using ID '{element_id}'")
                        success = True
                        break
                except Exception:
                    continue

            if not success:
                # Fallback to the original click-based approach
                dropdown = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "cc-exp-year"))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", dropdown
                )
                dropdown.click()
                time.sleep(1)
                option = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//span[normalize-space()='{year_value}']")
                        )
                    )
                option.click()
                print(f"[📅] Selected year: {year_value} using click method")

        except Exception as e:
            print(f"[❌] Failed selecting year: {type(e).__name__} – {e}")

    def click_join_now_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking Join Now button on {'Mobile' if is_mobile else 'Desktop'}")

            # Try multiple possible selectors for the Join Now button
            possible_selectors = [
                (By.ID, "submit_btn_checkout"),  # Primary selector (like secondary page)
                (By.XPATH, "//button[contains(text(), 'Join Now')]"),  # Fallback XPath
                (By.XPATH, "//button[contains(text(), 'join now')]"),  # Case insensitive
                (By.XPATH, "//input[@value='Join Now']"),  # Input button
                (By.CSS_SELECTOR, "button[type='submit']"),  # Generic submit button
            ]

            button = None
            for selector_type, selector_value in possible_selectors:
                try:
                    button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    print(f"[🔍] Found Join Now button using: {selector_type} = '{selector_value}'")
                    break
                except Exception:
                    continue

            if not button:
                raise Exception("Could not find Join Now button with any selector")

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)  # Give time for scroll to complete

            # Try regular click first
            try:
                button.click()
                print("[✓] Clicked Join Now button")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript click: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print("[✓] Clicked Join Now button using JavaScript")

        except Exception as e:
            print(f"[❌] Failed to click Join Now button: {type(e).__name__} – {e}")
            raise e 
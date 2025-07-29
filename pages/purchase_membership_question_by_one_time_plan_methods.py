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

    def open_custom_url(self, url):
        self.driver.get(url)

    def click_view_solution_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking View Solution button on {'Mobile' if is_mobile else 'Desktop'}")

            # Wait for the button to be present
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.view_solution_btn_css)
                )
            )
            
            # Find the button
            button = self.driver.find_element(By.CSS_SELECTOR, self.view_solution_btn_css)
            
            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)
            
            # Wait for element to be clickable
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.view_solution_btn_css))
            )
            
            # Try multiple click strategies to handle element interception
            click_success = False
            
            # Strategy 1: Regular click
            if not click_success:
                try:
                    button.click()
                    print(f"[✅] View Solution button clicked successfully")
                    click_success = True
                except Exception as click_error:
                    print(f"[⚠️] Regular click failed: {type(click_error).__name__}")
            
            # Strategy 2: JavaScript click
            if not click_success:
                try:
                    self.driver.execute_script("arguments[0].click();", button)
                    print(f"[✅] View Solution button clicked with JavaScript")
                    click_success = True
                except Exception as js_error:
                    print(f"[⚠️] JavaScript click failed: {type(js_error).__name__}")
            
            # Strategy 3: Try to close any overlapping accordion first
            if not click_success:
                try:
                    # Look for accordion elements that might be overlapping
                    accordion_selectors = [
                        "//strong[contains(@class,'accordion')]",
                        "//div[contains(@class,'accordion')]",
                        "//*[contains(@class,'step-heading')]",
                        "//*[contains(@class,'accordion')]"
                    ]
                    
                    for accordion_selector in accordion_selectors:
                        try:
                            accordion = self.driver.find_element(By.XPATH, accordion_selector)
                            if accordion.is_displayed():
                                print(f"[🔍] Found overlapping accordion, trying to close it")
                                self.driver.execute_script("arguments[0].click();", accordion)
                                time.sleep(0.5)
                                break
                        except:
                            continue
                    
                    # Try clicking the button again after closing accordion
                    button = self.driver.find_element(By.CSS_SELECTOR, self.view_solution_btn_css)
                    button.click()
                    print(f"[✅] View Solution button clicked after closing accordion")
                    click_success = True
                except Exception as accordion_error:
                    print(f"[⚠️] Accordion handling failed: {type(accordion_error).__name__}")
            
            # Strategy 4: Force click with JavaScript
            if not click_success:
                try:
                    self.driver.execute_script("""
                        let button = document.querySelector(arguments[0]);
                        if (button) {
                            button.style.zIndex = '9999';
                            button.style.position = 'relative';
                            button.click();
                        }
                    """, self.view_solution_btn_css)
                    print(f"[✅] View Solution button clicked with forced JavaScript")
                    click_success = True
                except Exception as force_error:
                    print(f"[⚠️] Force click failed: {type(force_error).__name__}")
            
            if not click_success:
                raise Exception("All click strategies failed for View Solution button")
                
        except Exception as e:
            print(f"[❌] Failed to click View Solution button: {type(e).__name__} – {e}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot(f"view_solution_failed_{int(time.time())}.png")
                print("[📸] Screenshot saved for debugging")
            except:
                pass
            raise e

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

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)

            # Try regular click first
            try:
                button.click()
                print(f"[✅] Popular Plan button clicked successfully: '{button.text.strip()}'")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[✅] Popular Plan button clicked with JavaScript: '{button.text.strip()}'")

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

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)

            # Try regular click first
            try:
                button.click()
                print(f"[✅] Monthly Access button clicked successfully: '{button.text.strip()}'")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[✅] Monthly Access button clicked with JavaScript: '{button.text.strip()}'")

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

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)

            # Try regular click first
            try:
                button.click()
                print(f"[✅] Six Month Plan button clicked successfully: '{button.text.strip()}'")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[✅] Six Month Plan button clicked with JavaScript: '{button.text.strip()}'")

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

            # Use multiple specific selectors for One Time Plan button to ensure we get the right one
            selectors = [
                "//div[contains(@class,'one-time')]//button[normalize-space()='Buy solution']",
                "//div[contains(@class,'one-time')]//button[normalize-space()='View Solution']",
                "//div[contains(@class,'one-time')]//button[@type='button']",
                "//div[contains(@class,'one-time')]//button[contains(@class,'btn')]",
                "//button[contains(@class,'one-time') and normalize-space()='Buy solution']",
                "//button[contains(@class,'one-time') and normalize-space()='View Solution']",
                # Fallback to more specific selectors
                "//div[@class='plans-card-header' and contains(.,'one-time')]//button",
                "//div[@class='plans-card-header' and contains(.,'One Time')]//button",
                "//div[@class='plans-card-header' and contains(.,'one time')]//button",
            ]

            button = None
            for i, selector in enumerate(selectors):
                try:
                    print(f"[🔍] Trying One Time Plan selector {i+1}/{len(selectors)}: {selector}")
                    button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"[✅] Found One Time Plan button with selector: {selector}")
                    break
                except Exception as e:
                    print(f"[⚠️] Selector {i+1} failed: {type(e).__name__}")
                    continue

            if not button:
                raise Exception("Could not find One Time Plan button with any selector")

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)

            # Re-find the element to avoid stale element issues
            try:
                button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                button.click()
                print(f"[✅] One Time Plan button clicked successfully")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                try:
                    button = self.driver.find_element(By.XPATH, selector)
                    self.driver.execute_script("arguments[0].click();", button)
                    print(f"[✅] One Time Plan button clicked with JavaScript")
                except Exception as js_error:
                    print(f"[⚠️] JavaScript click also failed: {type(js_error).__name__}")
                    # Final fallback: direct XPath click
                    self.driver.execute_script("""
                        let element = document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (element) {
                            element.click();
                        }
                    """, selector)
                    print(f"[✅] One Time Plan button clicked using direct XPath: {selector}")

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

            # Try multiple selectors for the payment toggle
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
                        toggle_found = True
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
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking View Solution button on {'Mobile' if is_mobile else 'Desktop'}")

            # Wait for the button to be present
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.view_solution_btn_css)
                )
            )
            
            # Find the button
            button = self.driver.find_element(By.CSS_SELECTOR, self.view_solution_btn_css)
            
            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)
            
            # Wait for element to be clickable
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, self.view_solution_btn_css))
            )
            
            # Try multiple click strategies to handle element interception
            click_success = False
            
            # Strategy 1: Regular click
            if not click_success:
                try:
                    button.click()
                    print(f"[✅] View Solution button clicked successfully")
                    click_success = True
                except Exception as click_error:
                    print(f"[⚠️] Regular click failed: {type(click_error).__name__}")
            
            # Strategy 2: JavaScript click
            if not click_success:
                try:
                    self.driver.execute_script("arguments[0].click();", button)
                    print(f"[✅] View Solution button clicked with JavaScript")
                    click_success = True
                except Exception as js_error:
                    print(f"[⚠️] JavaScript click failed: {type(js_error).__name__}")
            
            # Strategy 3: Try to close any overlapping accordion first
            if not click_success:
                try:
                    # Look for accordion elements that might be overlapping
                    accordion_selectors = [
                        "//strong[contains(@class,'accordion')]",
                        "//div[contains(@class,'accordion')]",
                        "//*[contains(@class,'step-heading')]",
                        "//*[contains(@class,'accordion')]"
                    ]
                    
                    for accordion_selector in accordion_selectors:
                        try:
                            accordion = self.driver.find_element(By.XPATH, accordion_selector)
                            if accordion.is_displayed():
                                print(f"[🔍] Found overlapping accordion, trying to close it")
                                self.driver.execute_script("arguments[0].click();", accordion)
                                time.sleep(0.5)
                                break
                        except:
                            continue
                    
                    # Try clicking the button again after closing accordion
                    button = self.driver.find_element(By.CSS_SELECTOR, self.view_solution_btn_css)
                    button.click()
                    print(f"[✅] View Solution button clicked after closing accordion")
                    click_success = True
                except Exception as accordion_error:
                    print(f"[⚠️] Accordion handling failed: {type(accordion_error).__name__}")
            
            # Strategy 4: Force click with JavaScript
            if not click_success:
                try:
                    self.driver.execute_script("""
                        let button = document.querySelector(arguments[0]);
                        if (button) {
                            button.style.zIndex = '9999';
                            button.style.position = 'relative';
                            button.click();
                        }
                    """, self.view_solution_btn_css)
                    print(f"[✅] View Solution button clicked with forced JavaScript")
                    click_success = True
                except Exception as force_error:
                    print(f"[⚠️] Force click failed: {type(force_error).__name__}")
            
            if not click_success:
                raise Exception("All click strategies failed for View Solution button")
                
        except Exception as e:
            print(f"[❌] Failed to click View Solution button: {type(e).__name__} – {e}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot(f"view_solution_failed_{int(time.time())}.png")
                print("[📸] Screenshot saved for debugging")
            except:
                pass
            raise e

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
            print("[🔍] Attempting to locate Popular Plan button...")

            # Try multiple selectors for the popular plan button
            selectors = [
                "//button[contains(@class,'new-btn-blue-area activate_button')]",
                "//button[contains(text(), 'Popular')]",
                "//button[contains(text(), 'popular')]",
                "//button[contains(@class, 'popular')]",
                "//a[contains(text(), 'Popular')]",
                "//a[contains(@class, 'popular')]",
            ]

            button_found = False
            for i, selector in enumerate(selectors):
                try:
                    print(f"[🔍] Trying selector {i+1}/{len(selectors)}: {selector}")
                    button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )

                    # Scroll to element with better positioning
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                        button,
                    )
                    time.sleep(1)  # Wait for scroll to complete

                    # Try regular click first
                    try:
                        button.click()
                        print(
                            f"[✓] Clicked Popular Plan button using selector: {selector}"
                        )
                        button_found = True
                        break
                    except Exception as click_error:
                        print(
                            f"[⚠️] Regular click failed, trying JavaScript click: {type(click_error).__name__}"
                        )
                        # Try JavaScript click as fallback
                        self.driver.execute_script("arguments[0].click();", button)
                        print(
                            f"[✓] Clicked Popular Plan button using JavaScript: {selector}"
                        )
                        button_found = True
                        break

                except Exception as e:
                    print(f"[⚠️] Selector {i+1} failed: {type(e).__name__}")
                    continue

            if not button_found:
                # Fallback: try to find any button that might be the popular plan
                print(
                    "[🔄] Trying fallback method - searching for any relevant buttons..."
                )
                try:
                    # Get all buttons and links on the page
                    all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    all_links = self.driver.find_elements(By.TAG_NAME, "a")

                    # Look for buttons/links with relevant text
                    relevant_elements = []
                    for element in all_buttons + all_links:
                        try:
                            text = element.text.lower()
                            if any(
                                keyword in text
                                for keyword in [
                                    "popular",
                                    "activate",
                                    "view solution",
                                    "buy",
                                ]
                            ):
                                relevant_elements.append(element)
                        except:
                            continue

                    if relevant_elements:
                        print(
                            f"[🔍] Found {len(relevant_elements)} potentially relevant elements"
                        )
                        for i, element in enumerate(
                            relevant_elements[:5]
                        ):  # Try first 5
                            try:
                                print(
                                    f"[🔍] Trying fallback element {i+1}: {element.text[:50]}..."
                                )
                                self.driver.execute_script(
                                    "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                                    element,
                                )
                                time.sleep(1)

                                try:
                                    element.click()
                                    print(
                                        f"[✓] Clicked fallback element: {element.text[:50]}..."
                                    )
                                    button_found = True
                                    break
                                except Exception as click_error:
                                    print(
                                        f"[⚠️] Regular click failed, trying JavaScript click: {type(click_error).__name__}"
                                    )
                                    self.driver.execute_script(
                                        "arguments[0].click();", element
                                    )
                                    print(
                                        f"[✓] Clicked fallback element with JavaScript: {element.text[:50]}..."
                                    )
                                    button_found = True
                                    break

                            except Exception as e:
                                print(
                                    f"[⚠️] Fallback element {i+1} failed: {type(e).__name__}"
                                )
                                continue
                    else:
                        print("[❌] No relevant buttons/links found")

                except Exception as fallback_error:
                    print(
                        f"[❌] Fallback method failed: {type(fallback_error).__name__} – {fallback_error}"
                    )

                if not button_found:
                    # Save screenshot and page source for debugging
                    timestamp = int(time.time())
                    self.driver.save_screenshot(
                        f"popular_plan_button_not_found_{timestamp}.png"
                    )
                    with open(
                        f"popular_plan_page_source_{timestamp}.html",
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(self.driver.page_source)
                    print(
                        f"[📸] Debug files saved: popular_plan_button_not_found_{timestamp}.png"
                    )
                    print(
                        f"[📄] Debug files saved: popular_plan_page_source_{timestamp}.html"
                    )
                    raise Exception("No popular plan button found after all attempts")

        except Exception as e:
            print(f"[❌] Failed to click Popular Plan button: {type(e).__name__} – {e}")
            raise e

    def click_monthly_access_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(
                f"[📱] Clicking Monthly Access button on {'Mobile' if is_mobile else 'Desktop'}"
            )

            button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@class='new-month-day-trail-1 plans-card-header']//button[@type='button'][normalize-space()='View Solution']",
                    )
                )
            )

            # Enhanced scrolling for mobile
            if is_mobile:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                    button,
                )
                time.sleep(1)
            else:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", button
                )
                time.sleep(0.5)

            try:
                button.click()
                print("[✅] Monthly Access button clicked successfully")
            except Exception as click_error:
                print(
                    f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}"
                )
                self.driver.execute_script("arguments[0].click();", button)
                print("[✅] Monthly Access button clicked with JavaScript")

        except Exception as e:
            print(
                f"[❌] Failed to click Monthly Access button: {type(e).__name__} – {e}"
            )
            raise e

    def click_six_month_plan_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(
                f"[📱] Clicking Six-Month Plan button on {'Mobile' if is_mobile else 'Desktop'}"
            )

            button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@class='new-month-day-trail-6 plans-card-header']//button[@type='button'][normalize-space()='View Solution']",
                    )
                )
            )

            # Enhanced scrolling for mobile
            if is_mobile:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                    button,
                )
                time.sleep(1)
            else:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", button
                )
                time.sleep(0.5)

            try:
                button.click()
                print("[✅] Six-Month Plan button clicked successfully")
            except Exception as click_error:
                print(
                    f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}"
                )
                self.driver.execute_script("arguments[0].click();", button)
                print("[✅] Six-Month Plan button clicked with JavaScript")

        except Exception as e:
            print(
                f"[❌] Failed to click Six-Month Plan button: {type(e).__name__} – {e}"
            )
            raise e

    def click_one_time_plan_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[📱] Clicking One Time Plan button on {'Mobile' if is_mobile else 'Desktop'}")

            # Use multiple specific selectors for One Time Plan button to ensure we get the right one
            selectors = [
                "//div[contains(@class,'one-time')]//button[normalize-space()='Buy solution']",
                "//div[contains(@class,'one-time')]//button[normalize-space()='View Solution']",
                "//div[contains(@class,'one-time')]//button[@type='button']",
                "//div[contains(@class,'one-time')]//button[contains(@class,'btn')]",
                "//button[contains(@class,'one-time') and normalize-space()='Buy solution']",
                "//button[contains(@class,'one-time') and normalize-space()='View Solution']",
                # Fallback to more specific selectors
                "//div[@class='plans-card-header' and contains(.,'one-time')]//button",
                "//div[@class='plans-card-header' and contains(.,'One Time')]//button",
                "//div[@class='plans-card-header' and contains(.,'one time')]//button",
            ]

            button = None
            for i, selector in enumerate(selectors):
                try:
                    print(f"[🔍] Trying One Time Plan selector {i+1}/{len(selectors)}: {selector}")
                    button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"[✅] Found One Time Plan button with selector: {selector}")
                    break
                except Exception as e:
                    print(f"[⚠️] Selector {i+1} failed: {type(e).__name__}")
                    continue

            if not button:
                raise Exception("Could not find One Time Plan button with any selector")

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.5)

            # Re-find the element to avoid stale element issues
            try:
                button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                button.click()
                print(f"[✅] One Time Plan button clicked successfully")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                try:
                    button = self.driver.find_element(By.XPATH, selector)
                    self.driver.execute_script("arguments[0].click();", button)
                    print(f"[✅] One Time Plan button clicked with JavaScript")
                except Exception as js_error:
                    print(f"[⚠️] JavaScript click also failed: {type(js_error).__name__}")
                    # Final fallback: direct XPath click
                    self.driver.execute_script("""
                        let element = document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (element) {
                            element.click();
                        }
                    """, selector)
                    print(f"[✅] One Time Plan button clicked using direct XPath: {selector}")

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
            print(
                f"[📱] Looking for Payment Toggle on {'Mobile' if is_mobile else 'Desktop'}"
            )

            # Try multiple selectors for payment toggle
            toggle_selectors = [
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
            for i, selector in enumerate(toggle_selectors):
                try:
                    print(
                        f"[🔍] Trying payment toggle selector {i+1}/{len(toggle_selectors)}: {selector}"
                    )
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
                        print(
                            f"[⚠️] Regular click failed, trying JavaScript: {type(click_error).__name__}"
                        )
                        self.driver.execute_script("arguments[0].click();", toggle)
                        print(
                            f"[✅] Clicked Payment Toggle with JavaScript: {selector}"
                        )
                        toggle_found = True
                        break

                except Exception as e:
                    print(
                        f"[⚠️] Payment toggle selector {i+1} failed: {type(e).__name__}"
                    )
                    continue

            if not toggle_found:
                print("[⚠️] Could not find payment toggle, continuing without it...")

        except Exception as e:
            print(f"[❌] Payment toggle failed: {type(e).__name__} – {e}")
            print("[⚠️] Continuing without payment toggle...")

    def enter_card_details(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(
                f"[💳] Entering card details on {'Mobile' if is_mobile else 'Desktop'}"
            )

            wait = WebDriverWait(self.driver, 15)

            # Enhanced mobile handling for card details
            if is_mobile:
                self._fill_card_field_mobile(
                    wait, "cc_num", CARD_NUMBER, delay_per_key=True
                )
                self.driver.execute_script("window.scrollBy(0, 200);")
                time.sleep(0.5)

                self._fill_card_field_mobile(wait, "cc_card_holder", CARD_HOLDER_NAME)
                self.driver.execute_script("window.scrollBy(0, 200);")
                time.sleep(0.5)

                self._fill_card_field_mobile(wait, "cc-cvc", CVC)
                self.driver.execute_script("window.scrollBy(0, 200);")
                time.sleep(0.5)

                self._fill_card_field_mobile(wait, "zipcode", POSTAL_CODE)
            else:
                self._fill_field(wait, "cc_num", CARD_NUMBER, delay_per_key=True)
                self._fill_field(wait, "cc_card_holder", CARD_HOLDER_NAME)
                self._fill_field(wait, "cc-cvc", CVC)
                self._fill_field(wait, "zipcode", POSTAL_CODE)

            print("[✅] Card details entered successfully.")

        except Exception as e:
            print(f"[❌] Error entering card details: {type(e).__name__} – {e}")
            self._js_fallback_card_fields()

    def _fill_card_field_mobile(self, wait, element_id, value, delay_per_key=False):
        """Enhanced field filling for mobile devices"""
        try:
            field = wait.until(EC.visibility_of_element_located((By.ID, element_id)))

            # Scroll to field with smooth behavior
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                field,
            )
            time.sleep(0.5)

            # Clear the field
            field.clear()
            time.sleep(0.3)

            # Fill the field
            if delay_per_key:
                for char in value:
                    field.send_keys(char)
                    time.sleep(0.03)
            else:
                field.send_keys(value)

            # Verify the value was entered correctly
            time.sleep(0.3)
            actual_value = field.get_attribute("value")
            if actual_value != value:
                print(
                    f"[⚠️] Value mismatch for {element_id}. Expected: {value}, Got: {actual_value}"
                )
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
                time.sleep(0.3)

                # Final verification
                final_value = field.get_attribute("value")
                if final_value != value:
                    print(
                        f"[❌] Failed to fill {element_id} correctly even with JavaScript"
                    )
                else:
                    print(
                        f"[✅] Successfully filled {element_id} with JavaScript fallback"
                    )
            else:
                print(f"[✅] Successfully filled {element_id}")

        except Exception as e:
            print(f"[❌] Error filling {element_id}: {type(e).__name__} – {e}")
            # Try JavaScript fallback
            try:
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
                print(f"[✅] Filled {element_id} via JavaScript fallback")
            except Exception as js_error:
                print(
                    f"[❌] JavaScript fallback also failed for {element_id}: {js_error}"
                )
                raise e

    def _fill_field(self, wait, element_id, value, delay_per_key=False):
        field = wait.until(EC.visibility_of_element_located((By.ID, element_id)))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", field
        )
        field.clear()
        if delay_per_key:
            for char in value:
                field.send_keys(char)
                time.sleep(0.03)
        else:
            field.send_keys(value)

    def _js_fallback_card_fields(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(
                f"[🔄] Using JavaScript fallback for card fields on {'Mobile' if is_mobile else 'Desktop'}"
            )

            # Enhanced JavaScript fallback with proper event dispatching
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
                            print(
                                f"[⚠️] Card field {field_id} verification failed. Expected: {expected_value}, Got: {actual_value}"
                            )
                    except Exception as verify_error:
                        print(f"[❌] Could not verify field {field_id}: {verify_error}")

            print("[✅] JavaScript fallback entered card details successfully.")

        except Exception as e:
            print(f"[❌] JavaScript fallback failed: {type(e).__name__} – {e}")
            raise e

    def select_expiry_month(self, month_value=EXPIRY_MONTH):
        try:
            self.driver.execute_script(
                """
                const select = document.getElementById('cc_expiry_month');
                if (select) {
                    select.value = arguments[0];
                    select.dispatchEvent(new Event('change', { bubbles: true }));
                }
            """,
                month_value,
            )
            print(f"[🌐] JS: Set expiry month to '{month_value}'")
        except Exception as e:
            print(f"[❌] Month selection failed: {type(e).__name__} – {e}")

    def select_expiry_year(self, year_value=EXPIRY_YEAR):
        try:
            self.driver.execute_script(
                """
                const select = document.getElementById('cc_expiry_year');
                if (select) {
                    select.value = arguments[0];
                    select.dispatchEvent(new Event('change', { bubbles: true }));
                }
            """,
                year_value,
            )
            print(f"[🌐] JS: Set expiry year to '{year_value}'")
        except Exception as e:
            print(f"[❌] Year selection failed: {type(e).__name__} – {e}")

    def click_join_now_button(self):
        try:
            btn = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "submit_btn_checkout"))
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", btn
            )
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.ID, "submit_btn_checkout"))
            ).click()
            print("[✓] Clicked the 'Join Now' button.")
        except Exception as e:
            print(f"[!] Click failed: {type(e).__name__} – {e}")
            try:
                self.driver.execute_script("arguments[0].click();", btn)
                print("[✓] JavaScript click succeeded.")
            except Exception as js_e:
                print(f"[✗] JS click failed: {type(js_e).__name__} – {js_e}")

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from constants import (CARD_HOLDER_NAME, CARD_NUMBER, CVC, DEFAULT_PASSWORD,
                       DEFAULT_UNIVERSITY, EMAIL_DOMAIN, EXPIRY_MONTH,
                       EXPIRY_YEAR, POSTAL_CODE, SECONDARY_URL,
                       VIEW_SOLUTION_BTN_CSS)


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
            print(
                f"[📱] Looking for One-Time Plan button on {'Mobile' if is_mobile else 'Desktop'}"
            )

            # Try multiple selectors for the one-time plan button
            selectors = [
                "//button[normalize-space()='Buy solution']",
                "//button[contains(text(), 'Buy solution')]",
                "//button[contains(text(), 'Buy Solution')]",
                "//button[contains(@class, 'buy-solution')]",
                "//a[contains(text(), 'Buy solution')]",
                "//a[contains(text(), 'Buy Solution')]",
                "//button[contains(text(), 'One-time')]",
                "//button[contains(text(), 'One time')]",
                "//button[contains(text(), 'Single')]",
                "//button[contains(text(), 'Purchase')]",
                "//a[contains(text(), 'One-time')]",
                "//a[contains(text(), 'One time')]",
                "//a[contains(text(), 'Single')]",
                "//a[contains(text(), 'Purchase')]",
            ]

            button_found = False
            for i, selector in enumerate(selectors):
                try:
                    print(f"[🔍] Trying selector {i+1}/{len(selectors)}: {selector}")
                    button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
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
                            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                            button,
                        )
                        time.sleep(0.5)

                    # Try regular click first
                    try:
                        button.click()
                        print(
                            f"[✅] Clicked One-Time Plan button using selector: {selector}"
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
                            f"[✅] Clicked One-Time Plan button using JavaScript: {selector}"
                        )
                        button_found = True
                        break

                except Exception as e:
                    print(f"[⚠️] Selector {i+1} failed: {type(e).__name__}")
                    continue

            if not button_found:
                # Fallback: try to find any button that might be the one-time plan
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
                                    "buy",
                                    "solution",
                                    "one",
                                    "single",
                                    "purchase",
                                    "order",
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

                                # Enhanced scrolling for mobile
                                if is_mobile:
                                    self.driver.execute_script(
                                        "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                                        element,
                                    )
                                    time.sleep(1)
                                else:
                                    self.driver.execute_script(
                                        "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                                        element,
                                    )
                                    time.sleep(0.5)

                                try:
                                    element.click()
                                    print(
                                        f"[✅] Clicked fallback element: {element.text[:50]}..."
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
                                        f"[✅] Clicked fallback element with JavaScript: {element.text[:50]}..."
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
                        f"one_time_plan_button_not_found_{timestamp}.png"
                    )
                    with open(
                        f"one_time_plan_page_source_{timestamp}.html",
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(self.driver.page_source)
                    print(
                        f"[📸] Debug files saved: one_time_plan_button_not_found_{timestamp}.png"
                    )
                    print(
                        f"[📄] Debug files saved: one_time_plan_page_source_{timestamp}.html"
                    )
                    raise Exception("No one-time plan button found after all attempts")

        except Exception as e:
            print(
                f"[❌] Failed to click One-Time Plan button: {type(e).__name__} – {e}"
            )
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

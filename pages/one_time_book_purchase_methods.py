import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Constants for configuration
from constants import (ADDRESS, BOOK_URL, CARD_HOLDER_NAME, CARD_NUMBER, CITY,
                       COUNTRY, CVC, DEFAULT_FIRST_NAME, DEFAULT_LAST_NAME,
                       DEFAULT_PASSWORD, DEFAULT_UNIVERSITY,
                       EXPIRY_MONTH_LABEL, EXPIRY_YEAR_LABEL, PHONE_NUMBER,
                       POSTAL_CODE, STATE)


class OneTimeBookPurchasePage:
    def __init__(self, driver):
        self.driver = driver
        self.book_url = BOOK_URL

    # ----------------------
    # Navigation & Core Flow
    # ----------------------
    def open_book_page(self):
        self.driver.get(self.book_url)

    def click_get_free_textbook(self):
        self._click_and_log(
            By.ID, "submit_btn_checkout", "Get Your Free Textbook", "📱🖥️"
        )

    def click_proceed_to_checkout(self):
        self._click_and_log(By.ID, "btn_checkout", "Proceed to Checkout", "📦")

    def click_register_link(self):
        self._click_and_log(By.ID, "signup", "Register", "📝")

    def _click_and_log(self, by, locator, name, emoji):
        is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((by, locator))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        time.sleep(0.5)
        button.click()
        print(f"[{emoji}] Clicked '{name}' on {'Mobile' if is_mobile else 'Desktop'}.")

    # ----------------------
    # Registration
    # ----------------------
    def generate_fake_email(self):
        return f"testuser_{int(time.time())}@example.com"

    def enter_email(self, email=None):
        email = email or self.generate_fake_email()
        self._fill_input("emailR", email, "[📧] Using email: {}")

    def enter_password(self, password=DEFAULT_PASSWORD):
        self._fill_input("passwordR", password)

    def enter_university(self, university=DEFAULT_UNIVERSITY):
        self._fill_input("uni", university)

    def click_signup_button(self):
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signup-button"))
        )
        btn.click()
        print("[✅] Clicked Sign Up button.")

    # ----------------------
    # Billing Details
    # ----------------------
    def fill_billing_details(self):
        wait = WebDriverWait(self.driver, 10)
        is_mobile = self.driver.execute_script("return window.innerWidth < 768;")

        print(f"[📱] Filling billing details on {'Mobile' if is_mobile else 'Desktop'}")

        # Fill basic text fields first
        self._fill_input("fname", DEFAULT_FIRST_NAME)
        self._fill_input("lname", DEFAULT_LAST_NAME)

        # Handle Country selection
        try:
            if is_mobile:
                # For mobile, use a more robust approach
                country_select = wait.until(
                    EC.presence_of_element_located((By.ID, "country_name_p"))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", country_select
                )
                time.sleep(0.5)

                # Try to find Pakistan by value first, then by text
                try:
                    Select(country_select).select_by_value("177")  # Pakistan's value
                    print("[🌍] Country selected by value (Mobile).")
                except:
                    try:
                        Select(country_select).select_by_visible_text(COUNTRY)
                        print("[🌍] Country selected by text (Mobile).")
                    except:
                        # Fallback to JavaScript
                        self.driver.execute_script(
                            f"""
                            let select = document.getElementById('country_name_p');
                            if (select) {{ 
                                select.value = '177'; 
                                select.dispatchEvent(new Event('change', {{ bubbles: true }})); 
                            }}
                        """
                        )
                        print("[🌍] Country selected via JavaScript (Mobile).")

                # Wait for state dropdown to populate
                time.sleep(2)
            else:
                country = wait.until(
                    EC.element_to_be_clickable((By.ID, "country_name_p"))
                )
                Select(country).select_by_visible_text(COUNTRY)
                print("[🌍] Country selected (Desktop).")
                # Wait for province to load only on desktop
                wait.until(
                    lambda d: any(
                        STATE in opt.text
                        for opt in Select(d.find_element(By.ID, "state")).options
                    )
                )
                print("[🏙️] State option is now available.")

        except Exception as e:
            print(f"[❌] Error selecting country: {type(e).__name__} – {e}")
            # Try JavaScript fallback
            self.driver.execute_script(
                f"""
                let select = document.getElementById('country_name_p');
                if (select) {{ 
                    select.value = '177'; 
                    select.dispatchEvent(new Event('change', {{ bubbles: true }})); 
                }}
            """
            )
            print("[🌍] Country selected via JavaScript fallback.")
            time.sleep(2)

        # Handle State selection
        try:
            if is_mobile:
                state_select = wait.until(
                    EC.presence_of_element_located((By.ID, "state"))
                )
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", state_select
                )
                time.sleep(0.5)

                # Try to find Punjab by text first
                try:
                    Select(state_select).select_by_visible_text(STATE)
                    print("[🏙️] State selected by text (Mobile).")
                except:
                    # Fallback to JavaScript
                    self.driver.execute_script(
                        f"""
                        let select = document.getElementById('state');
                        if (select) {{ 
                            for (let option of select.options) {{
                                if (option.text.includes('{STATE}')) {{
                                    select.value = option.value;
                                    select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    break;
                                }}
                            }}
                        }}
                    """
                    )
                    print("[🏙️] State selected via JavaScript (Mobile).")

                time.sleep(1)
            else:
                state = wait.until(EC.element_to_be_clickable((By.ID, "state")))
                Select(state).select_by_visible_text(STATE)
                print("[🏙️] State selected (Desktop).")

        except Exception as e:
            print(f"[❌] Error selecting state: {type(e).__name__} – {e}")
            # Try JavaScript fallback
            self.driver.execute_script(
                f"""
                let select = document.getElementById('state');
                if (select) {{ 
                    for (let option of select.options) {{
                        if (option.text.includes('{STATE}')) {{
                            select.value = option.value;
                            select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            break;
                        }}
                    }}
                }}
            """
            )
            print("[🏙️] State selected via JavaScript fallback.")

        # Fill remaining fields
        self._fill_input("city", CITY)
        self._fill_input("post_code", POSTAL_CODE)
        self._fill_input("address", ADDRESS)
        self._fill_input("phone_number", PHONE_NUMBER)

        # Additional mobile-specific handling
        if is_mobile:
            # Ensure all fields are properly filled by scrolling and checking
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)

            # Verify all fields have values
            fields_to_check = [
                "fname",
                "lname",
                "city",
                "post_code",
                "address",
                "phone_number",
            ]
            for field_id in fields_to_check:
                try:
                    field = self.driver.find_element(By.ID, field_id)
                    if not field.get_attribute("value"):
                        print(f"[⚠️] Field {field_id} is empty, refilling...")
                        if field_id == "fname":
                            field.send_keys(DEFAULT_FIRST_NAME)
                        elif field_id == "lname":
                            field.send_keys(DEFAULT_LAST_NAME)
                        elif field_id == "city":
                            field.send_keys(CITY)
                        elif field_id == "post_code":
                            field.send_keys(POSTAL_CODE)
                        elif field_id == "address":
                            field.send_keys(ADDRESS)
                        elif field_id == "phone_number":
                            field.send_keys(PHONE_NUMBER)
                except Exception as e:
                    print(f"[⚠️] Could not verify/fill field {field_id}: {e}")

        print("[✅] Billing details filled successfully.")

    # ----------------------
    # Payment Toggle
    # ----------------------
    def click_payment_toggle(self):
        try:
            # Try to find and click the payment toggle
            toggle = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "radio7"))
            )
            toggle.click()
            print("[💳] Payment toggle clicked.")
        except Exception as e:
            print(
                f"[⚠️] Could not find payment toggle, continuing without it... Error: {e}"
            )

    # ----------------------
    # Card Details
    # ----------------------
    def enter_card_details(self):
        wait = WebDriverWait(self.driver, 10)
        is_mobile = self.driver.execute_script("return window.innerWidth < 768;")

        print(f"[💳] Entering card details on {'Mobile' if is_mobile else 'Desktop'}")

        try:
            # Fill card number
            (
                self._fill_card_number_mobile()
                if is_mobile
                else self._fill_input("cc_num", CARD_NUMBER)
            )

            # Fill card holder name
            self._fill_input("cc_card_holder", CARD_HOLDER_NAME)

            # Fill CVC
            self._fill_input("cc-cvc", CVC)

            # Fill postal code
            self._fill_input("zipcode", POSTAL_CODE)

            print("[✅] Card details filled successfully.")

        except Exception as e:
            print(f"[❌] Error entering card details: {type(e).__name__} – {e}")

            # Enhanced JavaScript fallback for mobile
            if is_mobile:
                try:
                    print("[🔄] Trying enhanced JavaScript fallback for mobile...")
                    self.driver.execute_script(
                        f"""
                        // Fill card number
                        let cc_num = document.getElementById('cc_num');
                        if (cc_num) {{
                            cc_num.value = '{CARD_NUMBER}';
                            cc_num.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            cc_num.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                        
                        // Fill card holder
                        let cc_card_holder = document.getElementById('cc_card_holder');
                        if (cc_card_holder) {{
                            cc_card_holder.value = '{CARD_HOLDER_NAME}';
                            cc_card_holder.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            cc_card_holder.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                        
                        // Fill CVC
                        let cvc = document.getElementById('cc-cvc');
                        if (cvc) {{
                            cvc.value = '{CVC}';
                            cvc.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            cvc.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                        
                        // Fill postal code
                        let zipcode = document.getElementById('zipcode');
                        if (zipcode) {{
                            zipcode.value = '{POSTAL_CODE}';
                            zipcode.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            zipcode.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    """
                    )
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
                                    print(
                                        f"[⚠️] Card field {field_id} verification failed. Expected: {expected_value}, Got: {actual_value}"
                                    )
                            except Exception as verify_error:
                                print(
                                    f"[❌] Could not verify field {field_id}: {verify_error}"
                                )

                except Exception as js_error:
                    print(f"[❌] Enhanced JavaScript fallback also failed: {js_error}")
                    raise e

        # Take screenshot for debugging
        self.driver.save_screenshot("card_details_filled.png")

    def _fill_card_number_mobile(self):
        """Enhanced card number filling for mobile devices"""
        try:
            # Wait for the field to be present
            card_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "cc_num"))
            )

            # Scroll to the field with smooth behavior
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                card_field,
            )
            time.sleep(1)  # Wait for scroll to complete

            # Clear the field first
            card_field.clear()
            time.sleep(0.3)

            # Fill the field
            card_field.send_keys(CARD_NUMBER)
            time.sleep(0.3)

            # Verify the value was entered correctly
            actual_value = card_field.get_attribute("value")
            if actual_value != CARD_NUMBER:
                print(
                    f"[⚠️] Card number verification failed. Expected: {CARD_NUMBER}, Got: {actual_value}"
                )

                # Try JavaScript fallback
                self.driver.execute_script(
                    f"""
                    let field = document.getElementById('cc_num');
                    if (field) {{
                        field.value = '{CARD_NUMBER}';
                        field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                """
                )
                print("[✅] Card number filled via JavaScript fallback.")
            else:
                print("[✅] Card number filled successfully.")

        except Exception as e:
            print(f"[❌] Error filling card number: {type(e).__name__} – {e}")
            # Try JavaScript fallback
            self.driver.execute_script(
                f"""
                let field = document.getElementById('cc_num');
                if (field) {{
                    field.value = '{CARD_NUMBER}';
                    field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            """
            )
            print("[✅] Card number filled via JavaScript fallback.")

    # ----------------------
    # Expiry Selection
    # ----------------------
    def select_expiry_month(self, month_label=EXPIRY_MONTH_LABEL):
        self._select_dropdown(
            "cc-exp-month",
            month_label,
            "[📅] Expiry month selected.",
            "[❌] Failed to select expiry month.",
        )

    def select_expiry_year(self, year_label=EXPIRY_YEAR_LABEL):
        self._select_dropdown(
            "cc-exp-year",
            year_label,
            "[📅] Expiry year selected.",
            "[❌] Failed to select expiry year.",
        )

    def _select_dropdown(self, dropdown_id, option_text, success_log, failure_log):
        try:
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, dropdown_id))
            )
            Select(dropdown).select_by_visible_text(option_text)
            print(success_log)
        except Exception as e:
            print(f"{failure_log} Error: {type(e).__name__} – {e}")

    # ----------------------
    # Input Helper
    # ----------------------
    def _fill_input(self, field_id, value, log_template=None, delay_per_key=False):
        try:
            field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, field_id))
            )

            # Scroll to field with smooth behavior for mobile
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            if is_mobile:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                    field,
                )
                time.sleep(1)  # Wait for scroll to complete
            else:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", field
                )
                time.sleep(0.5)

            # Clear and fill the field
            field.clear()
            time.sleep(0.3)

            if delay_per_key:
                for char in value:
                    field.send_keys(char)
                    time.sleep(0.1)
            else:
                field.send_keys(value)

            time.sleep(0.3)

            # Verify the value was entered correctly
            actual_value = field.get_attribute("value")
            if actual_value != value:
                print(
                    f"[⚠️] Field {field_id} verification failed. Expected: {value}, Got: {actual_value}"
                )

                # Try JavaScript fallback
                self.driver.execute_script(
                    f"""
                    let field = document.getElementById('{field_id}');
                    if (field) {{
                        field.value = '{value}';
                        field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        field.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                    }}
                """
                )
                print(f"[✅] Filled {field_id} via JavaScript fallback")

                # Verify JavaScript fallback worked
                time.sleep(0.3)
                actual_value = self.driver.find_element(By.ID, field_id).get_attribute(
                    "value"
                )
                if actual_value != value:
                    print(
                        f"[⚠️] JavaScript fallback verification failed for {field_id}. Expected: {value}, Got: {actual_value}"
                    )

            if log_template:
                print(log_template.format(value))

        except Exception as e:
            print(f"[❌] Error filling {field_id}: {type(e).__name__} – {e}")
            # Try JavaScript fallback
            try:
                self.driver.execute_script(
                    f"""
                    let field = document.getElementById('{field_id}');
                    if (field) {{
                        field.value = '{value}';
                        field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        field.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                    }}
                """
                )
                print(f"[✅] Filled {field_id} via JavaScript fallback")

                # Verify JavaScript fallback worked
                time.sleep(0.3)
                actual_value = self.driver.find_element(By.ID, field_id).get_attribute(
                    "value"
                )
                if actual_value != value:
                    print(
                        f"[⚠️] JavaScript fallback verification failed for {field_id}. Expected: {value}, Got: {actual_value}"
                    )

            except Exception as js_error:
                print(
                    f"[❌] JavaScript fallback also failed for {field_id}: {js_error}"
                )
                raise e

    # ----------------------
    # Final Step
    # ----------------------
    def click_place_order(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(., 'Place Order')]")
                )
            )

            place_order_btn = self.driver.find_element(
                By.XPATH, "//button[contains(., 'Place Order')]"
            )
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")

            for _ in range(5):
                self.driver.execute_script("window.scrollBy(0, 300);")
                time.sleep(0.5)

            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(1)

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", place_order_btn
            )
            time.sleep(1)

            if is_mobile:
                self.driver.execute_script("arguments[0].click();", place_order_btn)
                print("[🛒📱] Clicked 'Place Order' using JS (Mobile).")
            else:
                place_order_btn.click()
                print("[🛒🖥️] Clicked 'Place Order' (Desktop).")

            self.driver.save_screenshot("after_place_order_click.png")

            WebDriverWait(self.driver, 25).until(
                lambda d: "Book Order #" in d.find_element(By.TAG_NAME, "body").text
            )
            print("[🎉] Order placed successfully!")

        except Exception as e:
            self.driver.save_screenshot("order_failure.png")
            with open("mobile_after_order.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print(f"[❌] Failed to place order: {type(e).__name__} – {e}")
            raise e

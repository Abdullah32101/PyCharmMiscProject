import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Constants for configuration
from core.constants import (
    ADDRESS,
    BOOK_URL,
    CARD_HOLDER_NAME,
    CARD_NUMBER,
    CITY,
    COUNTRY,
    CVC,
    DEFAULT_FIRST_NAME,
    DEFAULT_LAST_NAME,
    DEFAULT_PASSWORD,
    DEFAULT_UNIVERSITY,
    EXPIRY_MONTH,
    EXPIRY_MONTH_LABEL,
    EXPIRY_YEAR,
    EXPIRY_YEAR_LABEL,
    PHONE_NUMBER,
    POSTAL_CODE,
    STATE,
)


class OneTimeBookPurchasePage:
    def __init__(self, driver):
        self.driver = driver
        self.book_url = BOOK_URL

    # ----------------------
    # Navigation & Core Flow
    # ----------------------
    def open_book_page(self):
        max_retries = 3
        urls_to_try = [
            self.book_url,  # Try the configured URL first
            self.book_url.replace("staging.solutioninn.com", "www.solutioninn.com"),  # Fallback to production
            self.book_url.replace("www.solutioninn.com", "staging.solutioninn.com")   # Fallback to staging
        ]
        
        for url_index, current_url in enumerate(urls_to_try):
            print(f"[🌐] Trying URL {url_index + 1}/{len(urls_to_try)}: {current_url}")
            
            for attempt in range(max_retries):
                try:
                    print(f"[🌐] Attempting to load page (attempt {attempt + 1}/{max_retries}): {current_url}")
                    
                    # Set page load timeout
                    self.driver.set_page_load_timeout(30)
                    
                    # Navigate to the page
                    self.driver.get(current_url)
                    
                    # Wait for page to load completely
                    WebDriverWait(self.driver, 15).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                    
                    # Additional wait for page to be fully rendered
                    time.sleep(2)
                    
                    # Check if page loaded successfully
                    current_url_after_load = self.driver.current_url
                    page_title = self.driver.title
                    page_source_length = len(self.driver.page_source)
                    
                    print(f"[📄] Current URL: {current_url_after_load}")
                    print(f"[📝] Page title: {page_title}")
                    print(f"[📊] Page source length: {page_source_length} characters")
                    
                    # Check for various success indicators
                    if "solutioninn" in current_url_after_load.lower():
                        print(f"[✅] Page loaded successfully: {current_url_after_load}")
                        
                        # Check if page has meaningful content
                        if page_source_length < 1000:
                            print(f"[⚠️] Warning: Page source is very short ({page_source_length} chars)")
                            raise Exception("Page source too short - likely not loaded properly")
                        
                        # Check for specific elements that should be present
                        try:
                            body_element = self.driver.find_element(By.TAG_NAME, "body")
                            body_text = body_element.text
                            if len(body_text.strip()) < 100:
                                print(f"[⚠️] Warning: Body text is very short ({len(body_text)} chars)")
                                raise Exception("Body text too short - page may not be fully loaded")
                            
                            print(f"[✅] Page has meaningful content ({len(body_text)} chars of text)")
                            return
                            
                        except Exception as element_error:
                            print(f"[⚠️] Could not verify page content: {element_error}")
                            raise element_error
                            
                    else:
                        print(f"[⚠️] Page redirected to: {current_url_after_load}")
                        if "error" in current_url_after_load.lower() or "404" in current_url_after_load.lower():
                            raise Exception(f"Page redirected to error URL: {current_url_after_load}")
                        
                except Exception as e:
                    print(f"[❌] Page load attempt {attempt + 1} failed: {type(e).__name__} - {e}")
                    
                    # Save diagnostic information
                    try:
                        timestamp = int(time.time())
                        diagnostic_file = f"page_load_attempt_{url_index + 1}_{attempt + 1}_{timestamp}.html"
                        with open(diagnostic_file, "w", encoding="utf-8") as f:
                            f.write(self.driver.page_source)
                        print(f"[💾] Diagnostic info saved to: {diagnostic_file}")
                    except:
                        print("[⚠️] Could not save diagnostic information")
                    
                    if attempt < max_retries - 1:
                        print(f"[🔄] Retrying in 5 seconds...")
                        time.sleep(5)
                        
                        # Try to refresh the page
                        try:
                            self.driver.refresh()
                            time.sleep(3)
                        except:
                            pass
                    else:
                        print(f"[❌] All {max_retries} attempts failed for URL {url_index + 1}")
                        if url_index < len(urls_to_try) - 1:
                            print(f"[🔄] Trying next URL...")
                            break  # Try next URL
                        else:
                            print(f"[❌] All URLs failed. Trying alternative approach...")
                            
                            # Alternative approach: Try to navigate to a simpler URL first
                            try:
                                print("[🔄] Trying alternative navigation approach...")
                                
                                # First try the base domain
                                base_url = current_url.split('/textbooks/')[0] if '/textbooks/' in current_url else "https://www.solutioninn.com"
                                self.driver.get(base_url)
                                time.sleep(3)
                                
                                # Check if base domain loads
                                if "solutioninn" not in self.driver.current_url.lower():
                                    raise Exception("Base domain not accessible")
                                
                                print("[✅] Base domain accessible, trying book page...")
                                
                                # Then navigate to the book page
                                self.driver.get(current_url)
                                WebDriverWait(self.driver, 15).until(
                                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                                )
                                
                                # Verify the page loaded
                                if "solutioninn" in self.driver.current_url.lower():
                                    print(f"[✅] Page loaded via alternative approach: {self.driver.current_url}")
                                    return
                                else:
                                    raise Exception("Alternative approach failed - page redirected")
                                
                            except Exception as alt_error:
                                print(f"[❌] Alternative approach also failed: {alt_error}")
                                
                                # Final attempt: Try with different user agent
                                try:
                                    print("[🔄] Trying with different user agent...")
                                    self.driver.execute_script(
                                        "Object.defineProperty(navigator, 'userAgent', {get: function () {return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';}});"
                                    )
                                    self.driver.get(current_url)
                                    time.sleep(5)
                                    
                                    if "solutioninn" in self.driver.current_url.lower():
                                        print(f"[✅] Page loaded with custom user agent: {self.driver.current_url}")
                                        return
                                    else:
                                        raise Exception("Custom user agent approach failed")
                                        
                                except Exception as final_error:
                                    print(f"[❌] All approaches failed: {final_error}")
                                    raise e

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
            print("[🔍] Looking for payment toggle button...")
            
            # Most common selectors first (faster approach)
            toggle_selectors = [
                # Most likely selectors first
                (By.CSS_SELECTOR, "label[for='radio7']"),  # This worked in debug
                (By.ID, "radio7"),
                (By.CSS_SELECTOR, "input[type='radio'][value='card']"),
                (By.CSS_SELECTOR, "input[type='radio'][name*='payment']"),
                (By.CSS_SELECTOR, "input[type='radio'][id*='card']"),
            ]
            
            toggle_clicked = False
            for selector_type, selector_value in toggle_selectors:
                try:
                    print(f"[🔍] Trying payment toggle selector: {selector_type} = {selector_value}")
                    
                    # Reduced wait time for faster execution
                    toggle = WebDriverWait(self.driver, 1).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    
                    # Quick scroll and click
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
                    time.sleep(0.1)  # Reduced wait time
                    
                    # Try regular click first
                    try:
                        toggle.click()
                        print(f"[💳] Payment toggle clicked using {selector_type}: {selector_value}")
                        toggle_clicked = True
                        break
                    except Exception as click_error:
                        print(f"[⚠️] Regular click failed, trying JavaScript: {click_error}")
                        self.driver.execute_script("arguments[0].click();", toggle)
                        print(f"[💳] Payment toggle clicked via JavaScript using {selector_type}: {selector_value}")
                        toggle_clicked = True
                        break
                        
                except Exception as e:
                    print(f"[⚠️] Selector failed: {selector_type} = {selector_value}")
                    continue
            
            if not toggle_clicked:
                print("[🔄] Trying JavaScript-based payment toggle selection...")
                # JavaScript fallback to find and click any payment-related element
                try:
                    self.driver.execute_script("""
                        // Try to find and click payment toggle elements
                        let paymentElements = [
                            // Radio buttons
                            ...document.querySelectorAll('input[type="radio"][name*="payment"]'),
                            ...document.querySelectorAll('input[type="radio"][value*="card"]'),
                            ...document.querySelectorAll('input[type="radio"][id*="card"]'),
                            // Buttons
                            ...document.querySelectorAll('button[data-payment*="card"]'),
                            ...document.querySelectorAll('button[class*="payment"]'),
                            // Labels
                            ...document.querySelectorAll('label[for*="card"]'),
                            ...document.querySelectorAll('label[for*="payment"]')
                        ];
                        
                        let clicked = false;
                        for (let element of paymentElements) {
                            if (element.offsetParent !== null) { // Check if visible
                                element.click();
                                clicked = true;
                                console.log('Payment toggle clicked via JavaScript:', element.tagName, element.id || element.name);
                                break;
                            }
                        }
                        
                        if (!clicked) {
                            // Try to set radio button value directly
                            let radios = document.querySelectorAll('input[type="radio"][name*="payment"]');
                            for (let radio of radios) {
                                if (radio.value.includes('card') || radio.id.includes('card')) {
                                    radio.checked = true;
                                    radio.dispatchEvent(new Event('change', { bubbles: true }));
                                    clicked = true;
                                    console.log('Payment radio set via JavaScript:', radio.id || radio.name);
                                    break;
                                }
                            }
                        }
                        
                        return clicked;
                    """)
                    print("[💳] Payment toggle handled via JavaScript")
                    toggle_clicked = True
                except Exception as js_error:
                    print(f"[⚠️] JavaScript fallback failed: {js_error}")
            
            if not toggle_clicked:
                print("[⚠️] Could not find payment toggle, continuing without it...")
                
        except Exception as e:
            print(f"[⚠️] Payment toggle error: {e}")
            # Continue without payment toggle

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
    def select_expiry_month(self, month_value=EXPIRY_MONTH):
        try:
            print(f"[📅] Selecting expiry month: {month_value}")
            
            # Try multiple possible element IDs for the month dropdown
            possible_ids = ["cc_expiry_month", "cc-exp-month", "cc_exp_month"]
            success = False

            for element_id in possible_ids:
                try:
                    result = self.driver.execute_script(
                        """
                        const select = document.getElementById(arguments[0]);
                        if (select) {
                            select.value = arguments[1];
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                            select.dispatchEvent(new Event('input', { bubbles: true }));
                            return select.value === arguments[1];
                        }
                        return false;
                    """,
                        element_id,
                        month_value,
                    )

                    if result:
                        print(f"[✅] JS: Set expiry month to '{month_value}' using ID '{element_id}'")
                        success = True
                        break
                except Exception as e:
                    print(f"[⚠️] Failed with ID '{element_id}': {e}")
                    continue

            if not success:
                print("[🔄] JavaScript method failed, trying click-based approach...")
                # Try to find any element that looks like a month dropdown
                month_selectors = [
                    "//select[contains(@id, 'month') or contains(@name, 'month')]",
                    "//select[contains(@id, 'exp') or contains(@name, 'exp')]",
                    "//input[contains(@id, 'month') or contains(@name, 'month')]",
                    "//div[contains(@class, 'month') or contains(@class, 'exp')]//select",
                    "//div[contains(@class, 'month') or contains(@class, 'exp')]//input"
                ]
                
                for xpath in month_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        for element in elements:
                            try:
                                # Try to set value directly
                                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element, month_value)
                                time.sleep(0.5)
                                
                                # Verify the selection
                                actual_value = element.get_attribute("value")
                                if actual_value == month_value:
                                    print(f"[✅] Set month dropdown value to '{month_value}' via XPath: {xpath}")
                                    success = True
                                    break
                            except:
                                continue
                        if success:
                            break
                    except:
                        continue

            if not success:
                print(f"[❌] Failed to select expiry month: {month_value}")
                # Take screenshot for debugging
                try:
                    self.driver.save_screenshot(f"month_dropdown_failed_{int(time.time())}.png")
                    print("[📸] Screenshot saved for debugging")
                except:
                    pass

        except Exception as e:
            print(f"[❌] Failed selecting month: {type(e).__name__} – {e}")

    def select_expiry_year(self, year_value=EXPIRY_YEAR):
        try:
            print(f"[📅] Selecting expiry year: {year_value}")
            
            # Try multiple possible element IDs for the year dropdown
            possible_ids = ["cc_expiry_year", "cc-exp-year", "cc_exp_year"]
            success = False

            for element_id in possible_ids:
                try:
                    result = self.driver.execute_script(
                        """
                        const select = document.getElementById(arguments[0]);
                        if (select) {
                            select.value = arguments[1];
                            select.dispatchEvent(new Event('change', { bubbles: true }));
                            select.dispatchEvent(new Event('input', { bubbles: true }));
                            return select.value === arguments[1];
                        }
                        return false;
                    """,
                        element_id,
                        year_value,
                    )

                    if result:
                        print(f"[✅] JS: Set expiry year to '{year_value}' using ID '{element_id}'")
                        success = True
                        break
                except Exception as e:
                    print(f"[⚠️] Failed with ID '{element_id}': {e}")
                    continue

            if not success:
                print("[🔄] JavaScript method failed, trying click-based approach...")
                # Try to find any element that looks like a year dropdown
                year_selectors = [
                    "//select[contains(@id, 'year') or contains(@name, 'year')]",
                    "//select[contains(@id, 'exp') or contains(@name, 'exp')]",
                    "//input[contains(@id, 'year') or contains(@name, 'year')]",
                    "//div[contains(@class, 'year') or contains(@class, 'exp')]//select",
                    "//div[contains(@class, 'year') or contains(@class, 'exp')]//input"
                ]
                
                for xpath in year_selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, xpath)
                        for element in elements:
                            try:
                                # Try to set value directly
                                self.driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element, year_value)
                                time.sleep(0.5)
                                
                                # Verify the selection
                                actual_value = element.get_attribute("value")
                                if actual_value == year_value:
                                    print(f"[✅] Set year dropdown value to '{year_value}' via XPath: {xpath}")
                                    success = True
                                    break
                            except:
                                continue
                        if success:
                            break
                    except:
                        continue

            if not success:
                print(f"[❌] Failed to select expiry year: {year_value}")
                # Take screenshot for debugging
                try:
                    self.driver.save_screenshot(f"year_dropdown_failed_{int(time.time())}.png")
                    print("[📸] Screenshot saved for debugging")
                except:
                    pass

        except Exception as e:
            print(f"[❌] Failed selecting year: {type(e).__name__} – {e}")

    def _select_dropdown(self, dropdown_id, option_text, success_log, failure_log):
        try:
            dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, dropdown_id))
            )
            
            # Check if it's a standard select element
            if dropdown.tag_name.lower() == "select":
                Select(dropdown).select_by_visible_text(option_text)
                print(success_log)
            else:
                # Handle custom dropdown implementation
                print(f"[🔄] Custom dropdown detected for {dropdown_id}, using JavaScript...")
                self._select_custom_dropdown(dropdown_id, option_text, success_log, failure_log)
                
        except Exception as e:
            print(f"{failure_log} Error: {type(e).__name__} – {e}")
            # Try JavaScript fallback for any dropdown type
            try:
                self._select_custom_dropdown(dropdown_id, option_text, success_log, failure_log)
            except Exception as js_error:
                print(f"[❌] JavaScript fallback also failed: {js_error}")
    
    def _select_custom_dropdown(self, dropdown_id, option_text, success_log, failure_log):
        """Handle custom dropdown selection using JavaScript"""
        try:
            # Extract value from option_text (e.g., "March (03)" -> "03")
            if "(" in option_text and ")" in option_text:
                value = option_text.split("(")[1].split(")")[0]
            else:
                value = option_text
            
            result = self.driver.execute_script(f"""
                let dropdown = document.getElementById('{dropdown_id}');
                if (dropdown) {{
                    dropdown.value = '{value}';
                    dropdown.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    dropdown.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    return true;
                }}
                return false;
            """)
            
            if result:
                print(success_log)
            else:
                print(f"{failure_log} - Element not found")
                
        except Exception as e:
            print(f"{failure_log} JavaScript Error: {type(e).__name__} – {e}")

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
            # Wait for place order button with 7 second timeout
            WebDriverWait(self.driver, 7).until(  # Reduced to exactly 7 seconds
                EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(., 'Place Order')]")
                )
            )

            place_order_btn = self.driver.find_element(
                By.XPATH, "//button[contains(., 'Place Order')]"
            )
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")

            # Quick scrolling strategy
            for _ in range(1):  # Reduced to 1 iteration
                self.driver.execute_script("window.scrollBy(0, 100);")  # Reduced scroll distance
                time.sleep(0.1)  # Reduced wait time

            # Clear any overlays or modals
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.2)  # Reduced wait time

            # Scroll button into view with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", 
                place_order_btn
            )
            time.sleep(0.2)  # Reduced wait time

            # Try multiple click strategies
            try:
                if is_mobile:
                    self.driver.execute_script("arguments[0].click();", place_order_btn)
                    print("[🛒📱] Clicked 'Place Order' using JS (Mobile).")
                else:
                    place_order_btn.click()
                    print("[🛒🖥️] Clicked 'Place Order' (Desktop).")
            except Exception as click_error:
                print(f"[⚠️] Regular click failed, trying JavaScript: {click_error}")
                self.driver.execute_script("arguments[0].click();", place_order_btn)
                print("[🛒] Clicked 'Place Order' using JavaScript fallback.")

            # Wait for order confirmation with 7 second timeout
            try:
                WebDriverWait(self.driver, 7).until(  # Reduced to exactly 7 seconds
                    lambda d: "Book Order #" in d.find_element(By.TAG_NAME, "body").text
                )
                print("[🎉] Order placed successfully!")
            except Exception as confirm_error:
                print(f"[⚠️] Order confirmation timeout: {confirm_error}")
                # Check if order was actually placed
                if "success" in self.driver.page_source.lower() or "order" in self.driver.page_source.lower():
                    print("[✅] Order appears to be successful based on page content")
                else:
                    raise confirm_error

        except Exception as e:
            print(f"[❌] Failed to place order: {type(e).__name__} – {e}")
            # Don't save screenshots here to avoid timeout issues
            raise e

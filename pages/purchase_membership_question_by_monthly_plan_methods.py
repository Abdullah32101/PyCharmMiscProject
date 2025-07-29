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
)


class SolutionInnPrimaryPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = PRIMARY_URL

    def open(self):
        self.driver.get(self.url)

    def zoom_out(self, zoom_level=0.8):
        """Zoom out the page to make elements more visible"""
        try:
            self.driver.execute_script(f"document.body.style.zoom = '{zoom_level}'")
            print(f"[ZOOM] Zoomed out to {zoom_level * 100}%")
        except Exception as e:
            print(f"[WARNING] Zoom failed: {type(e).__name__} - {e}")

    def zoom_in(self, zoom_level=1.2):
        """Zoom in the page"""
        try:
            self.driver.execute_script(f"document.body.style.zoom = '{zoom_level}'")
            print(f"[SEARCH] Zoomed in to {zoom_level * 100}%")
        except Exception as e:
            print(f"[WARNING] Zoom failed: {type(e).__name__} - {e}")

    def reset_zoom(self):
        """Reset zoom to normal (100%)"""
        try:
            self.driver.execute_script("document.body.style.zoom = '1'")
            print("[SEARCH] Zoom reset to 100%")
        except Exception as e:
            print(f"[WARNING] Zoom reset failed: {type(e).__name__} - {e}")

    def open_custom_url(self, url):
        self.driver.get(url)

    def click_view_solution_button(self):
        try:
            # Try multiple selectors to find the View Solution button
            working_selector = None
            
            # Selectors for the View Solution button
            selectors = [
                ".view_solution_btn.step1PopupButton",
                ".view_solution_btn",
                "button.view_solution_btn",
                "[class*='view_solution']",
                "[class*='step1PopupButton']",
                "button[class*='view']",
                "button[class*='solution']",
                "//button[contains(text(), 'View Solution')]",
                "//button[contains(text(), 'view solution')]",
                "//a[contains(text(), 'View Solution')]",
                "//a[contains(text(), 'view solution')]",
                "//*[contains(text(), 'View Solution')]",
                "//*[contains(text(), 'view solution')]",
            ]
            
            # Find working selector first
            for selector in selectors:
                try:
                    print(f"[SEARCH] Trying View Solution button selector: {selector}")
                    
                    if selector.startswith("//"):
                        # XPath selector
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        button = self.driver.find_element(By.XPATH, selector)
                    else:
                        # CSS selector
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if button and button.is_displayed():
                        working_selector = selector
                        print(f"[SUCCESS] Found View Solution button with selector: {selector}")
                        break
                        
                except Exception as e:
                    print(f"[FAIL] Selector {selector} failed: {type(e).__name__}")
                    continue
            
            if not working_selector:
                raise Exception("Could not find View Solution button with any selector")
            
            # Enhanced accordion and overlay handling
            try:
                # Close any open accordions that might be blocking the button
                accordion_elements = self.driver.find_elements(By.CSS_SELECTOR, ".accordion.step-heading")
                for accordion in accordion_elements:
                    if "active" in accordion.get_attribute("class") or "open" in accordion.get_attribute("class"):
                        self.driver.execute_script("arguments[0].click();", accordion)
                        time.sleep(0.5)
                        print("[FIX] Closed overlapping accordion element")
                
                # Remove any other overlapping elements
                self.driver.execute_script("""
                    // Remove any overlays, modals, or popups
                    var overlays = document.querySelectorAll('.modal, .overlay, .popup, .tooltip, .dropdown-menu');
                    overlays.forEach(function(overlay) {
                        overlay.style.display = 'none';
                        overlay.style.visibility = 'hidden';
                    });
                    
                    // Hide any elements that might be covering the button
                    var coveringElements = document.querySelectorAll('[style*="z-index"]');
                    coveringElements.forEach(function(element) {
                        if (parseInt(element.style.zIndex) > 1000) {
                            element.style.display = 'none';
                        }
                    });
                """)
                time.sleep(0.5)
                print("[FIX] Removed potential overlapping elements")
                
            except Exception as cleanup_error:
                print(f"[WARNING] Could not clean up overlapping elements: {cleanup_error}")
            
            # Try multiple click strategies with fresh element finding
            click_success = False
            
            # Strategy 1: Regular click with fresh element
            if not click_success:
                try:
                    # Re-find the element right before clicking to avoid stale element
                    if working_selector.startswith("//"):
                        button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, working_selector))
                        )
                    else:
                        button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, working_selector))
                        )
                    
                    # Scroll to button with better positioning
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", button)
                    time.sleep(1)
                    
                    button.click()
                    print("[SUCCESS] Clicked 'View Solution' button successfully")
                    click_success = True
                except Exception as click_error:
                    print(f"[WARNING] Regular click failed: {click_error}")
            
            # Strategy 2: JavaScript click with fresh element
            if not click_success:
                try:
                    # Re-find the element
                    if working_selector.startswith("//"):
                        button = self.driver.find_element(By.XPATH, working_selector)
                    else:
                        button = self.driver.find_element(By.CSS_SELECTOR, working_selector)
                    
                    self.driver.execute_script("arguments[0].click();", button)
                    print("[SUCCESS] Clicked 'View Solution' button using JavaScript")
                    click_success = True
                except Exception as js_error:
                    print(f"[WARNING] JavaScript click failed: {js_error}")
            
            # Strategy 3: Force click with fresh element
            if not click_success:
                try:
                    # Re-find the element
                    if working_selector.startswith("//"):
                        button = self.driver.find_element(By.XPATH, working_selector)
                    else:
                        button = self.driver.find_element(By.CSS_SELECTOR, working_selector)
                    
                    # Scroll to button and force click
                    self.driver.execute_script("""
                        arguments[0].scrollIntoView({block: 'center', inline: 'center'});
                        arguments[0].focus();
                        arguments[0].dispatchEvent(new MouseEvent('click', {
                            bubbles: true,
                            cancelable: true,
                            view: window
                        }));
                    """, button)
                    print("[SUCCESS] Clicked 'View Solution' button using force click")
                    click_success = True
                except Exception as force_error:
                    print(f"[WARNING] Force click failed: {force_error}")
            
            # Strategy 4: Final attempt with element removal and fresh element
            if not click_success:
                try:
                    # Remove all potential blockers and try again
                    self.driver.execute_script("""
                        // Remove all potential blocking elements
                        var blockers = document.querySelectorAll('.modal, .overlay, .popup, .tooltip, .dropdown-menu, .accordion.step-heading');
                        blockers.forEach(function(blocker) {
                            blocker.remove();
                        });
                    """)
                    time.sleep(1)
                    
                    # Re-find the element one more time
                    if working_selector.startswith("//"):
                        button = self.driver.find_element(By.XPATH, working_selector)
                    else:
                        button = self.driver.find_element(By.CSS_SELECTOR, working_selector)
                    
                    # Try clicking again
                    self.driver.execute_script("arguments[0].click();", button)
                    print("[SUCCESS] Clicked 'View Solution' button after removing all blockers")
                    click_success = True
                except Exception as final_error:
                    print(f"[ERROR] All click strategies failed: {final_error}")
                    raise final_error
                        
        except Exception as e:
            print(f"[ERROR] Failed to click View Solution button: {type(e).__name__} - {e}")
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
            print(f"[MOBILE] Clicking Popular Plan button on {'Mobile' if is_mobile else 'Desktop'}")

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
                print(f"[SUCCESS] Popular Plan button clicked successfully: '{button.text.strip()}'")
            except Exception as click_error:
                print(f"[WARNING] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[SUCCESS] Popular Plan button clicked with JavaScript: '{button.text.strip()}'")

        except Exception as e:
            print(f"[ERROR] Failed to click Popular Plan button: {type(e).__name__} - {e}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot(f"popular_plan_failed_{int(time.time())}.png")
                print("[SCREENSHOT] Screenshot saved for debugging")
            except:
                pass
            raise e

    def click_monthly_access_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[MOBILE] Clicking Monthly Access button on {'Mobile' if is_mobile else 'Desktop'}")

            # Try multiple selectors for Monthly Access button
            selectors = [
                "//div[@class='new-month-day-trail-1 plans-card-header']//button[@type='button'][normalize-space()='View Solution']",
                "//div[contains(@class,'month-day-trail-1')]//button[contains(text(),'View Solution')]",
                "//div[contains(@class,'month')]//button[contains(text(),'View Solution')]",
                "//button[contains(text(),'View Solution')]",
                "//button[contains(text(),'view solution')]",
                "//a[contains(text(),'View Solution')]",
                "//a[contains(text(),'view solution')]",
                "//*[contains(text(),'View Solution')]",
                "//*[contains(text(),'view solution')]",
                "//div[contains(@class,'monthly')]//button",
                "//div[contains(@class,'month')]//button",
                "//button[contains(@class,'monthly')]",
                "//button[contains(@class,'month')]",
                "//div[contains(@class,'trail-1')]//button",
                "//div[contains(@class,'trail')]//button",
                "//button[contains(text(),'Monthly')]",
                "//button[contains(text(),'monthly')]",
                "//a[contains(text(),'Monthly')]",
                "//a[contains(text(),'monthly')]",
            ]
            
            button = None
            working_selector = None
            
            # Find working selector first
            for selector in selectors:
                try:
                    print(f"[SEARCH] Trying Monthly Access button selector: {selector}")
                    
                    if selector.startswith("//"):
                        # XPath selector
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        button = self.driver.find_element(By.XPATH, selector)
                    else:
                        # CSS selector
                        WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if button and button.is_displayed():
                        working_selector = selector
                        print(f"[SUCCESS] Found Monthly Access button with selector: {selector}")
                        break
                        
                except Exception as e:
                    print(f"[FAIL] Selector {selector} failed: {type(e).__name__}")
                    continue
            
            if not working_selector:
                raise Exception("Could not find Monthly Access button with any selector")
            
            # Wait for page to stabilize after finding the button
            time.sleep(2)
            
            # Try multiple click strategies with immediate execution
            click_success = False
            
            # Strategy 1: Immediate click with fresh element
            if not click_success:
                try:
                    # Re-find the element and click immediately
                    if working_selector.startswith("//"):
                        button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, working_selector))
                        )
                    else:
                        button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, working_selector))
                        )
                    
                    # Click immediately without scrolling first
                    button.click()
                    print(f"[SUCCESS] Monthly Access button clicked successfully: '{button.text.strip()}'")
                    click_success = True
                except Exception as click_error:
                    print(f"[WARNING] Immediate click failed: {click_error}")
            
            # Strategy 2: JavaScript click with fresh element
            if not click_success:
                try:
                    # Re-find the element
                    if working_selector.startswith("//"):
                        button = self.driver.find_element(By.XPATH, working_selector)
                    else:
                        button = self.driver.find_element(By.CSS_SELECTOR, working_selector)
                    
                    # Click with JavaScript immediately
                    self.driver.execute_script("arguments[0].click();", button)
                    print(f"[SUCCESS] Monthly Access button clicked with JavaScript: '{button.text.strip()}'")
                    click_success = True
                except Exception as js_error:
                    print(f"[WARNING] JavaScript click failed: {js_error}")
            
            # Strategy 3: Direct XPath click without finding element first
            if not click_success:
                try:
                    # Click directly using XPath without finding the element first
                    if working_selector.startswith("//"):
                        self.driver.execute_script(f"""
                            let element = document.evaluate('{working_selector}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            if (element) {{
                                element.click();
                            }}
                        """)
                    else:
                        self.driver.execute_script(f"""
                            let element = document.querySelector('{working_selector}');
                            if (element) {{
                                element.click();
                            }}
                        """)
                    print(f"[SUCCESS] Monthly Access button clicked using direct XPath/CSS: {working_selector}")
                    click_success = True
                except Exception as direct_error:
                    print(f"[WARNING] Direct XPath/CSS click failed: {direct_error}")
            
            # Strategy 4: Try clicking by text content
            if not click_success:
                try:
                    # Try to find and click any button with "View Solution" text
                    self.driver.execute_script("""
                        let buttons = document.querySelectorAll('button, a, input[type="button"]');
                        for (let button of buttons) {
                            if (button.textContent && button.textContent.toLowerCase().includes('view solution')) {
                                button.click();
                                return true;
                            }
                        }
                        return false;
                    """)
                    print(f"[SUCCESS] Monthly Access button clicked using text search")
                    click_success = True
                except Exception as text_error:
                    print(f"[WARNING] Text-based click failed: {text_error}")
            
            if not click_success:
                raise Exception("All click strategies failed for Monthly Access button")

        except Exception as e:
            print(f"[ERROR] Failed to click Monthly Access button: {type(e).__name__} - {e}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot(f"monthly_access_failed_{int(time.time())}.png")
                print("[SCREENSHOT] Screenshot saved for debugging")
            except:
                pass
            raise e

    def click_six_month_plan_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(f"[MOBILE] Clicking Six Month Plan button on {'Mobile' if is_mobile else 'Desktop'}")

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
                print(f"[SUCCESS] Six Month Plan button clicked successfully: '{button.text.strip()}'")
            except Exception as click_error:
                print(f"[WARNING] Regular click failed, trying JavaScript: {type(click_error).__name__}")
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[SUCCESS] Six Month Plan button clicked with JavaScript: '{button.text.strip()}'")

        except Exception as e:
            print(f"[ERROR] Failed to click Six Month Plan button: {type(e).__name__} - {e}")
            # Take screenshot for debugging
            try:
                self.driver.save_screenshot(f"six_month_plan_failed_{int(time.time())}.png")
                print("[SCREENSHOT] Screenshot saved for debugging")
            except:
                pass
            raise e

    def click_one_time_plan_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(
                f"[MOBILE] Clicking One Time Plan button on {'Mobile' if is_mobile else 'Desktop'}"
            )

            # Try multiple selectors for the one-time plan button
            selectors = [
                "//button[contains(@class,'new-btn-blue-area activate_button')]",
                "//button[contains(text(), 'One Time')]",
                "//button[contains(text(), 'one time')]",
                "//button[contains(text(), 'One-Time')]",
                "//button[contains(text(), 'one-time')]",
                "//a[contains(text(), 'One Time')]",
                "//a[contains(text(), 'one time')]",
                "//a[contains(text(), 'One-Time')]",
                "//a[contains(text(), 'one-time')]",
            ]

            button_found = False
            for i, selector in enumerate(selectors):
                try:
                    print(f"[SEARCH] Trying selector {i+1}/{len(selectors)}: {selector}")
                    button = WebDriverWait(
                        self.driver, 3
                    ).until(  # Reduced from 10 seconds
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )

                    # Scroll to element with better positioning
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                        button,
                    )
                    time.sleep(0.2)  # Reduced from 1 second

                    # Try regular click first
                    try:
                        button.click()
                        print(
                            f"[✓] Clicked One Time Plan button using selector: {selector}"
                        )
                        button_found = True
                        break
                    except Exception as click_error:
                        print(
                            f"[WARNING] Regular click failed, trying JavaScript click: {type(click_error).__name__}"
                        )
                        # Try JavaScript click as fallback
                        self.driver.execute_script("arguments[0].click();", button)
                        print(
                            f"[✓] Clicked One Time Plan button using JavaScript: {selector}"
                        )
                        button_found = True
                        break

                except Exception as e:
                    print(f"[WARNING] Selector {i+1} failed: {type(e).__name__}")
                    continue

            if not button_found:
                # Fallback: try to find any button that might be the one-time plan
                print(
                    "[RETRY] Trying fallback method - searching for any relevant buttons..."
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
                                    "one time",
                                    "one-time",
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
                            f"[SEARCH] Found {len(relevant_elements)} potentially relevant elements"
                        )
                        for i, element in enumerate(
                            relevant_elements[:5]
                        ):  # Try first 5
                            try:
                                print(
                                    f"[SEARCH] Trying fallback element {i+1}: {element.text[:50]}..."
                                )
                                self.driver.execute_script(
                                    "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                                    element,
                                )
                                time.sleep(0.2)  # Reduced from 1 second

                                try:
                                    element.click()
                                    print(
                                        f"[✓] Clicked fallback element: {element.text[:50]}..."
                                    )
                                    button_found = True
                                    break
                                except Exception as click_error:
                                    print(
                                        f"[WARNING] Regular click failed, trying JavaScript click: {type(click_error).__name__}"
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
                                    f"[WARNING] Fallback element {i+1} failed: {type(e).__name__}"
                                )
                                continue
                    else:
                        print("[ERROR] No relevant buttons/links found")

                except Exception as fallback_error:
                    print(
                        f"[ERROR] Fallback method failed: {type(fallback_error).__name__} - {fallback_error}"
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
                        f"[SCREENSHOT] Debug files saved: one_time_plan_button_not_found_{timestamp}.png"
                    )
                    print(
                        f"[FILE] Debug files saved: one_time_plan_page_source_{timestamp}.html"
                    )
                    raise Exception("No one-time plan button found after all attempts")

        except Exception as e:
            print(
                f"[ERROR] Failed to click One Time Plan button: {type(e).__name__} - {e}"
            )
            raise e

    def _click_plan_button(self, xpath, label):
        """Generic method to click plan buttons"""
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )

            # Scroll to element with better positioning
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                button,
            )
            time.sleep(0.2)  # Reduced from 1 second

            # Try regular click first
            try:
                button.click()
                print(f"[✓] Clicked {label} button")
            except Exception as click_error:
                print(
                    f"[WARNING] Regular click failed, trying JavaScript click: {type(click_error).__name__}"
                )
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print(f"[✓] Clicked {label} button using JavaScript")

        except Exception as e:
            print(f"[ERROR] Failed to click {label} button: {type(e).__name__} - {e}")
            raise e

    def click_payment_toggle(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(
                f"[📱] Looking for Payment Toggle on {'Mobile' if is_mobile else 'Desktop'}"
            )

            # Try multiple selectors for payment toggle (same as secondary page)
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

            # Enhanced mobile handling for card details (same as secondary page)
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
                print(
                    f"[WARNING] Card field {element_id} verification failed. Expected: {value}, Got: {actual_value}"
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
                print(f"[SUCCESS] Card field {element_id} filled via JavaScript fallback.")

                # Final verification
                time.sleep(0.3)
                final_value = field.get_attribute("value")
                if final_value != value:
                    print(
                        f"[ERROR] Card field {element_id} still not correct after JavaScript fallback. Expected: {value}, Got: {final_value}"
                    )
                else:
                    print(
                        f"[SUCCESS] Card field {element_id} filled successfully using JavaScript fallback."
                    )
            else:
                print(f"[SUCCESS] Card field {element_id} filled successfully: {value}")

        except Exception as e:
            print(
                f"[ERROR] Error in _fill_card_field_mobile for {element_id}: {type(e).__name__} - {e}"
            )
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
            print(f"[ERROR] Error filling field {element_id}: {type(e).__name__} - {e}")
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
                        print(
                            f"[WEB] JS: Set expiry month to '{month_value}' using ID '{element_id}'"
                        )
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
                print(f"[DATE] Selected month: {month_value} using click method")

        except Exception as e:
            print(f"[ERROR] Failed selecting month: {type(e).__name__} - {e}")

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
                        print(
                            f"[WEB] JS: Set expiry year to '{year_value}' using ID '{element_id}'"
                        )
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
                print(f"[DATE] Selected year: {year_value} using click method")

        except Exception as e:
            print(f"[ERROR] Failed selecting year: {type(e).__name__} - {e}")

    def click_join_now_button(self):
        try:
            is_mobile = self.driver.execute_script("return window.innerWidth < 768;")
            print(
                f"[MOBILE] Clicking Join Now button on {'Mobile' if is_mobile else 'Desktop'}"
            )

            # Try multiple possible selectors for the Join Now button
            possible_selectors = [
                (
                    By.ID,
                    "submit_btn_checkout",
                ),  # Primary selector (like secondary page)
                (By.XPATH, "//button[contains(text(), 'Join Now')]"),  # Fallback XPath
                (
                    By.XPATH,
                    "//button[contains(text(), 'join now')]",
                ),  # Case insensitive
                (By.XPATH, "//input[@value='Join Now']"),  # Input button
                (By.CSS_SELECTOR, "button[type='submit']"),  # Generic submit button
            ]

            button = None
            for selector_type, selector_value in possible_selectors:
                try:
                    button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    print(
                        f"[SEARCH] Found Join Now button using: {selector_type} = '{selector_value}'"
                    )
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
                print(
                    f"[WARNING] Regular click failed, trying JavaScript click: {type(click_error).__name__}"
                )
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", button)
                print("[✓] Clicked Join Now button using JavaScript")

        except Exception as e:
            print(f"[ERROR] Failed to click Join Now button: {type(e).__name__} - {e}")
            raise e

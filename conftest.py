import os
import traceback

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from db.db_helper import MySQLHelper
from screenshot_utils import screenshot_manager

# By default: headless = True for CI environments
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

# Initialize database helper lazily to avoid import-time connection issues
db_helper = None


def get_db_helper():
    """Get database helper instance, creating it if needed"""
    global db_helper
    if db_helper is None:
        db_helper = MySQLHelper()
    return db_helper


# Global variable to store device information
_device_info = {"name": "unknown", "resolution": "unknown"}


@pytest.fixture(scope="function")
def device_info():
    """Fixture to store and retrieve device information"""
    return _device_info


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Setup database table for test results"""
    helper = get_db_helper()
    helper.create_test_results_table()
    yield
    helper.close()


@pytest.fixture(autouse=True)
def capture_test_results(request, device_info):
    """Automatically capture test results and store in database"""
    import time

    # Get test information
    test_name = request.node.name
    module_name = request.module.__name__ if request.module else "unknown"

    # Start timing
    start_time = time.time()

    # Run the test
    yield

    # Calculate duration
    end_time = time.time()
    total_time_duration = round(end_time - start_time, 3)

    # Get device information from the global variable
    device_name = device_info["name"]
    screen_resolution = device_info["resolution"]

    # Get device information and screen resolution from driver if available
    try:
        # Try to get driver from the request if it's available
        if hasattr(request, "funcargs") and "driver" in request.funcargs:
            driver = request.funcargs["driver"]
            if driver:
                # Get device name from the parametrized fixture - this is the key fix
                # The device name comes from the driver fixture's request.param
                if hasattr(request, "funcargs") and "driver" in request.funcargs:
                    driver_fixture = request._fixturemanager._arg2fixturedefs["driver"][
                        0
                    ]
                    if (
                        hasattr(driver_fixture, "cached_result")
                        and driver_fixture.cached_result
                    ):
                        # Get the device name from the driver fixture's cached result
                        device_name = driver_fixture.cached_result[0].param
                        print(
                            f"[📱] Got device name from driver fixture: {device_name}"
                        )

                # If we still don't have a device name, try to get it from the current request
                if (
                    device_name == "unknown"
                    and hasattr(request, "param")
                    and request.param
                ):
                    device_name = request.param
                    print(f"[📱] Got device name from request param: {device_name}")

                # Get actual screen resolution from the driver
                try:
                    width = driver.execute_script("return window.innerWidth;")
                    height = driver.execute_script("return window.innerHeight;")
                    screen_resolution = f"{width}x{height}"
                    print(f"[📱] Detected screen resolution: {screen_resolution}")
                except Exception as res_error:
                    print(f"[⚠️] Could not get screen resolution: {res_error}")
                    # Fallback to device-based resolution
                    if device_name == "desktop":
                        screen_resolution = "1920x1080"  # Default desktop resolution
                    elif "iPhone" in device_name:
                        screen_resolution = "375x812"  # iPhone X resolution
                    elif "iPad" in device_name:
                        screen_resolution = "1024x1366"  # iPad Pro resolution
                    elif "Pixel" in device_name:
                        screen_resolution = "411x823"  # Pixel 4 resolution
                    elif "Samsung Galaxy" in device_name:
                        if "S21" in device_name or "S20" in device_name:
                            screen_resolution = "360x800"
                        elif "S10" in device_name:
                            screen_resolution = "360x640"
                        else:
                            screen_resolution = "360x800"  # Default Samsung resolution
                    else:
                        screen_resolution = "unknown"

                # Enhanced device name detection if still unknown
                if device_name == "unknown":
                    try:
                        # Try to detect device type from user agent or viewport
                        user_agent = driver.execute_script(
                            "return navigator.userAgent;"
                        )
                        viewport_width = driver.execute_script(
                            "return window.innerWidth;"
                        )

                        if "iPhone" in user_agent or viewport_width <= 414:
                            device_name = "iPhone"
                        elif "iPad" in user_agent or (
                            viewport_width > 414 and viewport_width <= 1024
                        ):
                            device_name = "iPad"
                        elif "Android" in user_agent or "Mobile" in user_agent:
                            device_name = "Android"
                        elif viewport_width > 1024:
                            device_name = "Desktop"
                        else:
                            device_name = "Mobile"

                        print(f"[📱] Detected device type: {device_name}")
                    except Exception as device_error:
                        print(f"[⚠️] Could not detect device type: {device_error}")
                        device_name = "unknown"

    except Exception as e:
        print(f"[⚠️] Error getting device information: {e}")
        # Fallback device detection
        if hasattr(request, "param") and request.param:
            device_name = request.param
        else:
            device_name = "unknown"

        # Fallback resolution based on device name
        if device_name == "desktop":
            screen_resolution = "1920x1080"
        elif "iPhone" in device_name:
            screen_resolution = "375x812"
        elif "iPad" in device_name:
            screen_resolution = "1024x1366"
        elif "Pixel" in device_name:
            screen_resolution = "411x823"
        elif "Samsung Galaxy" in device_name:
            if "S21" in device_name or "S20" in device_name:
                screen_resolution = "360x800"
            elif "S10" in device_name:
                screen_resolution = "360x640"
            else:
                screen_resolution = "360x800"  # Default Samsung resolution
        else:
            screen_resolution = "unknown"

    # Capture the result after test execution
    if hasattr(request.node, "rep_call"):
        if request.node.rep_call.passed:
            status = "PASSED"
            error_message = None
        elif request.node.rep_call.failed:
            status = "FAILED"
            error_message = (
                str(request.node.rep_call.longrepr)
                if hasattr(request.node.rep_call, "longrepr")
                else "Test failed"
            )
        else:
            status = "ERROR"
            error_message = "Unknown error"
    else:
        # Fallback for cases where rep_call is not available
        status = "ERROR"
        error_message = "Result capture failed"

    # Capture screenshot and generate error link if test failed
    error_link = None
    if (
        status in ["FAILED", "ERROR"]
        and hasattr(request, "funcargs")
        and "driver" in request.funcargs
    ):
        driver = request.funcargs["driver"]
        if driver:
            try:
                # Capture screenshot for failed test
                _, error_link = screenshot_manager.capture_screenshot(
                    driver, test_name, stage=getattr(request, "param", ""), error=True
                )

                # Also capture page source for debugging
                screenshot_manager.capture_page_source(
                    driver, test_name, stage=getattr(request, "param", ""), error=True
                )

                print(f"[🔗] Error link generated: {error_link}")
            except Exception as screenshot_error:
                print(f"[⚠️] Failed to capture error screenshot: {screenshot_error}")

    # Clean test case name by removing device information
    import re

    cleaned_test_name = re.sub(r"\[.*?\]", "", test_name).strip(" _")

    # Store result in database
    try:
        print(
            f"[💾] Storing test result: {cleaned_test_name} - {status} - Device: {device_name} - Resolution: {screen_resolution}"
        )
        helper = get_db_helper()
        helper.store_test_result_in_tables(
            cleaned_test_name,
            module_name,
            status,
            error_message,
            None,  # test_data
            total_time_duration,
            device_name,
            screen_resolution,
            error_link,
        )
    except Exception as e:
        print(f"❌ Failed to store test result in database: {e}")
        print(f"Error details: {type(e).__name__} - {e}")
        import traceback

        traceback.print_exc()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    outcome = yield
    rep = outcome.get_result()

    # Set the result for the fixture to access
    item.rep_call = rep


# Function to get device list based on environment variable
def get_device_list():
    """Get list of devices to test based on environment variable"""
    # Check if mobile test is specifically requested
    if os.getenv("MOBILE_TEST", "false").lower() == "true":
        return ["iPhone X"]  # Force mobile testing

    devices_env = os.getenv(
        "TEST_DEVICES", "desktop,iPad Pro,iPhone X,Samsung Galaxy S21"
    )
    return [device.strip() for device in devices_env.split(",")]


@pytest.fixture(params=get_device_list())
def driver(request):
    device = request.param

    # Store device information in global variable
    global _device_info  # noqa: F824
    _device_info["name"] = device

    chrome_options = Options()

    if HEADLESS:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        print("✅ Running in headless mode")
    else:
        print("🚫 Headless mode disabled")

    if device == "desktop":
        print("[🖥️] Running on desktop")
        chrome_options.add_argument("--start-maximized")
        _device_info["resolution"] = "1920x1080"  # Default desktop resolution
    else:
        # Use valid Chrome device names that are known to work
        device_mapping = {
            "iPhone X": "iPhone X",
            "iPad Pro": "iPad Pro",
            "Pixel 4": "Pixel 4",
        }

        if device in device_mapping:
            mobile_emulation = {"deviceName": device_mapping[device]}
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            print(f"[📱] Running on mobile: {device}")

            # Set default resolutions for known devices
            if device == "iPhone X":
                _device_info["resolution"] = "375x812"
            elif device == "iPad Pro":
                _device_info["resolution"] = "1024x1366"
            elif device == "Pixel 4":
                _device_info["resolution"] = "411x823"
        elif "Samsung Galaxy" in device:
            # Use custom device metrics for Samsung devices with proper Android user agent
            if "S21" in device:
                mobile_emulation = {
                    "deviceMetrics": {"width": 360, "height": 800, "pixelRatio": 3.0},
                    "userAgent": "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                }
                _device_info["resolution"] = "360x800"
            elif "S20" in device:
                mobile_emulation = {
                    "deviceMetrics": {"width": 360, "height": 800, "pixelRatio": 3.0},
                    "userAgent": "Mozilla/5.0 (Linux; Android 11; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                }
                _device_info["resolution"] = "360x800"
            elif "S10" in device:
                mobile_emulation = {
                    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
                    "userAgent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                }
                _device_info["resolution"] = "360x640"
            else:
                # Generic Samsung device
                mobile_emulation = {
                    "deviceMetrics": {"width": 360, "height": 800, "pixelRatio": 3.0},
                    "userAgent": "Mozilla/5.0 (Linux; Android 12; Samsung Galaxy) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                }
                _device_info["resolution"] = "360x800"

            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            print(f"[📱] Running on Samsung Android: {device}")
        else:
            # Fallback to custom dimensions for unknown devices
            mobile_emulation = {
                "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            print(f"[📱] Running on mobile with custom dimensions: {device}")
            _device_info["resolution"] = "375x812"  # Default mobile resolution

    # Add additional options for better stability
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # Disable user data directory completely for CI compatibility
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    chrome_options.add_argument("--disable-features=TranslateUI")
    chrome_options.add_argument("--disable-ipc-flooding-protection")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    # Execute script to remove webdriver property
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    # Update resolution with actual values from driver
    try:
        width = driver.execute_script("return window.innerWidth;")
        height = driver.execute_script("return window.innerHeight;")
        _device_info["resolution"] = f"{width}x{height}"
        print(
            f"[📱] Updated device info - Name: {_device_info['name']}, Resolution: {_device_info['resolution']}"
        )
    except Exception as e:
        print(f"[⚠️] Could not get actual resolution: {e}")

    yield driver
    driver.quit()

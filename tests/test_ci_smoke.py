import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_page_load_smoke(driver):
    """Simple smoke test to verify page loads in CI"""
    try:
        print(f"[🚀] Starting smoke test on device: {driver.execute_script('return window.innerWidth')}x{driver.execute_script('return window.innerHeight')}")
        
        # Navigate to a simple page (GitHub or similar)
        driver.get("https://www.google.com")
        
        # Wait for page to load (short timeout)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        # Verify page title
        assert "Google" in driver.title
        
        print(f"[✅] Smoke test passed on device")
        
    except Exception as e:
        print(f"[❌] Smoke test failed: {e}")
        raise

def test_selenium_basic(driver):
    """Basic Selenium functionality test"""
    try:
        print(f"[🧪] Testing basic Selenium functionality")
        
        # Test basic navigation
        driver.get("https://httpbin.org/html")
        
        # Test element finding
        element = driver.find_element(By.TAG_NAME, "h1")
        assert element.text == "Herman Melville - Moby-Dick"
        
        print(f"[✅] Basic Selenium test passed")
        
    except Exception as e:
        print(f"[❌] Basic Selenium test failed: {e}")
        raise 
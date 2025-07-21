#!/usr/bin/env python3
"""
Script to get valid Chrome device names for mobile emulation
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json

def get_valid_devices():
    """Get list of valid Chrome device names"""
    try:
        # Create Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Create driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Get device list using CDP
        devices = driver.execute_cdp_cmd('Emulation.getDeviceMetricsOverride', {})
        
        # Get available devices
        available_devices = driver.execute_cdp_cmd('Emulation.getDeviceMetricsOverride', {})
        
        print("Available Chrome devices:")
        print("=" * 50)
        
        # Try to get device list from Chrome DevTools
        try:
            # This is a workaround to get device names
            # Chrome doesn't expose device names directly, so we'll use common ones
            common_devices = [
                "iPhone 12 Pro",
                "iPhone 12 Pro Max", 
                "iPhone 12",
                "iPhone 12 Mini",
                "iPhone 11 Pro",
                "iPhone 11 Pro Max",
                "iPhone 11",
                "iPhone XR",
                "iPhone XS",
                "iPhone XS Max",
                "iPhone X",
                "iPhone 8",
                "iPhone 8 Plus",
                "iPhone 7",
                "iPhone 7 Plus",
                "iPhone SE",
                "iPad Pro",
                "iPad",
                "iPad Air",
                "iPad Mini",
                "Galaxy S20",
                "Galaxy S20 Plus",
                "Galaxy S20 Ultra",
                "Galaxy S10",
                "Galaxy S10 Plus",
                "Galaxy S9",
                "Galaxy S9 Plus",
                "Galaxy Note 20",
                "Galaxy Note 20 Ultra",
                "Pixel 5",
                "Pixel 4",
                "Pixel 4 XL",
                "Pixel 3",
                "Pixel 3 XL",
                "Nexus 5X",
                "Nexus 6P"
            ]
            
            print("Common Chrome device names that should work:")
            for device in common_devices:
                print(f"  - {device}")
                
        except Exception as e:
            print(f"Error getting device list: {e}")
        
        driver.quit()
        
    except Exception as e:
        print(f"Error: {e}")

def test_device_name(device_name):
    """Test if a specific device name is valid"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Try to set mobile emulation
        mobile_emulation = {"deviceName": device_name}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # Try to create driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get("https://www.google.com")
        print(f"✅ {device_name} - VALID")
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ {device_name} - INVALID: {str(e)[:100]}...")
        return False

if __name__ == "__main__":
    print("🔍 Getting valid Chrome device names...")
    get_valid_devices()
    
    print("\n🧪 Testing common device names...")
    print("=" * 50)
    
    test_devices = [
        "iPhone 12 Pro",
        "iPhone 12", 
        "iPhone 11",
        "iPhone X",
        "iPad Pro",
        "iPad",
        "Galaxy S20",
        "Galaxy S10",
        "Pixel 5",
        "Pixel 4"
    ]
    
    valid_devices = []
    for device in test_devices:
        if test_device_name(device):
            valid_devices.append(device)
    
    print(f"\n✅ Valid devices found: {len(valid_devices)}")
    print("=" * 50)
    for device in valid_devices:
        print(f"  - {device}") 
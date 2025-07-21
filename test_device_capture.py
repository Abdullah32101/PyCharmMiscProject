#!/usr/bin/env python3
"""
Test script to verify device information capture
"""

import pytest
import sys
import os

def test_device_info_capture(driver, device_info):
    """Simple test to verify device information is captured"""
    print(f"[🧪] Running test on device: {device_info['name']}")
    print(f"[🧪] Screen resolution: {device_info['resolution']}")
    
    # Simple test - just navigate to a page
    driver.get("https://www.google.com")
    
    # Verify device info is set
    assert device_info['name'] != "unknown", f"Device name should not be unknown, got: {device_info['name']}"
    assert device_info['resolution'] != "unknown", f"Resolution should not be unknown, got: {device_info['resolution']}"
    
    print(f"[✅] Test passed - Device: {device_info['name']}, Resolution: {device_info['resolution']}")

if __name__ == "__main__":
    print("=" * 60)
    print("DEVICE INFORMATION CAPTURE TEST")
    print("=" * 60)
    
    # Set environment variable to force mobile testing
    os.environ["MOBILE_TEST"] = "true"
    os.environ["TEST_DEVICES"] = "iPhone X,iPad Pro,desktop"
    
    # Run the test
    pytest_args = [
        __file__,
        "-v",
        "--tb=short",
        "--capture=no",
        "-s"
    ]
    
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print("\n[🎉] Device information capture test passed!")
        print("[💾] Check the database for device and resolution information.")
    else:
        print(f"\n[❌] Device information capture test failed with exit code: {exit_code}")
    
    sys.exit(exit_code) 
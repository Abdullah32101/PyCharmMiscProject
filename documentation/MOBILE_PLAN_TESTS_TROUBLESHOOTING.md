# Mobile Plan Tests Troubleshooting Guide

## Overview
This guide helps diagnose and fix issues with mobile versions of monthly and onetime plan tests, and addresses database device name and resolution problems.

## Issues Addressed

### 1. **Mobile Version Not Running**
**Problem**: Monthly and onetime plan tests were not properly handling mobile devices.

**Root Causes**:
- No mobile-specific scrolling behavior
- Missing mobile detection and handling
- Inadequate field filling for mobile devices
- No JavaScript fallbacks for mobile interactions

**Solutions Implemented**:
- Added mobile detection: `is_mobile = self.driver.execute_script("return window.innerWidth < 768;")`
- Enhanced scrolling with smooth behavior for mobile: `scrollIntoView({block: 'center', behavior: 'smooth'})`
- Mobile-specific field filling with verification
- JavaScript fallbacks for all interactions
- Enhanced error handling and logging

### 2. **Database Device Name and Resolution Issues**
**Problem**: Device names and screen resolutions were not being properly captured and stored in the database.

**Root Causes**:
- Device name not being passed correctly from conftest.py
- Screen resolution detection failing
- No fallback mechanisms for device detection

**Solutions Implemented**:
- Enhanced device name capture from parametrized fixtures
- Real-time screen resolution detection from driver
- Fallback device detection using user agent and viewport
- Improved error handling and logging for device information

## Enhanced Mobile Features

### 1. **Mobile-Specific Scrolling**
```python
if is_mobile:
    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
    time.sleep(1)  # Wait for scroll to complete
else:
    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.5)
```

### 2. **Enhanced Field Filling for Mobile**
```python
def _fill_card_field_mobile(self, wait, element_id, value, delay_per_key=False):
    """Enhanced field filling for mobile devices"""
    try:
        field = wait.until(EC.visibility_of_element_located((By.ID, element_id)))
        
        # Scroll to field with smooth behavior
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", field)
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
            # Try JavaScript fallback
            self.driver.execute_script(f"""
                let field = document.getElementById('{element_id}');
                if (field) {{
                    field.value = '{value}';
                    field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            """)
```

### 3. **Enhanced Device Detection**
```python
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
        screen_resolution = "1920x1080"
    elif "iPhone" in device_name:
        screen_resolution = "375x812"
    elif "iPad" in device_name:
        screen_resolution = "1024x1366"
```

## Test Runners Created

### 1. **Monthly Plan Test Runner** (`run_monthly_test.py`)
```bash
# Run all devices
python run_monthly_test.py

# Run mobile devices only
python run_monthly_test.py mobile
```

### 2. **Onetime Plan Test Runner** (`run_onetime_test.py`)
```bash
# Run all devices
python run_onetime_test.py

# Run mobile devices only
python run_onetime_test.py mobile
```

### 3. **Comprehensive Plan Test Runner** (`run_all_plan_tests.py`)
```bash
# Run all plan tests on all devices
python run_all_plan_tests.py

# Run all plan tests on mobile devices only
python run_all_plan_tests.py mobile

# Run specific plan tests
python run_all_plan_tests.py monthly
python run_all_plan_tests.py onetime
python run_all_plan_tests.py sixmonth
```

## Mobile-Specific Improvements

### 1. **Button Clicking**
- Enhanced scrolling with smooth behavior
- JavaScript fallback for failed clicks
- Mobile-specific wait times
- Better error handling and logging

### 2. **Form Field Interaction**
- Mobile-specific field filling with verification
- Character-by-character entry for sensitive fields
- JavaScript fallbacks with proper event dispatching
- Field value verification after entry

### 3. **Payment Toggle**
- Multiple selector strategies
- Mobile-specific scrolling
- JavaScript fallback for radio button selection
- Enhanced error handling

### 4. **Card Details Entry**
- Mobile-specific scrolling between fields
- Enhanced JavaScript fallback
- Field value verification
- Better error handling and recovery

## Database Integration

### 1. **Device Name Storage**
- Proper device name capture from parametrized fixtures
- Fallback device detection using user agent
- Enhanced logging for device information

### 2. **Screen Resolution Storage**
- Real-time resolution detection from driver
- Fallback resolution based on device type
- Proper error handling for resolution detection

### 3. **Test Result Storage**
- Automatic storage in appropriate tables based on test type
- Device and resolution information included
- Enhanced error handling and logging

## Debugging Features

### 1. **Enhanced Logging**
- Device type detection logging
- Screen resolution detection logging
- Step-by-step progress logging
- Error details with context

### 2. **Screenshot Capture**
- Automatic screenshots on test failure
- Screenshots saved with timestamps
- Page source saving for debugging

### 3. **HTML Reports**
- Comprehensive HTML reports for each test run
- Self-contained reports with all information
- Mobile-specific report naming

## Common Mobile Issues and Solutions

### 1. **Element Not Interactable**
**Solution**: Enhanced scrolling with smooth behavior and JavaScript fallbacks

### 2. **Field Values Not Entering**
**Solution**: Mobile-specific field filling with verification and JavaScript fallbacks

### 3. **Button Clicks Not Working**
**Solution**: Multiple click strategies with JavaScript fallbacks

### 4. **Screen Resolution Not Detected**
**Solution**: Real-time detection with fallback to device-based resolution

### 5. **Device Name Not Stored**
**Solution**: Enhanced device detection with multiple fallback mechanisms

## Testing Different Devices

The enhanced system supports multiple devices:
- **Desktop**: 1920x1080 resolution
- **iPhone X**: 375x812 resolution
- **iPad Pro**: 1024x1366 resolution
- **Pixel 4**: 411x823 resolution

## Performance Optimizations

### 1. **Mobile-Specific Wait Times**
- Longer wait times for mobile devices
- Smooth scrolling behavior
- Enhanced field verification

### 2. **JavaScript Fallbacks**
- Proper event dispatching
- Field value verification
- Enhanced error recovery

### 3. **Database Optimization**
- Efficient device information capture
- Proper error handling
- Enhanced logging

## Monitoring and Reporting

### 1. **Real-time Logging**
- Device type detection
- Screen resolution detection
- Step-by-step progress
- Error details with context

### 2. **Database Reports**
- Device and resolution information stored
- Test results with device context
- Enhanced error tracking

### 3. **HTML Reports**
- Comprehensive test reports
- Device information included
- Screenshot integration

## Getting Help

If issues persist:
1. Run the mobile-specific test runners
2. Check all generated screenshots and HTML files
3. Review console logs for specific error messages
4. Check database for device and resolution information
5. Compare with desktop test results

## Test Data Reference

The tests use these constants:
- **Card Number**: 4242424242424242 (test card)
- **Expiry**: 03/2032
- **CVC**: 123
- **Email**: Auto-generated with timestamp
- **Password**: Zeeshan@9671
- **University**: Punjab University Lahore

Make sure these test credentials are still valid for the staging environment. 
# One-Time Plan Test Troubleshooting Guide

## Overview
This guide helps diagnose and fix issues with the `test_onetime_plan.py` test.

## Common Failure Points

### 1. **One-Time Plan Button Not Found**
**Symptoms:**
- Error: "No one-time plan button found after all attempts"
- Screenshot: `one_time_plan_button_not_found_*.png`

**Possible Causes:**
- Button text has changed on the website
- Button is in an iframe
- Button is dynamically loaded
- Button has different CSS classes or IDs

**Solutions:**
- Check the generated HTML file: `one_time_plan_page_source_*.html`
- Look for buttons with text containing: "Buy", "Solution", "One", "Single", "Purchase"
- Update selectors in `click_one_time_plan_button()` method

### 2. **Payment Toggle Not Found**
**Symptoms:**
- Warning: "Could not find payment toggle, continuing without it..."
- Payment form doesn't appear

**Possible Causes:**
- Radio button ID has changed from 'radio7'
- Payment method selection is handled differently
- Form is already pre-selected

**Solutions:**
- Check if payment form appears without toggle
- Update radio button selectors
- Add more payment method selectors

### 3. **Confirmation Message Not Detected**
**Symptoms:**
- Warning: "No confirmation message found"
- Test appears to hang

**Possible Causes:**
- Confirmation page has different CSS classes
- Page redirects to different URL
- Success/error messages have different structure

**Solutions:**
- Check the final screenshot: `onetime_plan_final_*.png`
- Look at page title and URL changes
- Update confirmation selectors

### 4. **Card Details Entry Fails**
**Symptoms:**
- Error: "Error entering card details"
- Form fields not found

**Possible Causes:**
- Form field IDs have changed
- Form is in an iframe
- Form validation errors

**Solutions:**
- Check if form fields exist with different IDs
- Verify iframe handling
- Check for validation error messages

## Debugging Steps

### Step 1: Run the Enhanced Test
```bash
python run_onetime_test.py
```

### Step 2: Check Generated Files
After test run, look for:
- `onetime_plan_final_primary_*.png` - Final state screenshot
- `onetime_plan_final_secondary_*.png` - Final state screenshot
- `onetime_plan_error_primary_*.png` - Error screenshot
- `onetime_plan_error_secondary_*.png` - Error screenshot
- `onetime_plan_error_primary_*.html` - Page source at error
- `onetime_plan_error_secondary_*.html` - Page source at error

### Step 3: Analyze Screenshots
1. Open the error screenshots
2. Look for:
   - Missing buttons
   - Error messages
   - Form validation errors
   - Page layout issues

### Step 4: Check Page Source
1. Open the HTML files
2. Search for:
   - Button elements with relevant text
   - Form field IDs
   - Error message elements
   - Confirmation message elements

## Quick Fixes

### If Button Text Changed:
Update the selectors in both page objects:
```python
selectors = [
    "//button[normalize-space()='NEW_BUTTON_TEXT']",
    "//button[contains(text(), 'NEW_BUTTON_TEXT')]",
    # Add more variations
]
```

### If Payment Toggle Changed:
Update the toggle selectors:
```python
toggle_selectors = [
    "//label[@for='NEW_RADIO_ID']",
    "//input[@id='NEW_RADIO_ID']",
    # Add more variations
]
```

### If Confirmation Selectors Changed:
Update the confirmation check:
```python
confirmation_selectors = [
    ".NEW_SUCCESS_CLASS",
    ".NEW_ERROR_CLASS",
    # Add more variations
]
```

## Environment Issues

### Chrome Driver Issues:
- Update Chrome browser
- Update ChromeDriver
- Check for compatibility issues

### Network Issues:
- Check internet connection
- Verify staging site is accessible
- Check for rate limiting

### Timing Issues:
- Increase wait times in the test
- Add more explicit waits
- Check for slow page loading

## Getting Help

If the issue persists:
1. Save all generated files (screenshots, HTML, logs)
2. Note the exact error messages
3. Check if the issue occurs on both primary and secondary stages
4. Compare with working tests (monthly, six-month, popular plans)

## Test Data

The test uses these constants:
- **Card Number**: 4242424242424242 (test card)
- **Expiry**: 03/2032
- **CVC**: 123
- **Email**: Auto-generated with timestamp
- **Password**: Zeeshan@9671
- **University**: Punjab University Lahore

Make sure these test credentials are still valid for the staging environment. 
# Mobile Book Purchase Test Troubleshooting Guide

## Overview
This guide helps diagnose and fix issues with the mobile version of the book purchase test that occur during billing details entry.

## Common Mobile-Specific Issues

### 1. **Form Fields Not Visible/Clickable**
**Symptoms:**
- Error: "Element not interactable"
- Fields appear but cannot be filled
- Scrolling issues on mobile

**Causes:**
- Mobile viewport issues
- Form fields hidden behind other elements
- Touch interaction problems

**Solutions:**
- Added mobile-specific scrolling with `scrollIntoView({block: 'center', behavior: 'smooth'})`
- Added delays between field interactions
- Enhanced JavaScript fallback for field filling

### 2. **Country/State Selection Issues**
**Symptoms:**
- Country dropdown not populating
- State dropdown remains empty after country selection
- JavaScript errors in console

**Causes:**
- AJAX loading delays on mobile
- Different dropdown behavior on mobile
- Timing issues with dynamic content

**Solutions:**
- Added multiple selection methods (value, text, JavaScript)
- Increased wait times for mobile (2 seconds vs 1 second)
- Added verification that options are loaded before selection

### 3. **Card Details Entry Problems**
**Symptoms:**
- Card number not entering correctly
- Form validation errors
- Fields clearing unexpectedly

**Causes:**
- Mobile keyboard interference
- Form validation triggering too early
- Touch input issues

**Solutions:**
- Added character-by-character entry for card number
- Enhanced JavaScript fallback with proper event dispatching
- Added field value verification after entry

### 4. **Payment Toggle Issues**
**Symptoms:**
- Payment method not switching to credit card
- Radio button not clickable
- Form not appearing after toggle

**Causes:**
- Touch target too small on mobile
- JavaScript event handling differences
- Form loading delays

**Solutions:**
- Added mobile-specific click handling
- Increased wait times for form appearance
- Added scrolling to payment section

## Debugging Steps

### Step 1: Run Mobile-Specific Test
```bash
python run_mobile_book_test.py
```

### Step 2: Check Generated Files
After test run, look for:
- `mobile_book_test_failure.png` - Screenshot at failure point
- `mobile_book_test_failure.html` - Page source at failure
- `card_details_filled.png` - Screenshot after card entry
- `book_purchase_error_*.png` - Error screenshots

### Step 3: Analyze Console Logs
Look for these specific log messages:
- `[📱] Filling billing details on Mobile`
- `[🌍] Country selected by value (Mobile)`
- `[🏙️] State selected by text (Mobile)`
- `[💳] Entering card details on Mobile`
- `[✅] Card details filled successfully`

### Step 4: Check Form Field Values
Verify that all fields have correct values:
- `fname`: "Zeeshan"
- `lname`: "Ali"
- `country_name_p`: "177" (Pakistan)
- `state`: Should contain "Punjab"
- `city`: "Lahore"
- `post_code`: "54000"
- `address`: "House No 11, sector A2, Gulberg"
- `phone_number`: "032064970863333"

## Mobile-Specific Fixes Applied

### 1. Enhanced `fill_billing_details()` Method
- Added mobile detection and specific handling
- Multiple fallback methods for country/state selection
- Field value verification after entry
- Better error handling and logging

### 2. Improved `_fill_input()` Method
- Mobile-specific scrolling behavior
- Value verification after entry
- JavaScript fallback for failed interactions
- Better timing and delays

### 3. Enhanced `enter_card_details()` Method
- Mobile-specific scrolling between fields
- Enhanced JavaScript fallback
- Field value verification
- Better error handling

### 4. Test Case Improvements
- Mobile-specific wait times
- Additional scrolling and stabilization
- Better error reporting
- Page source saving for debugging

## Testing Different Mobile Devices

The test supports multiple mobile devices:
- iPhone X
- iPad Pro
- Pixel 4

To test specific devices, modify the `conftest.py` file or use the mobile test runner.

## Common Error Messages and Solutions

### "Element not interactable"
**Solution:** Added scrolling and delays before interaction

### "TimeoutException"
**Solution:** Increased wait times for mobile devices

### "NoSuchElementException"
**Solution:** Added JavaScript fallback for element interaction

### "StaleElementReferenceException"
**Solution:** Added element refresh and retry logic

## Performance Tips for Mobile Testing

1. **Use Headless Mode for CI/CD:**
   ```bash
   HEADLESS=true python run_mobile_book_test.py
   ```

2. **Reduce Wait Times for Faster Testing:**
   - Modify time.sleep() values in the code
   - Use shorter WebDriverWait timeouts

3. **Enable Screenshots Only on Failure:**
   - Screenshots are automatically saved on test failure
   - Remove screenshot calls for faster execution

## Monitoring and Logging

The enhanced code includes comprehensive logging:
- Device type detection
- Step-by-step progress
- Error details with context
- Field value verification results

## Getting Help

If issues persist:
1. Run the mobile-specific test runner
2. Check all generated screenshots and HTML files
3. Review console logs for specific error messages
4. Compare with desktop test results
5. Check if the issue is device-specific

## Test Data Reference

The test uses these constants from `constants.py`:
- **Country**: "Pakistan" (value: "177")
- **State**: "Punjab"
- **City**: "Lahore"
- **Postal Code**: "54000"
- **Address**: "House No 11, sector A2, Gulberg"
- **Phone**: "032064970863333"
- **Card Number**: "4242424242424242"
- **Card Holder**: "Zeeshan Ali"
- **CVC**: "123"
- **Expiry**: "03/2032"

Make sure these values are still valid for the staging environment. 
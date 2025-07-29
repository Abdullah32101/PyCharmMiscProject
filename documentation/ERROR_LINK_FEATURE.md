# Error Link Feature Documentation

## Overview

The Error Link Feature automatically captures screenshots when tests fail and stores URLs in the database that allow you to view the affected screen. When you open the error link, you can see exactly what the screen looked like when the test failed.

## Features

### 1. **Automatic Screenshot Capture**
- Screenshots are automatically captured when tests fail
- Screenshots are saved in the `screenshots/` directory
- Each screenshot has a unique timestamp and descriptive filename

### 2. **Error Link Generation**
- File:// URLs are generated for each screenshot
- Links are stored in the database `error_link` column
- Links can be opened in any web browser to view the screenshot

### 3. **Page Source Capture**
- HTML page source is also captured for failed tests
- Page source files are saved alongside screenshots
- Useful for debugging element selection issues

### 4. **Database Integration**
- Error links are automatically stored in the database
- Links are associated with specific test results
- Easy to query and retrieve error screenshots

## Database Schema Changes

### New Column Added
```sql
ALTER TABLE test_results 
ADD COLUMN error_link VARCHAR(500) NULL 
COMMENT 'URL link to screenshot showing affected screen';
```

### Updated Table Structure
```sql
CREATE TABLE test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_case_name VARCHAR(255) NOT NULL,
    module_name VARCHAR(255) NOT NULL,
    test_status ENUM('PASSED', 'FAILED', 'SKIPPED', 'ERROR') NOT NULL,
    test_datetime DATETIME NOT NULL,
    error_message TEXT,
    error_summary VARCHAR(255),
    total_time_duration DECIMAL(10,3) NULL,
    device_name VARCHAR(50) NULL,
    screen_resolution VARCHAR(50) NULL,
    error_link VARCHAR(500) NULL,  -- NEW COLUMN
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Implementation Details

### 1. Screenshot Manager (`screenshot_utils.py`)
```python
from screenshot_utils import screenshot_manager

# Capture screenshot and get error link
file_path, error_link = screenshot_manager.capture_screenshot(
    driver, 
    test_name, 
    stage="primary", 
    error=True
)
```

### 2. Database Helper Updates (`db/db_helper.py`)
```python
# Store test result with error link
db_helper.store_test_result_in_tables(
    test_name,
    module_name,
    status,
    error_message,
    test_data,
    total_time_duration,
    device_name,
    screen_resolution,
    error_link  # NEW PARAMETER
)
```

### 3. Automatic Capture (`conftest.py`)
```python
# Screenshots are automatically captured for failed tests
if status in ["FAILED", "ERROR"]:
    _, error_link = screenshot_manager.capture_screenshot(
        driver, 
        test_name, 
        stage=getattr(request, 'param', ''), 
        error=True
    )
```

## File Structure

```
project/
├── screenshots/                    # Screenshot directory
│   ├── test_name_error_stage_timestamp.png
│   ├── test_name_error_stage_timestamp.html
│   └── ...
├── screenshot_utils.py            # Screenshot management utility
├── add_error_link_column.py       # Database migration script
├── test_error_link_feature.py     # Feature test script
└── ERROR_LINK_FEATURE.md          # This documentation
```

## Usage Examples

### 1. Running Tests with Error Links
```bash
# Run tests normally - error links will be captured automatically
python -m pytest tests/test_monthly_plan.py

# Run with headless mode
HEADLESS=true python -m pytest tests/test_monthly_plan.py
```

### 2. Viewing Error Screenshots
```sql
-- Query failed tests with error links
SELECT test_case_name, test_status, error_link 
FROM test_results 
WHERE test_status IN ('FAILED', 'ERROR') 
AND error_link IS NOT NULL;
```

### 3. Opening Error Links
```python
# Error links are file:// URLs that can be opened in browsers
# Example: file:///path/to/project/screenshots/test_error_primary_1234567890.png
```

## Screenshot Naming Convention

### Format
```
{test_name}_{type}_{stage}_{timestamp}.{extension}
```

### Examples
- `test_monthly_plan_error_primary_1752836753.png`
- `test_onetime_plan_final_secondary_1752837473.png`
- `test_book_purchase_error_1752837592.html`

### Components
- `test_name`: Name of the test function
- `type`: `error` (for failed tests) or `final` (for completed tests)
- `stage`: Test stage (primary, secondary, etc.)
- `timestamp`: Unix timestamp for uniqueness
- `extension`: `.png` for screenshots, `.html` for page source

## Error Link Format

### File URLs
```
file:///absolute/path/to/screenshot.png
```

### Example
```
file:///c:/Users/Admin/PyCharmMiscProject/screenshots/test_monthly_plan_error_primary_1752836753.png
```

## Database Migration

### Adding the New Column
```bash
# Run the migration script
python add_error_link_column.py
```

### Verification
```sql
-- Check if column was added
DESCRIBE test_results;

-- Verify column exists
SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'test_results' 
AND COLUMN_NAME = 'error_link';
```

## Testing the Feature

### Run Feature Test
```bash
python test_error_link_feature.py
```

### Expected Output
```
🧪 Testing Error Link Feature
==================================================
[🧪] Original: test<>:"/\|?*file.png
[🧪] Sanitized: test______file.png
[🧪] Test path: screenshots/test.png
[🧪] Generated URL: file:///path/to/screenshots/test.png
[✅] Screenshot manager tests passed
[📸] Screenshot captured: screenshots/test_error_link_feature_error_test_1234567890.png
[🔗] Error link: file:///path/to/screenshots/test_error_link_feature_error_test_1234567890.png
[✅] Test result stored in database with error link
[🔍] Stored error link: file:///path/to/screenshots/test_error_link_feature_error_test_1234567890.png
[✅] Error link verification passed

🎉 All tests passed!
```

## Benefits

### 1. **Visual Debugging**
- See exactly what the screen looked like when the test failed
- Identify UI issues, element positioning problems
- Debug responsive design issues on different devices

### 2. **Faster Troubleshooting**
- No need to reproduce the exact test conditions
- Immediate visual feedback on test failures
- Historical record of test failures

### 3. **Better Documentation**
- Visual evidence of test failures
- Screenshots can be shared with team members
- Useful for bug reports and issue tracking

### 4. **Device-Specific Debugging**
- Screenshots show the exact device and resolution
- Helpful for mobile testing issues
- Compare behavior across different devices

## Troubleshooting

### Common Issues

#### 1. Screenshots Not Being Captured
- Check if the test is actually failing
- Verify the driver is available in the test context
- Check file permissions for the screenshots directory

#### 2. Error Links Not Working
- Ensure the file path is correct
- Check if the screenshot file exists
- Verify the file:// URL format

#### 3. Database Column Not Added
- Run the migration script: `python add_error_link_column.py`
- Check database permissions
- Verify the table structure

#### 4. Permission Errors
- Ensure write permissions to the screenshots directory
- Check if the directory exists and is writable
- Verify Chrome driver permissions

### Debug Commands
```bash
# Check if screenshots directory exists
ls -la screenshots/

# Verify database column
python add_error_link_column.py

# Test the feature
python test_error_link_feature.py

# Check recent test results
python view_test_results.py
```

## Future Enhancements

### Potential Improvements
1. **Web-based Screenshot Viewer**: Create a web interface to view screenshots
2. **Screenshot Comparison**: Compare screenshots between test runs
3. **Automatic Cleanup**: Implement automatic cleanup of old screenshots
4. **Cloud Storage**: Store screenshots in cloud storage for team access
5. **Screenshot Annotations**: Add ability to annotate screenshots
6. **Video Recording**: Record video of test execution for complex failures

### Configuration Options
```python
# Future configuration options
SCREENSHOT_CONFIG = {
    'enabled': True,
    'max_screenshots': 100,
    'cleanup_days': 7,
    'cloud_storage': False,
    'video_recording': False,
    'annotations': False
}
```

## Support

For issues or questions about the Error Link Feature:
1. Check this documentation
2. Run the test script: `python test_error_link_feature.py`
3. Review the troubleshooting section
4. Check the database migration: `python add_error_link_column.py` 
# Database Integration for Test Results

This project now includes automatic database integration to store all test case results. Every test execution will automatically capture and store the results in a MySQL database.

## Database Schema

The system creates a `test_results` table with the following structure:

```sql
CREATE TABLE test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_case_name VARCHAR(255) NOT NULL,
    module_name VARCHAR(255) NOT NULL,
    test_status ENUM('PASSED', 'FAILED', 'SKIPPED', 'ERROR') NOT NULL,
    test_datetime DATETIME NOT NULL,
    error_message TEXT,
    error_summary VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Setup Instructions

### 1. Database Configuration

Your database configuration is already set up in `db/db_config.py`:

```python
DB_CONFIG = {
    'host': 'solutionsole.com',
    'user': 'root',
    'password': 'SolutionInn321',
    'database': 'test'
}
```

### 2. Initialize Database

Run the database initialization script to create the required table:

```bash
python init_database.py
```

This will:
- Connect to your database
- Create the `test_results` table if it doesn't exist
- Test the connection
- Display current test record count

### 3. Run Tests

Your tests will now automatically store results in the database. No changes needed to your existing test files!

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_book_purchase.py

# Run with specific device
pytest tests/test_book_purchase.py::test_book_page_load_and_click -k "desktop"
```

## Viewing Test Results

### 1. Command Line Viewer

Use the `view_test_results.py` script to view and analyze test results:

```bash
# View recent test results and statistics
python view_test_results.py

# View only failed tests
python view_test_results.py failed

# View test statistics
python view_test_results.py stats

# View breakdown by module
python view_test_results.py modules

# View recent tests (last 50)
python view_test_results.py recent 50
```

### 2. Database Queries

You can also query the database directly:

```sql
-- View all test results
SELECT * FROM test_results ORDER BY test_datetime DESC;

-- View failed tests
SELECT * FROM test_results WHERE test_status IN ('FAILED', 'ERROR');

-- Get test statistics
SELECT 
    COUNT(*) as total_tests,
    SUM(CASE WHEN test_status = 'PASSED' THEN 1 ELSE 0 END) as passed_tests,
    SUM(CASE WHEN test_status = 'FAILED' THEN 1 ELSE 0 END) as failed_tests
FROM test_results;

-- View results by module
SELECT 
    module_name,
    COUNT(*) as total_tests,
    SUM(CASE WHEN test_status = 'PASSED' THEN 1 ELSE 0 END) as passed_tests
FROM test_results
GROUP BY module_name;
```

## Features

### Automatic Result Capture

- **Test Case Name**: Automatically captured from the test function name
- **Module Name**: Automatically captured from the test file name
- **Test Status**: Automatically determined (PASSED, FAILED, SKIPPED, ERROR)
- **Test DateTime**: Automatically recorded when the test completes
- **Error Message**: Captured for failed tests (if available)

### Multi-Device Testing

The system supports testing across multiple devices:
- Desktop
- iPhone 12
- Galaxy S20
- iPad

Each test run on different devices will be recorded separately in the database.

### Error Handling

- Database connection errors are gracefully handled
- Test execution continues even if database storage fails
- Error messages are logged for debugging

## File Structure

```
├── db/
│   ├── db_config.py          # Database configuration
│   └── db_helper.py          # Database helper functions
├── conftest.py               # Pytest configuration with DB integration
├── init_database.py          # Database initialization script
├── view_test_results.py      # Test results viewer
└── DATABASE_INTEGRATION.md   # This documentation
```

## Troubleshooting

### Database Connection Issues

1. **Check Configuration**: Verify your database settings in `db/db_config.py`
2. **Test Connection**: Run `python init_database.py` to test the connection
3. **Network Issues**: Ensure your server can reach the database host
4. **Credentials**: Verify username and password are correct

### Missing Test Results

1. **Check Logs**: Look for database error messages in test output
2. **Verify Table**: Ensure the `test_results` table exists
3. **Permissions**: Verify the database user has INSERT permissions

### Performance Considerations

- The database integration adds minimal overhead to test execution
- Results are stored asynchronously to avoid blocking test execution
- Consider archiving old test results periodically to maintain performance

## Example Output

When running tests, you'll see output like:

```
✅ Test results table created successfully
✅ Test result inserted: test_book_page_load_and_click - PASSED
✅ Test result inserted: test_monthly_plan_purchase - FAILED
```

When viewing results:

```
============================================================
 RECENT TEST RESULTS (Last 20)
============================================================
ID   Test Case Name                    Module               Status     DateTime
--------------------------------------------------------------------------------
1    test_book_page_load_and_click     test_book_purchase   ✅ PASSED   2024-01-15 10:30:15
2    test_monthly_plan_purchase        test_monthly_plan     ❌ FAILED   2024-01-15 10:25:30

📊 Test Statistics:
   Total Tests: 15
   ✅ Passed: 12 (80.0%)
   ❌ Failed: 2 (13.3%)
   ⏭️ Skipped: 1 (6.7%)
   ⚠️ Errors: 0 (0.0%)
``` 
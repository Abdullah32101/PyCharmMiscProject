# Test Results Storage in Database Tables

This document explains how test results are automatically stored across all database tables based on test type and execution status.

## Overview

When you run tests, the system automatically stores results in **multiple tables** based on the test type:

1. **`test_results`** - Always stores basic test information with error summaries
2. **`users`** - Stores test user data for user-related tests
3. **`books`** - Stores test book data for book-related tests
4. **`orders`** - Stores order records for purchase/subscription tests
5. **`subscriptions`** - Stores subscription records for plan tests

## Test Type Detection

The system automatically detects test types based on test case names and module names:

| Test Type | Keywords | Tables Updated |
|-----------|----------|----------------|
| **Book Tests** | `book`, `purchase` | `test_results`, `orders`, `books` |
| **Monthly Plan** | `monthly` | `test_results`, `orders`, `subscriptions` |
| **Six Month Plan** | `six_month` | `test_results`, `orders`, `subscriptions` |
| **Onetime Plan** | `onetime` | `test_results`, `orders` |
| **User Tests** | `user`, `register` | `test_results`, `users` |
| **Other Tests** | (default) | `test_results`, `orders` |

## Storage Logic

### 1. Book Purchase Tests

**Example**: `test_book_page_load_and_click`

**Tables Updated**:
- `test_results`: Basic test info with error summary
- `orders`: Order record with `book_purchase` type
- `books`: Test book data (if needed)

**Order Details**:
```sql
order_type: 'book_purchase'
amount: 49.99 (if PASSED) / 0.00 (if FAILED)
payment_status: 'completed' (if PASSED) / 'failed' (if FAILED)
order_status: 'completed' (if PASSED) / 'cancelled' (if FAILED)
```

### 2. Monthly Plan Tests

**Example**: `test_monthly_plan_purchase`

**Tables Updated**:
- `test_results`: Basic test info
- `orders`: Order record with `monthly_plan` type
- `subscriptions`: Subscription record

**Subscription Details**:
```sql
subscription_type: 'monthly'
amount: 29.99
start_date: Current date
end_date: Current date + 1 month
status: 'active' (if PASSED) / 'cancelled' (if FAILED)
```

### 3. Six Month Plan Tests

**Example**: `test_six_month_plan_purchase`

**Tables Updated**:
- `test_results`: Basic test info
- `orders`: Order record with `six_month_plan` type
- `subscriptions`: Subscription record

**Subscription Details**:
```sql
subscription_type: 'six_month'
amount: 149.99
start_date: Current date
end_date: Current date + 6 months
status: 'active' (if PASSED) / 'cancelled' (if FAILED)
```

### 4. Onetime Plan Tests

**Example**: `test_onetime_plan_purchase`

**Tables Updated**:
- `test_results`: Basic test info
- `orders`: Order record with `onetime_plan` type

**Order Details**:
```sql
order_type: 'onetime_plan'
amount: 99.99 (if PASSED) / 0.00 (if FAILED)
payment_status: 'completed' (if PASSED) / 'failed' (if FAILED)
order_status: 'completed' (if PASSED) / 'cancelled' (if FAILED)
```

### 5. User Tests

**Example**: `test_user_registration`

**Tables Updated**:
- `test_results`: Basic test info
- `users`: User record

**User Details**:
```sql
username: 'test_user_[random_id]'
email: 'test_user_[random_id]@test.com'
user_type: 'student'
is_active: TRUE (if PASSED) / FALSE (if FAILED)
```

## Data Relationships

### Test Results → Orders
- Every test creates a unique order number: `TEST-[8-char-id]`
- Order status reflects test status
- Payment status reflects test success/failure

### Test Results → Subscriptions
- Plan tests create subscription records
- Subscription status reflects test status
- Auto-renewal enabled for successful tests

### Test Results → Users
- User tests create user records
- User activation reflects test status
- Unique usernames for each test run

## Example Test Execution Flow

### Running a Book Purchase Test

```bash
pytest tests/test_book_purchase.py::test_book_page_load_and_click
```

**What Gets Stored**:

1. **test_results table**:
   ```sql
   test_case_name: 'test_book_page_load_and_click'
   module_name: 'test_book_purchase'
   test_status: 'PASSED' or 'FAILED'
   test_datetime: '2024-01-15 10:30:15'
   error_summary: 'Element not found' (for failed tests)
   ```

2. **orders table**:
   ```sql
   order_number: 'TEST-A1B2C3D4'
   order_type: 'book_purchase'
   amount: 49.99
   payment_status: 'completed'
   order_status: 'completed'
   ```

3. **books table** (if needed):
   ```sql
   title: 'Test Book for Automation'
   author: 'Test Author'
   isbn: '978-TEST-1234'
   price: 49.99
   ```

## Viewing Comprehensive Results

### Command Line Tools

**Basic Test Results**:
```bash
python view_test_results.py
```

**Comprehensive Results**:
```bash
python view_comprehensive_results.py summary
python view_comprehensive_results.py recent 20
python view_comprehensive_results.py breakdown
```

**Database Management**:
```bash
python manage_database.py summary
python manage_database.py view orders 10
python manage_database.py view subscriptions 5
```

### SQL Queries

**View Test Results with Related Data**:
```sql
SELECT tr.test_case_name, tr.test_status, tr.test_datetime,
       o.order_number, o.order_type, o.amount,
       s.subscription_type, s.status
FROM test_results tr
LEFT JOIN orders o ON o.order_number LIKE 'TEST-%'
LEFT JOIN subscriptions s ON s.user_id = o.user_id
ORDER BY tr.test_datetime DESC;
```

**Test Success Rate by Type**:
```sql
SELECT 
    CASE 
        WHEN test_case_name LIKE '%book%' THEN 'Book Tests'
        WHEN test_case_name LIKE '%monthly%' THEN 'Monthly Plan'
        WHEN test_case_name LIKE '%six_month%' THEN 'Six Month Plan'
        WHEN test_case_name LIKE '%onetime%' THEN 'Onetime Plan'
        ELSE 'Other Tests'
    END as test_category,
    COUNT(*) as total_tests,
    SUM(CASE WHEN test_status = 'PASSED' THEN 1 ELSE 0 END) as passed_tests,
    (SUM(CASE WHEN test_status = 'PASSED' THEN 1 ELSE 0 END) / COUNT(*)) * 100 as success_rate
FROM test_results
GROUP BY test_category;
```

## Benefits of Multi-Table Storage

1. **Complete Test Coverage**: Every test creates realistic data across all tables
2. **Business Logic Validation**: Test results reflect actual business scenarios
3. **Data Integrity**: Foreign key relationships ensure data consistency
4. **Comprehensive Reporting**: View test results from business perspective
5. **Realistic Testing**: Tests create actual orders, subscriptions, and user records

## Test Data Management

### Automatic Cleanup
- Test data is marked with `TEST-` prefixes
- Can be easily identified and cleaned up
- Maintains data integrity for production

### Sample Data
```bash
# Insert sample data for testing
python manage_database.py sample

# View all test-related data
python manage_database.py search orders "TEST-"
python manage_database.py search users "test_user"
```

### Data Retention
- Test results are kept for analysis
- Old test data can be archived
- Production data remains separate

## Error Handling

- Database errors don't stop test execution
- Failed database operations are logged
- Test results are still captured in `test_results` table
- Graceful degradation ensures test continuity

## New Features

### 1. Clean Module Names
- Module names are automatically cleaned to remove the `test.` prefix
- `test.test_book_purchase` becomes `test_book_purchase`
- Makes test results more readable and organized

### 2. Error Summary Column
- New `error_summary` column provides concise error descriptions
- Automatically extracts meaningful error messages from full error text
- Supports common error patterns:
  - ElementClickInterceptedException
  - NoSuchElementException
  - TimeoutException
  - AssertionError
  - WebDriverException
  - General Exception

### 3. Enhanced Error Display
- Test results viewer now shows both error summary and full error details
- Error summary is limited to 250 characters for readability
- Failed test details include both summary and full error message

## Database Schema Updates

To add the new `error_summary` column to existing databases:

```bash
python update_database_schema.py
```

This script will:
- Check if the column already exists
- Add the column if it doesn't exist
- Verify the database connection
- Display current test record count

This comprehensive storage approach ensures that your test results provide both technical metrics and business insights across all your database tables! 
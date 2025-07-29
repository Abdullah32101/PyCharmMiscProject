# GitHub Actions Test Suite Execution Guide

## Overview
This guide explains how to execute the test suite in GitHub Actions environment. The test framework is designed to run automatically in CI/CD pipelines and store results in a database.

## Available Workflows

### 1. Execute Test Suite (execute-test-suite.yml)
**Primary workflow for running all test suites**

**Triggers:**
- Push to main, master, develop, or test-ci-cd branches
- Pull requests to main or master
- Manual trigger with workflow_dispatch

**Features:**
- ✅ Runs comprehensive test suite runner
- ✅ Executes individual test suites
- ✅ Database integration with MySQL
- ✅ Screenshot capture for failures
- ✅ Test result storage in database
- ✅ Artifact upload for results

### 2. Test Automation (test-automation.yml)
**Advanced workflow with additional features**

**Features:**
- ✅ Multi-device testing (Desktop, Mobile, Tablet)
- ✅ Code quality checks
- ✅ Coverage reporting
- ✅ Security scanning
- ✅ PR comments with results

### 3. Complete Test Suite (complete-test-suite.yml)
**Legacy workflow for comprehensive testing**

## How to Execute Test Suite

### Method 1: Automatic Execution
The test suite will automatically execute when you:
1. Push code to main, master, develop, or test-ci-cd branches
2. Create a pull request to main or master branches

### Method 2: Manual Trigger
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "Execute Test Suite" workflow
4. Click "Run workflow"
5. Choose the test type (all, smoke, database, mobile)
6. Click "Run workflow"

### Method 3: Local Execution
Run the trigger script locally:
```bash
python trigger_test_suite_execution.py
```

## Test Suites Included

### 1. Comprehensive Test Suite Runner
- **File:** `run_all_test_suites.py`
- **Description:** Main test suite runner that executes all test suites
- **Features:** Database storage, result tracking, summary generation

### 2. Smoke Tests
- **File:** `tests/test_ci_smoke.py`
- **Description:** Fast CI smoke tests for basic functionality
- **Tests:** Page loading, Selenium basic functionality

### 3. Database Integration Tests
- **File:** `test_db_integration.py`
- **Description:** Database connection and integration tests
- **Tests:** Connection validation, data storage, retrieval

### 4. Error Link Tests
- **File:** `test_error_link_simple.py`
- **Description:** Error link generation and validation tests
- **Tests:** Screenshot capture, error link creation

### 5. Individual Test Files
- **Files:** Various test files in the root directory
- **Description:** Specific functionality tests
- **Tests:** CI/CD triggers, workflow tests, etc.

## Environment Setup

### GitHub Actions Environment
The workflow automatically sets up:
- Python 3.9
- MySQL 8.0 database
- Chrome browser
- All required dependencies

### Environment Variables
```bash
GITHUB_ACTIONS=true
TEST_DB_HOST=127.0.0.1
TEST_DB_USER=test_user
TEST_DB_PASSWORD=test_pass
TEST_DB_NAME=test_results
TEST_DB_PORT=3306
```

## Database Configuration

### Local Test Database (GitHub Actions)
- **Host:** 127.0.0.1
- **Database:** test_results
- **User:** test_user
- **Password:** test_pass

### Remote Database (Fallback)
- **Host:** 18.235.51.183
- **Database:** solutioninn_testing
- **User:** sqa_user
- **Password:** Hassan123!@#

## Test Results

### Database Storage
All test results are stored in the `test_results` table with:
- Test case name
- Module name
- Test status (PASSED/FAILED/SKIPPED/ERROR)
- Execution time
- Error messages
- Device information
- Screenshot links

### Artifacts
The workflow uploads:
- Screenshots of failed tests
- HTML test reports
- Coverage reports
- Test summary files

### PR Comments
For pull requests, the workflow automatically comments with:
- Test execution status
- Framework information
- Test suite details
- Links to artifacts

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check if MySQL service is running
   - Verify environment variables
   - Check network connectivity

2. **Chrome Installation Failed**
   - Workflow includes fallback to chromium-browser
   - Check system dependencies

3. **Test Timeout**
   - Tests have timeout limits (300-600 seconds)
   - Check for hanging processes
   - Review test complexity

4. **Missing Dependencies**
   - All dependencies are installed via requirements.txt
   - Check for version conflicts

### Debug Steps

1. **Check Workflow Logs**
   - Go to Actions tab in GitHub
   - Click on the failed workflow
   - Review step-by-step logs

2. **Run Locally**
   - Use the trigger script: `python trigger_test_suite_execution.py`
   - Check local environment setup

3. **Database Verification**
   - Run: `python test_database_connection.py`
   - Check connection parameters

## Best Practices

1. **Regular Execution**
   - Run tests on every push
   - Use scheduled runs for continuous monitoring

2. **Result Monitoring**
   - Check database for test trends
   - Review failed test screenshots
   - Monitor execution times

3. **Maintenance**
   - Keep dependencies updated
   - Clean up old artifacts
   - Monitor database storage

## Support

For issues with test execution:
1. Check the workflow logs
2. Review this documentation
3. Test locally first
4. Check database connectivity

## Quick Start

To immediately execute the test suite:

1. **Via GitHub UI:**
   - Go to Actions → Execute Test Suite → Run workflow

2. **Via Command Line:**
   ```bash
   git push origin main
   ```

3. **Via Local Script:**
   ```bash
   python trigger_test_suite_execution.py
   ```

The test suite will execute and provide detailed results in the GitHub Actions interface. 
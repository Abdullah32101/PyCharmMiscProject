# SolutionInn Automated Testing System

A comprehensive automated testing framework for SolutionInn membership plans and book purchase workflows. This system includes database integration, CI/CD pipeline setup, and robust error handling.

## 🚀 Features

### ✅ Complete Test Automation
- **Membership Plan Testing**: Monthly, 3-month, 6-month, and one-time plan automation
- **Book Purchase Testing**: Automated one-time book purchase workflows
- **Payment Processing**: Credit card payment automation with multiple payment methods
- **User Registration**: Automated email verification and user account creation
- **Mobile Testing**: Support for mobile device testing and responsive design validation

### 🗄️ Database Integration
- **Comprehensive Logging**: All test results stored in database with detailed error tracking
- **Error Link Feature**: Direct links to failed test screenshots for debugging
- **Test Result Analysis**: Detailed reporting and analytics for test performance
- **Database Migration**: Automated schema updates and data migration scripts

### 🔧 CI/CD Pipeline
- **GitHub Actions**: Automated test execution on code changes
- **Database Connection**: Robust database connectivity for GitHub Actions environment
- **Email Notifications**: Automated email reports for test results
- **Error Handling**: Comprehensive error handling and recovery mechanisms

### 📊 Monitoring & Debugging
- **Screenshot Capture**: Automatic screenshot capture for failed tests
- **Log Management**: Comprehensive logging system for debugging
- **Error Tracking**: Detailed error analysis and reporting
- **Performance Monitoring**: Test execution time and performance metrics

## 📁 Project Structure

```
PyCharmMiscProject/
├── 📁 core/                    # Core project files and constants
├── 📁 database/                # Database management and connection scripts
├── 📁 database_scripts/        # Database schema and migration scripts
├── 📁 db/                      # Database configuration and helpers
├── 📁 pages/                   # Page object models for test automation
├── 📁 scripts/                 # Main execution scripts and test runners
├── 📁 shell_scripts/           # Shell scripts for server operations
├── 📁 testing/                 # Testing utilities and debugging tools
├── 📁 tests/                   # Test case implementations
├── 📁 utilities/               # Utility scripts and maintenance tools
├── 📁 config/                  # Configuration files and setup
├── 📁 documentation/           # Comprehensive project documentation
└── 📁 assets/                  # CSS and styling assets
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Chrome/Chromium browser
- MySQL/PostgreSQL database
- Git

### Quick Start
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd PyCharmMiscProject
   ```

2. **Install dependencies**:
   ```bash
   pip install -r config/requirements.txt
   ```

3. **Configure database**:
   ```bash
   # Update database configuration in db/db_config.py
   # Run database setup scripts
   python database_scripts/create_tables.py
   ```

4. **Run tests**:
   ```bash
   # Run all membership plan tests
   python scripts/run_all_membership_plan_tests.py
   
   # Run specific test suite
   python scripts/run_purchase_membership_question_by_monthly_plan_test.py
   ```

## 🧪 Test Suites

### Membership Plan Tests
- **Monthly Plan**: `tests/test_purchase_membership_question_by_monthly_plan.py`
- **3-Month Popular Plan**: `tests/test_purchase_membership_question_by_three_month_popular_plan.py`
- **6-Month Plan**: `tests/test_purchase_membership_questions_by_six_month_plan.py`
- **One-Time Plan**: `tests/test_purchase_membership_question_by_one_time_plan.py`

### Book Purchase Tests
- **One-Time Book Purchase**: `tests/test_one_time_book_purchase.py`

### Mobile Tests
- **Mobile Book Purchase**: `scripts/run_mobile_one_time_book_test.py`

## 🔧 Configuration

### Database Configuration
Update `db/db_config.py` with your database credentials:
```python
DB_CONFIG = {
    'host': 'your-database-host',
    'port': 3306,
    'user': 'your-username',
    'password': 'your-password',
    'database': 'your-database-name'
}
```

### Test Configuration
Update `core/constants.py` with your test URLs and credentials:
```python
PRIMARY_URL = "https://staging.solutioninn.com/15"
SECONDARY_URL = "https://staging.solutioninn.com/study-help/..."
DEFAULT_PASSWORD = "your-test-password"
```

## 📊 Database Schema

The system uses the following main tables:
- `test_results`: Stores all test execution results
- `error_logs`: Detailed error information with screenshots
- `test_cases`: Test case definitions and metadata
- `subscription_types`: Membership plan configurations

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow
The system includes GitHub Actions workflows for:
- Automated test execution on pull requests
- Database connection testing
- Email notifications for test results
- Error reporting and debugging

### Workflow Files
- `.github/workflows/test-automation.yml`: Main test automation workflow
- `.github/workflows/database-test.yml`: Database connection testing

## 📈 Monitoring & Reporting

### Test Results Dashboard
- Comprehensive test result analysis
- Performance metrics and trends
- Error rate monitoring
- Screenshot gallery for failed tests

### Email Reports
- Automated email notifications
- Detailed test result summaries
- Error analysis and recommendations
- Performance insights

## 🔍 Troubleshooting

### Common Issues
1. **Database Connection**: Check database credentials and network connectivity
2. **Browser Issues**: Ensure Chrome/Chromium is installed and accessible
3. **Payment Processing**: Verify test payment credentials are valid
4. **Email Verification**: Check email service configuration

### Debug Tools
- `testing/debug_*.py`: Various debugging utilities
- `database/diagnose_*.py`: Database connection diagnostics
- `utilities/check_code_quality.py`: Code quality analysis

## 📚 Documentation

Comprehensive documentation is available in the `documentation/` folder:
- **Setup Guides**: Installation and configuration instructions
- **Troubleshooting**: Common issues and solutions
- **API Documentation**: Database and test framework APIs
- **Best Practices**: Coding standards and testing guidelines

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation in `documentation/`
- Review troubleshooting guides
- Open an issue on GitHub

---

**Last Updated**: January 2025
**Version**: 1.0.0
**Status**: Production Ready ✅

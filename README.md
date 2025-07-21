# Automated Test Framework

A comprehensive automated testing framework built with Python, Selenium, and Pytest for web application testing across multiple devices and browsers.

## 🚀 Features

- **Multi-device Testing**: Support for desktop, mobile (iPhone, iPad, Samsung Galaxy), and tablet devices
- **Cross-browser Compatibility**: Chrome-based testing with mobile emulation
- **Database Integration**: MySQL database for storing test results and analytics
- **Screenshot Capture**: Automatic screenshot capture for failed tests with error links
- **Test Reporting**: Comprehensive HTML reports with detailed test results
- **Device Detection**: Automatic device and screen resolution detection
- **Error Tracking**: Detailed error logging and debugging capabilities

## 📋 Prerequisites

- Python 3.7+
- Chrome browser
- MySQL database
- Git

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd PyCharmMiscProject
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**
   ```bash
   python init_database.py
   ```

## 🗄️ Database Configuration

The framework uses MySQL for storing test results. Configure your database connection in `db/db_config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'test_framework'
}
```

## 🧪 Running Tests

### Basic Test Execution
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_one_time_book_purchase.py

# Run with specific device
pytest --device="iPhone X"
```

### Environment Variables

- `HEADLESS`: Set to "true" for headless mode
- `MOBILE_TEST`: Set to "true" to force mobile testing
- `TEST_DEVICES`: Comma-separated list of devices to test

### Device Options
- `desktop`
- `iPhone X`
- `iPad Pro`
- `Samsung Galaxy S21`
- `Samsung Galaxy S20`
- `Samsung Galaxy S10`
- `Pixel 4`

## 📁 Project Structure

```
PyCharmMiscProject/
├── conftest.py                 # Pytest configuration and fixtures
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── db/                         # Database configuration and helpers
│   ├── db_config.py
│   └── db_helper.py
├── tests/                      # Test files
│   ├── test_one_time_book_purchase.py
│   ├── test_purchase_membership_question_by_monthly_plan.py
│   └── ...
├── pages/                      # Page Object Model classes
│   ├── one_time_book_purchase_methods.py
│   └── ...
├── assets/                     # Static assets
│   └── style.css
├── screenshots/                # Test screenshots (auto-generated)
└── test_reports/              # Test reports (auto-generated)
```

## 🔧 Configuration

### Test Configuration
The framework automatically configures:
- Device emulation settings
- Screen resolutions
- User agents
- Chrome options

### Screenshot Management
- Automatic screenshot capture on test failures
- Error link generation for debugging
- Page source capture for failed tests

## 📊 Test Results

Test results are stored in the MySQL database with the following information:
- Test name and module
- Execution status (PASSED/FAILED/ERROR)
- Device information and screen resolution
- Execution duration
- Error messages and links
- Screenshots for failed tests

## 🐛 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   - Ensure Chrome browser is installed
   - The framework automatically downloads the correct ChromeDriver version

2. **Database Connection Issues**
   - Verify MySQL is running
   - Check database credentials in `db/db_config.py`

3. **Device Emulation Issues**
   - Ensure Chrome supports the specified device
   - Check device names in the device mapping

### Debug Mode
Run tests with verbose output:
```bash
pytest -v -s
```

## 📈 Reporting

### View Test Results
```bash
# View comprehensive results
python view_comprehensive_results.py

# View simple test results
python view_test_results.py
```

### Generate Reports
```bash
# Generate HTML report
pytest --html=test_reports/report.html
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing documentation
3. Create an issue in the repository

## 🔄 Version History

- **v1.0.0**: Initial release with basic test framework
- **v1.1.0**: Added database integration
- **v1.2.0**: Enhanced device support and error tracking
- **v1.3.0**: Improved screenshot management and reporting

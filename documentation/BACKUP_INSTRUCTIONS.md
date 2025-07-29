# Backup and Transfer Instructions

## 🚀 Quick Transfer Guide

### Method 1: Git Repository (Recommended)
```bash
# On new laptop:
git clone <your-repository-url>
cd PyCharmMiscProject
pip install -r requirements.txt
python init_database.py
```

### Method 2: Direct Copy
1. Copy the entire `PyCharmMiscProject` folder to new laptop
2. Install Python 3.7+ on new machine
3. Run: `pip install -r requirements.txt`
4. Configure database in `db/db_config.py`
5. Run: `python init_database.py`

### Method 3: Create Backup Archive
```bash
# Create a backup archive (excluding unnecessary files)
tar -czf test_framework_backup.tar.gz --exclude='__pycache__' --exclude='screenshots' --exclude='test_reports' PyCharmMiscProject/
```

## 📋 Pre-Transfer Checklist

### ✅ Before Transferring:
- [ ] All code is committed to Git
- [ ] Database configuration is documented
- [ ] Environment variables are noted
- [ ] Dependencies are listed in requirements.txt

### ✅ On New Laptop:
- [ ] Install Python 3.7+
- [ ] Install Chrome browser
- [ ] Install MySQL (if using database)
- [ ] Install Git
- [ ] Clone/copy project files
- [ ] Install Python dependencies
- [ ] Configure database connection
- [ ] Test with a simple test run

## 🔧 Configuration Updates Needed

### Database Configuration
Update `db/db_config.py` with new database credentials:
```python
DB_CONFIG = {
    'host': 'localhost',  # or your database server
    'user': 'your_username',
    'password': 'your_password',
    'database': 'test_framework'
}
```

### Environment Variables
Set these on the new machine:
```bash
# Windows
set HEADLESS=false
set MOBILE_TEST=false
set TEST_DEVICES=desktop,iPhone X,iPad Pro

# Linux/Mac
export HEADLESS=false
export MOBILE_TEST=false
export TEST_DEVICES=desktop,iPhone X,iPad Pro
```

## 🧪 Testing the Transfer

After transferring, run these tests:

```bash
# Test basic setup
python -c "import pytest; print('Pytest OK')"
python -c "from selenium import webdriver; print('Selenium OK')"

# Test database connection
python test_db_simple.py

# Run a simple test
pytest tests/test_one_time_book_purchase.py -v
```

## 📁 Important Files to Transfer

### Essential Files:
- ✅ All `.py` files
- ✅ `requirements.txt`
- ✅ `conftest.py`
- ✅ `README.md`
- ✅ `db/` folder
- ✅ `tests/` folder
- ✅ `pages/` folder
- ✅ `assets/` folder

### Files to Exclude:
- ❌ `__pycache__/` folders
- ❌ `screenshots/` folder (auto-generated)
- ❌ `test_reports/` folder (auto-generated)
- ❌ `.git/` folder (will be recreated)
- ❌ Any temporary files

## 🆘 Troubleshooting Transfer Issues

### Common Issues:
1. **Python version mismatch**
   - Ensure both laptops have same Python version
   - Use virtual environments for consistency

2. **Missing dependencies**
   - Run `pip install -r requirements.txt`
   - Check for any missing system packages

3. **Database connection issues**
   - Verify MySQL is installed and running
   - Check database credentials
   - Ensure database exists

4. **Chrome driver issues**
   - Framework auto-downloads ChromeDriver
   - Ensure Chrome browser is installed

### Verification Commands:
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test database connection
python -c "from db.db_helper import MySQLHelper; print('Database OK')"

# Test Selenium setup
python -c "from selenium import webdriver; print('Selenium OK')"
```

## 📞 Support

If you encounter issues during transfer:
1. Check this troubleshooting guide
2. Review the main README.md
3. Ensure all prerequisites are met
4. Test with a simple example first 
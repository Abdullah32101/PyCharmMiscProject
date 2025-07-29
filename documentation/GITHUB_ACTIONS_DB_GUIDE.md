# 🚀 GitHub Actions Database Access Guide

## 📋 Overview

This guide explains how to access your remote database (`solutionsole.com`) from GitHub Actions workflows. The database is used to store test results and analytics.

## 🗄️ Database Configuration

### Current Setup
- **Host**: `solutionsole.com`
- **Database**: `test`
- **User**: `root`
- **Password**: `SolutionInn321`

### Configuration in Workflows

All GitHub Actions workflows now use this configuration:

```python
DB_CONFIG = {
    'host': 'solutionsole.com',
    'user': 'root',
    'password': 'SolutionInn321',
    'database': 'test'
}
```

## 🔧 Workflow Updates Made

### 1. **Scheduled Tests Workflow** (`.github/workflows/scheduled-tests.yml`)
- ✅ Removed local MySQL service
- ✅ Updated to use remote database
- ✅ Added database connection test
- ✅ Updated test reporting

### 2. **Test Automation Workflow** (`.github/workflows/test-automation.yml`)
- ✅ Removed local MySQL service
- ✅ Updated to use remote database
- ✅ Simplified database initialization

### 3. **Deploy Staging Workflow** (`.github/workflows/deploy-staging.yml`)
- ✅ Removed local MySQL service
- ✅ Updated to use remote database
- ✅ Added database connection verification

## 🧪 Testing Database Connection

### Manual Test Script
Use `test_db_connection_github.py` to test database connectivity:

```bash
python test_db_connection_github.py
```

### Expected Output
```
🔧 Testing database connection in GitHub Actions...
📅 Test Time: 2024-01-15 10:30:15
🖥️ Environment: true
🗄️ Database Host: solutionsole.com
📊 Database Name: test

✅ Database connection successful!
📊 Current test records in database: 150
📋 test_results table has 12 columns:
  - id: int(11)
  - test_case_name: varchar(255)
  - module_name: varchar(255)
  - test_status: enum('PASSED','FAILED','SKIPPED','ERROR')
  - test_datetime: datetime
  - error_message: text
  - error_summary: varchar(255)
  - total_time_duration: decimal(10,3)
  - device_name: varchar(50)
  - screen_resolution: varchar(50)
  - error_link: varchar(500)
  - created_at: timestamp

🎉 Database connection test completed successfully!
```

## 🚨 Troubleshooting Database Issues

### Common Issues and Solutions

#### 1. **Connection Timeout**
```
Error: (2003, "Can't connect to MySQL server on 'solutionsole.com'")
```

**Solutions:**
- Check if `solutionsole.com` is accessible from GitHub Actions
- Verify database server is running
- Check firewall settings on the database server
- Ensure MySQL is configured to accept external connections

#### 2. **Authentication Failed**
```
Error: (1045, "Access denied for user 'root'@'%'")
```

**Solutions:**
- Verify username and password are correct
- Check if the user has permission to connect from external hosts
- Ensure the user has proper privileges on the database

#### 3. **Database Not Found**
```
Error: (1049, "Unknown database 'test'")
```

**Solutions:**
- Verify the database name is correct
- Check if the database exists
- Ensure the user has access to the database

#### 4. **Network Connectivity Issues**
```
Error: (2002, "Can't connect to MySQL server")
```

**Solutions:**
- Test connectivity from GitHub Actions runner
- Check if the database server allows connections from GitHub's IP ranges
- Verify port 3306 is open and accessible

### Debugging Steps

#### Step 1: Test Basic Connectivity
```bash
# Test if the host is reachable
ping solutionsole.com

# Test if port 3306 is open
telnet solutionsole.com 3306
```

#### Step 2: Test Database Connection
```bash
# Use the test script
python test_db_connection_github.py
```

#### Step 3: Check Database Server Configuration
```sql
-- Check if user can connect from any host
SELECT user, host FROM mysql.user WHERE user = 'root';

-- Check user privileges
SHOW GRANTS FOR 'root'@'%';
```

#### Step 4: Verify Database Exists
```sql
-- List all databases
SHOW DATABASES;

-- Check if test database exists
USE test;
SHOW TABLES;
```

## 🔒 Security Considerations

### Database Security Best Practices

1. **Use Environment Variables** (Recommended)
   ```yaml
   env:
     DB_HOST: ${{ secrets.DB_HOST }}
     DB_USER: ${{ secrets.DB_USER }}
     DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
     DB_NAME: ${{ secrets.DB_NAME }}
   ```

2. **Create Dedicated Database User**
   ```sql
   CREATE USER 'github_actions'@'%' IDENTIFIED BY 'strong_password';
   GRANT SELECT, INSERT, UPDATE ON test.* TO 'github_actions'@'%';
   FLUSH PRIVILEGES;
   ```

3. **Restrict Network Access**
   - Configure firewall to only allow connections from GitHub Actions IP ranges
   - Use VPN or private network if possible

4. **Regular Password Rotation**
   - Change database passwords regularly
   - Use strong, unique passwords

## 📊 Monitoring Database Usage

### Check Test Results
```sql
-- View recent test results
SELECT * FROM test_results ORDER BY created_at DESC LIMIT 10;

-- Get test statistics
SELECT 
    test_status,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM test_results 
GROUP BY test_status;
```

### Monitor Database Performance
```sql
-- Check table size
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables 
WHERE table_schema = 'test';

-- Check recent activity
SELECT 
    COUNT(*) as recent_tests,
    MAX(created_at) as last_test
FROM test_results 
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR);
```

## 🚀 Next Steps

### Immediate Actions
1. ✅ Update all workflow files to use remote database
2. ✅ Test database connection in GitHub Actions
3. ✅ Verify test results are being stored correctly

### Future Improvements
1. 🔄 Use GitHub Secrets for database credentials
2. 🔄 Create dedicated database user for GitHub Actions
3. 🔄 Implement database connection pooling
4. 🔄 Add database backup and recovery procedures
5. 🔄 Set up database monitoring and alerting

## 📞 Support

If you encounter database issues:

1. **Check the logs** in GitHub Actions workflow runs
2. **Run the test script** locally to verify connectivity
3. **Review this guide** for troubleshooting steps
4. **Contact your database administrator** for server-side issues

---

*Last updated: January 2024* 
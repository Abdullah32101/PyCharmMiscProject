# 🚀 Complete Server Database Setup Guide

## 📋 Overview
This guide will help you set up your `solutionsole.com` server database to work with GitHub Actions.

## 🎯 Goal
Enable GitHub Actions to connect to your MySQL database on `solutionsole.com` and store test results.

## 📁 Files Created
- ✅ `server_database_setup.sh` - Automated setup script for Linux server
- ✅ `server_database_setup.bat` - Windows instructions
- ✅ `test_db_connection_simple.py` - Simple connection test
- ✅ `test_db_connection_github.py` - Detailed connection test
- ✅ Updated GitHub Actions workflows with proper error handling

## 🔧 Step-by-Step Server Setup

### **Step 1: SSH into Your Server**
```bash
ssh your-username@solutionsole.com
```

### **Step 2: Download the Setup Script**
Copy the `server_database_setup.sh` file to your server, or create it directly:

```bash
# Create the setup script on your server
nano server_database_setup.sh
# Copy the contents from the file I created
chmod +x server_database_setup.sh
```

### **Step 3: Run the Automated Setup**
```bash
./server_database_setup.sh
```

This script will automatically:
- ✅ Check MySQL status
- ✅ Update MySQL configuration (bind-address)
- ✅ Configure firewall settings
- ✅ Update user permissions
- ✅ Test connections
- ✅ Provide detailed feedback

### **Step 4: Manual Commands (if automated script fails)**

#### **4.1 Check MySQL Status**
```bash
sudo systemctl status mysql
```

#### **4.2 Update MySQL Configuration**
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```
Find and change:
```ini
# From:
bind-address = 127.0.0.1

# To:
bind-address = 0.0.0.0
```

#### **4.3 Restart MySQL**
```bash
sudo systemctl restart mysql
```

#### **4.4 Update User Permissions**
```bash
mysql -u root -p
```
Then run these SQL commands:
```sql
-- Grant external access permissions
GRANT ALL PRIVILEGES ON test.* TO 'root'@'%' IDENTIFIED BY 'SolutionInn321';
FLUSH PRIVILEGES;

-- Verify the changes
SELECT user, host FROM mysql.user WHERE user = 'root';
SHOW GRANTS FOR 'root'@'%';
EXIT;
```

#### **4.5 Configure Firewall**
```bash
sudo ufw status
sudo ufw allow 3306
```

#### **4.6 Test Local Connection**
```bash
mysql -u root -p -h localhost test
```

## 🧪 Testing the Setup

### **Test 1: Local Connection**
```bash
mysql -u root -p -h localhost test
```

### **Test 2: External Connection**
```bash
mysql -u root -p'SolutionInn321' -h localhost test
```

### **Test 3: Port Listening**
```bash
sudo netstat -tlnp | grep ":3306"
```

## 🚀 GitHub Actions Testing

### **Step 1: Run the Workflow**
1. Go to your GitHub repository
2. Click **Actions** tab
3. Select **Scheduled Test Runner**
4. Click **Run workflow**
5. Choose test suite (e.g., "database" for quick test)

### **Step 2: Monitor the Results**
Watch for these success messages:
```
✅ Network connectivity to solutionsole.com:3306 successful
✅ Database connection successful!
📊 Current test records in database: [number]
```

### **Step 3: Check Test Results**
- ✅ Database connection should succeed
- ✅ Test results should be stored in database
- ✅ GitHub issue should be created with summary

## 🔍 Troubleshooting

### **Common Issues and Solutions**

#### **Issue 1: Connection Timeout**
```
Error: (2003, "Can't connect to MySQL server on 'solutionsole.com'")
```
**Solution:**
- Check if MySQL is running: `sudo systemctl status mysql`
- Verify bind-address: `grep bind-address /etc/mysql/mysql.conf.d/mysqld.cnf`
- Check firewall: `sudo ufw status`

#### **Issue 2: Access Denied**
```
Error: (1045, "Access denied for user 'root'@'%'")
```
**Solution:**
- Update user permissions in MySQL
- Check if user exists: `SELECT user, host FROM mysql.user WHERE user = 'root';`

#### **Issue 3: Database Not Found**
```
Error: (1049, "Unknown database 'test'")
```
**Solution:**
- Create the database: `CREATE DATABASE test;`
- Verify database exists: `SHOW DATABASES;`

#### **Issue 4: Port Not Listening**
```
Error: Connection refused
```
**Solution:**
- Check if MySQL is listening: `sudo netstat -tlnp | grep ":3306"`
- Restart MySQL: `sudo systemctl restart mysql`

## 📊 Verification Checklist

After setup, verify these items:

- ✅ [ ] MySQL is running: `sudo systemctl status mysql`
- ✅ [ ] bind-address is 0.0.0.0: `grep bind-address /etc/mysql/mysql.conf.d/mysqld.cnf`
- ✅ [ ] Port 3306 is open: `sudo ufw status`
- ✅ [ ] User has external permissions: `SHOW GRANTS FOR 'root'@'%';`
- ✅ [ ] Local connection works: `mysql -u root -p -h localhost test`
- ✅ [ ] GitHub Actions workflow succeeds
- ✅ [ ] Test results are stored in database

## 🎉 Success Indicators

When everything is working correctly, you should see:

1. **GitHub Actions Logs:**
   ```
   ✅ Network connectivity to solutionsole.com:3306 successful
   ✅ Database connection successful!
   📊 Current test records in database: 150
   ```

2. **Database Records:**
   ```sql
   SELECT * FROM test_results ORDER BY created_at DESC LIMIT 5;
   ```

3. **GitHub Issue Created:**
   - Automatic issue with test summary
   - Labels: automated, testing, scheduled

## 📞 Support

If you encounter issues:

1. **Check the server setup script output** for specific error messages
2. **Review the GitHub Actions logs** for connection details
3. **Test local connections** on the server first
4. **Verify firewall and network settings**

---

**🎯 Goal Achieved:** Your GitHub Actions workflow will now successfully connect to your `solutionsole.com` database and store test results! 
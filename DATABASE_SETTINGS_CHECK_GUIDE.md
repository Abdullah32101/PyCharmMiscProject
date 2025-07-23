# 🔍 Database Settings Check Guide

## 📋 Overview
This guide explains how to check your database settings on the `solutionsole.com` server to ensure GitHub Actions can connect properly.

## 🎯 What We Need to Check

### **1. MySQL Service Status**
### **2. MySQL Configuration (bind-address)**
### **3. User Permissions**
### **4. Port Listening**
### **5. Database Existence**

---

## 🔧 Step-by-Step Database Settings Check

### **Step 1: Check MySQL Service Status**

SSH into your server and run:
```bash
ssh your-username@solutionsole.com
sudo systemctl status mysql
```

**✅ Expected Output:**
```
● mysql.service - MySQL Community Server
   Loaded: loaded (/etc/systemd/system/mysql.service; enabled)
   Active: active (running) since [date]
```

**❌ If MySQL is not running:**
```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

---

### **Step 2: Check MySQL Configuration (bind-address)**

This is the most important setting for external connections:

```bash
grep bind-address /etc/mysql/mysql.conf.d/mysqld.cnf
```

**✅ Expected Output:**
```
bind-address = 0.0.0.0
```

**❌ If you see:**
```
bind-address = 127.0.0.1
```

**Fix it:**
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# Change: bind-address = 0.0.0.0
sudo systemctl restart mysql
```

---

### **Step 3: Check User Permissions**

Connect to MySQL and check user permissions:

```bash
mysql -u root -p
```

Then run these SQL commands:
```sql
-- Check current users
SELECT user, host FROM mysql.user WHERE user = 'root';

-- Check specific permissions
SHOW GRANTS FOR 'root'@'%';

-- Exit MySQL
EXIT;
```

**✅ Expected Output:**
```
+------+------+
| user | host |
+------+------+
| root | %    |
| root | localhost |
+------+------+

+-------------------------------------------------------------+
| Grants for root@%                                            |
+-------------------------------------------------------------+
| GRANT ALL PRIVILEGES ON test.* TO 'root'@'%'                |
+-------------------------------------------------------------+
```

**❌ If 'root'@'%' is missing:**
```sql
GRANT ALL PRIVILEGES ON test.* TO 'root'@'%' IDENTIFIED BY 'SolutionInn321';
FLUSH PRIVILEGES;
```

---

### **Step 4: Check Port Listening**

Check if MySQL is listening on port 3306:

```bash
sudo netstat -tlnp | grep 3306
```

**✅ Expected Output:**
```
tcp6       0      0 :::3306                 :::*                    LISTEN      13021/mysqld
```

**❌ If no output:**
- MySQL is not listening on port 3306
- Check MySQL service status
- Restart MySQL: `sudo systemctl restart mysql`

---

### **Step 5: Check Database Existence**

Verify the 'test' database exists:

```bash
mysql -u root -p -e "SHOW DATABASES;"
```

**✅ Expected Output:**
```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| test               |
+--------------------+
```

**❌ If 'test' database is missing:**
```bash
mysql -u root -p -e "CREATE DATABASE test;"
```

---

### **Step 6: Test Local Connection**

Test the exact connection that GitHub Actions will use:

```bash
mysql -u root -p'SolutionInn321' -h localhost test
```

**✅ Expected Output:**
```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is [number]
Server version: 10.1.48-MariaDB MariaDB Server

MariaDB [test]>
```

**❌ If connection fails:**
- Check password is correct
- Check user permissions
- Check database exists

---

## 🧪 Complete Database Test Script

Run this script on your server to check everything at once:

```bash
#!/bin/bash
echo "🔍 Database Settings Check"
echo "=========================="

echo "1. Checking MySQL service status..."
if sudo systemctl is-active --quiet mysql; then
    echo "✅ MySQL is running"
else
    echo "❌ MySQL is not running"
    exit 1
fi

echo "2. Checking bind-address..."
BIND_ADDRESS=$(grep bind-address /etc/mysql/mysql.conf.d/mysqld.cnf | head -1 | awk '{print $3}')
if [ "$BIND_ADDRESS" = "0.0.0.0" ]; then
    echo "✅ bind-address is correct: $BIND_ADDRESS"
else
    echo "❌ bind-address needs fixing: $BIND_ADDRESS"
fi

echo "3. Checking port 3306..."
if sudo netstat -tlnp | grep -q ":3306"; then
    echo "✅ Port 3306 is listening"
else
    echo "❌ Port 3306 is not listening"
fi

echo "4. Checking user permissions..."
mysql -u root -p -e "SELECT user, host FROM mysql.user WHERE user = 'root' AND host = '%';" 2>/dev/null | grep -q "root" && echo "✅ root@% user exists" || echo "❌ root@% user missing"

echo "5. Checking test database..."
mysql -u root -p -e "SHOW DATABASES LIKE 'test';" 2>/dev/null | grep -q "test" && echo "✅ test database exists" || echo "❌ test database missing"

echo "6. Testing connection..."
if mysql -u root -p'SolutionInn321' -h localhost -e "SELECT 1;" 2>/dev/null; then
    echo "✅ Local connection successful"
else
    echo "❌ Local connection failed"
fi

echo "=========================="
echo "Check complete!"
```

---

## 🚨 Common Issues and Solutions

### **Issue 1: bind-address is 127.0.0.1**
**Problem:** MySQL only accepts local connections
**Solution:** Change to `bind-address = 0.0.0.0`

### **Issue 2: User 'root'@'%' doesn't exist**
**Problem:** No external access permissions
**Solution:** `GRANT ALL PRIVILEGES ON test.* TO 'root'@'%'`

### **Issue 3: Port 3306 not listening**
**Problem:** MySQL not bound to external interfaces
**Solution:** Check bind-address and restart MySQL

### **Issue 4: Database 'test' doesn't exist**
**Problem:** Target database missing
**Solution:** `CREATE DATABASE test;`

---

## 🎯 Quick Commands Summary

```bash
# 1. Check MySQL status
sudo systemctl status mysql

# 2. Check bind-address
grep bind-address /etc/mysql/mysql.conf.d/mysqld.cnf

# 3. Check port listening
sudo netstat -tlnp | grep 3306

# 4. Check user permissions
mysql -u root -p -e "SELECT user, host FROM mysql.user WHERE user = 'root';"

# 5. Test connection
mysql -u root -p'SolutionInn321' -h localhost test
```

---

## 📊 Verification Checklist

After running all checks, verify:

- ✅ [ ] MySQL service is running
- ✅ [ ] bind-address = 0.0.0.0
- ✅ [ ] Port 3306 is listening
- ✅ [ ] User 'root'@'%' exists
- ✅ [ ] Database 'test' exists
- ✅ [ ] Local connection works
- ✅ [ ] GitHub Actions can connect

---

**🎯 Goal:** All checks should pass for GitHub Actions to connect successfully! 
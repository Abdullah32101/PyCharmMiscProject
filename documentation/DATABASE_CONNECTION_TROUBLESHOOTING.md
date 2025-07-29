# 🔧 Database Connection Troubleshooting Guide

## 🚨 **Issue Identified:**
GitHub Actions cannot connect to database server `solutionsole.com:3306`

**Error:** `Can't connect to MySQL server on 'solutionsole.com:3306' (110)`

## 🔍 **Root Cause Analysis:**

### **Error Code 110:**
- **Meaning:** Connection timeout
- **Cause:** Network connectivity issue or firewall blocking

## 🛠️ **Solutions (In Order of Priority):**

### **1. Check Database Server Status**
```bash
# On your database server
sudo systemctl status mysql
sudo systemctl status mysqld
```

### **2. Verify MySQL Remote Access**
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Check if remote access is enabled
SELECT user, host FROM mysql.user WHERE user = 'root';

-- If no remote access, create it:
CREATE USER 'root'@'%' IDENTIFIED BY 'SolutionInn321';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;
```

### **3. Check MySQL Configuration**
```bash
# Edit MySQL config
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Ensure these lines are set:
bind-address = 0.0.0.0  # Allow all IPs
port = 3306

# Restart MySQL
sudo systemctl restart mysql
```

### **4. Configure Firewall**
```bash
# Allow MySQL port
sudo ufw allow 3306
sudo ufw allow from any to any port 3306

# Or for specific IP ranges (GitHub Actions)
sudo ufw allow from 140.82.112.0/20 to any port 3306
sudo ufw allow from 143.55.64.0/20 to any port 3306
```

### **5. GitHub Actions IP Ranges**
Add these IP ranges to your firewall:
- `140.82.112.0/20`
- `143.55.64.0/20`
- `185.199.108.0/22`
- `192.30.252.0/22`

## 🧪 **Testing Database Connectivity:**

### **From Local Machine:**
```bash
# Test connection
mysql -h solutionsole.com -u root -p -e "SELECT 1;"
```

### **From GitHub Actions:**
The workflow now includes better error reporting and will show:
- Connection status
- Error details
- Troubleshooting suggestions

## 📋 **Immediate Actions:**

1. **Check if database server is running**
2. **Verify MySQL accepts remote connections**
3. **Configure firewall to allow GitHub Actions IPs**
4. **Test connection manually**
5. **Re-run GitHub Actions workflow**

## 🎯 **Expected Result:**
After fixing, the workflow should show:
```
✅ Database connection successful!
✅ Database verification completed successfully!
✅ All test results have been stored in the database
```

## 📞 **If Still Having Issues:**
1. Check server logs: `sudo tail -f /var/log/mysql/error.log`
2. Test with different MySQL client
3. Verify network connectivity
4. Consider using SSH tunnel for secure connection 
#!/bin/bash

# Simple Database Fix Script for 18.235.51.183
# Run these commands manually on your database server

echo "🔧 Database Server Fix for 18.235.51.183"
echo "========================================"
echo "Your Database Credentials:"
echo "Host: 18.235.51.183"
echo "User: sqa_user"
echo "Password: Hassan123!@#"
echo "Database: solutioninn_testing"
echo ""

echo "📋 Manual Steps to Fix Database Server:"
echo "========================================"
echo ""

echo "1. 🔥 Fix Firewall (Run these commands):"
echo "   sudo ufw allow 3306"
echo "   sudo ufw reload"
echo ""

echo "2. 🗄️ Configure MySQL (Edit the file):"
echo "   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf"
echo "   Find the line: bind-address = 127.0.0.1"
echo "   Change it to: bind-address = 0.0.0.0"
echo "   Save and exit (Ctrl+X, Y, Enter)"
echo ""

echo "3. 🔄 Restart MySQL:"
echo "   sudo systemctl restart mysql"
echo "   sudo systemctl status mysql"
echo ""

echo "4. 👤 Create Database and User (Run these commands):"
echo "   mysql -u root -p"
echo "   (Enter your MySQL root password when prompted)"
echo ""

echo "5. 📝 In MySQL, run these commands:"
echo "   CREATE DATABASE IF NOT EXISTS solutioninn_testing;"
echo "   CREATE USER IF NOT EXISTS 'sqa_user'@'%' IDENTIFIED BY 'Hassan123!@#';"
echo "   GRANT ALL PRIVILEGES ON solutioninn_testing.* TO 'sqa_user'@'%';"
echo "   FLUSH PRIVILEGES;"
echo "   EXIT;"
echo ""

echo "6. 🧪 Test the Connection:"
echo "   mysql -u sqa_user -pHassan123!@# -e 'SELECT 1 as test;'"
echo ""

echo "7. 🌐 Test Network Connectivity:"
echo "   telnet 18.235.51.183 3306"
echo ""

echo "8. 📊 Check if port is listening:"
echo "   sudo netstat -tlnp | grep 3306"
echo ""

echo "🎯 After completing these steps, your database should be accessible!"
echo ""

echo "🔍 If you're still having issues:"
echo "1. Check if you're using a cloud provider (AWS, Google Cloud, etc.)"
echo "2. Configure security groups/firewall rules to allow port 3306"
echo "3. Ensure the server allows external connections"
echo ""

echo "📞 Test from your local machine:"
echo "python test_database_connection.py" 
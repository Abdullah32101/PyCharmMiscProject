#!/bin/bash

# Database Server Fix Script
# Run this script on your database server (18.235.51.183)

echo "🔧 Database Server Fix Script"
echo "================================"
echo "This script will fix common database connection issues"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Please run this script as root (use sudo)${NC}"
    exit 1
fi

echo "📋 Step 1: Checking MySQL service status..."
systemctl is-active --quiet mysql
print_status $? "MySQL service status"

if [ $? -ne 0 ]; then
    echo "🔄 Starting MySQL service..."
    systemctl start mysql
    systemctl enable mysql
    print_status $? "MySQL service started and enabled"
fi

echo ""
echo "📋 Step 2: Configuring firewall..."
# Check if ufw is active
if command -v ufw &> /dev/null && ufw status | grep -q "Status: active"; then
    echo "🔥 UFW is active, allowing port 3306..."
    ufw allow 3306
    print_status $? "Port 3306 allowed in UFW"
else
    echo "🔥 Configuring iptables for port 3306..."
    iptables -A INPUT -p tcp --dport 3306 -j ACCEPT
    iptables-save > /etc/iptables/rules.v4
    print_status $? "Port 3306 allowed in iptables"
fi

echo ""
echo "📋 Step 3: Configuring MySQL bind address..."
# Backup original config
cp /etc/mysql/mysql.conf.d/mysqld.cnf /etc/mysql/mysql.conf.d/mysqld.cnf.backup

# Update bind-address
sed -i 's/bind-address.*=.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

# Check if the change was made
if grep -q "bind-address = 0.0.0.0" /etc/mysql/mysql.conf.d/mysqld.cnf; then
    print_status 0 "MySQL bind-address configured"
else
    print_status 1 "Failed to configure MySQL bind-address"
fi

echo ""
echo "📋 Step 4: Restarting MySQL service..."
systemctl restart mysql
print_status $? "MySQL service restarted"

echo ""
echo "📋 Step 5: Creating database and user..."
# Create MySQL script
cat > /tmp/setup_db.sql << 'EOF'
CREATE DATABASE IF NOT EXISTS solutioninn_testing;
CREATE USER IF NOT EXISTS 'sqa_user'@'%' IDENTIFIED BY 'Hassan123!@#';
GRANT ALL PRIVILEGES ON solutioninn_testing.* TO 'sqa_user'@'%';
FLUSH PRIVILEGES;
SELECT 'Database and user created successfully' as status;
EOF

# Run the script (will prompt for root password)
echo "Please enter your MySQL root password when prompted:"
mysql -u root -p < /tmp/setup_db.sql
print_status $? "Database and user setup"

echo ""
echo "📋 Step 6: Testing connection..."
# Test connection
mysql -u sqa_user -pHassan123!@# -e "SELECT 1 as test;" 2>/dev/null
print_status $? "Database connection test"

echo ""
echo "📋 Step 7: Checking port availability..."
netstat -tlnp | grep 3306
print_status $? "Port 3306 listening"

echo ""
echo "📋 Step 8: Final connectivity test..."
# Get server IP
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "🌐 Testing connection from $SERVER_IP:3306"
telnet $SERVER_IP 3306 < /dev/null 2>&1
print_status $? "Local connectivity test"

echo ""
echo "🎉 Database server configuration complete!"
echo ""
echo "📊 Summary:"
echo "- MySQL service: $(systemctl is-active mysql)"
echo "- Port 3306: $(netstat -tlnp | grep 3306 | wc -l) listener(s)"
echo "- Database: solutioninn_testing"
echo "- User: sqa_user"
echo "- Bind address: 0.0.0.0"
echo ""
echo "🔧 If you're still having issues:"
echo "1. Check your cloud provider's security groups/firewall"
echo "2. Ensure the server allows external connections"
echo "3. Test from a different machine: telnet 18.235.51.183 3306"
echo ""
echo "📝 Next steps:"
echo "1. Test the connection from GitHub Actions"
echo "2. Run your test suites"
echo "3. Monitor the database logs: tail -f /var/log/mysql/error.log" 
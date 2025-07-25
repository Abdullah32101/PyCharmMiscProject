#!/bin/bash
# Database Server Configuration Fix Script
# Run this script on your database server (18.235.51.183)

echo "🔧 Fixing database server configuration for GitHub Actions access..."
echo "================================================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ This script must be run as root (use sudo)"
    exit 1
fi

echo "📋 Step 1: Updating MySQL bind-address..."
# Find and update MySQL configuration file
MYSQL_CONF_FILES=(
    "/etc/mysql/mysql.conf.d/mysqld.cnf"
    "/etc/mysql/mysqld.cnf"
    "/etc/my.cnf"
    "/etc/mysql/my.cnf"
)

MYSQL_CONF_UPDATED=false
for conf_file in "${MYSQL_CONF_FILES[@]}"; do
    if [ -f "$conf_file" ]; then
        echo "   Found MySQL config: $conf_file"
        # Backup original file
        cp "$conf_file" "$conf_file.backup.$(date +%Y%m%d_%H%M%S)"
        
        # Update bind-address
        sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' "$conf_file"
        
        # Check if bind-address line exists, if not add it
        if ! grep -q "bind-address" "$conf_file"; then
            echo "bind-address = 0.0.0.0" >> "$conf_file"
        fi
        
        MYSQL_CONF_UPDATED=true
        echo "   ✅ Updated bind-address in $conf_file"
        break
    fi
done

if [ "$MYSQL_CONF_UPDATED" = false ]; then
    echo "   ⚠️ Could not find MySQL configuration file"
    echo "   Please manually set bind-address = 0.0.0.0 in your MySQL config"
fi

echo ""
echo "👤 Step 2: Granting external access to sqa_user..."
# Create MySQL script
cat > /tmp/fix_mysql_users.sql << 'EOF'
-- Grant external access to sqa_user
GRANT ALL PRIVILEGES ON solutioninn_testing.* TO 'sqa_user'@'%' IDENTIFIED BY 'Hassan123!@#';

-- Also grant access to root for testing (optional)
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root';

-- Flush privileges
FLUSH PRIVILEGES;

-- Show current users
SELECT user, host FROM mysql.user WHERE user IN ('sqa_user', 'root');
EOF

# Execute MySQL script
mysql -u root -p < /tmp/fix_mysql_users.sql
rm /tmp/fix_mysql_users.sql

echo ""
echo "🔥 Step 3: Configuring firewall..."
# Check if ufw is available
if command -v ufw &> /dev/null; then
    ufw allow 3306
    echo "   ✅ UFW: Allowed port 3306"
else
    echo "   ⚠️ UFW not found, please manually allow port 3306"
fi

# Check if iptables is available
if command -v iptables &> /dev/null; then
    iptables -A INPUT -p tcp --dport 3306 -j ACCEPT
    echo "   ✅ iptables: Allowed port 3306"
fi

echo ""
echo "🔄 Step 4: Restarting MySQL service..."
# Try different service names
if systemctl list-unit-files | grep -q mysql; then
    systemctl restart mysql
    echo "   ✅ MySQL service restarted"
elif systemctl list-unit-files | grep -q mysqld; then
    systemctl restart mysqld
    echo "   ✅ MySQL service restarted"
else
    echo "   ⚠️ Could not restart MySQL service automatically"
    echo "   Please restart MySQL manually: sudo systemctl restart mysql"
fi

echo ""
echo "🔍 Step 5: Testing MySQL configuration..."
# Wait a moment for MySQL to start
sleep 3

# Test MySQL is running
if systemctl is-active --quiet mysql || systemctl is-active --quiet mysqld; then
    echo "   ✅ MySQL service is running"
else
    echo "   ❌ MySQL service is not running"
    echo "   Please check MySQL logs and restart manually"
fi

# Test bind-address
echo "   📡 Testing bind-address configuration..."
netstat -tlnp | grep 3306

echo ""
echo "✅ Database server configuration updated!"
echo "========================================"
echo "🔍 Next steps:"
echo "   1. Test connection from external host:"
echo "      mysql -h 18.235.51.183 -u sqa_user -p solutioninn_testing"
echo "   2. Run your GitHub Actions workflow again"
echo "   3. Check if logs are now being stored in remote database"
echo ""
echo "📋 Configuration summary:"
echo "   - bind-address: 0.0.0.0 (allows external connections)"
echo "   - sqa_user: granted external access"
echo "   - Firewall: port 3306 allowed"
echo "   - MySQL service: restarted" 
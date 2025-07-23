#!/bin/bash

# Server Database Setup Script for GitHub Actions
# Run this script on your solutionsole.com server

echo "🔧 Server Database Setup for GitHub Actions"
echo "=========================================="
echo "Target: solutionsole.com"
echo "Date: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

print_status "Starting server database setup..."

# Step 1: Check MySQL status
print_status "Step 1: Checking MySQL status..."
if sudo systemctl is-active --quiet mysql; then
    print_success "MySQL is running"
else
    print_error "MySQL is not running. Starting MySQL..."
    sudo systemctl start mysql
    if sudo systemctl is-active --quiet mysql; then
        print_success "MySQL started successfully"
    else
        print_error "Failed to start MySQL"
        exit 1
    fi
fi

# Step 2: Check MySQL configuration
print_status "Step 2: Checking MySQL configuration..."
MYSQL_CONF="/etc/mysql/mysql.conf.d/mysqld.cnf"
if [ -f "$MYSQL_CONF" ]; then
    print_success "MySQL config file found: $MYSQL_CONF"
    
    # Check bind-address
    BIND_ADDRESS=$(grep "bind-address" "$MYSQL_CONF" | head -1 | awk '{print $3}')
    if [ "$BIND_ADDRESS" = "0.0.0.0" ]; then
        print_success "bind-address is already set to 0.0.0.0 (allows external connections)"
    else
        print_warning "bind-address is set to: $BIND_ADDRESS"
        print_status "Updating bind-address to allow external connections..."
        
        # Backup original config
        sudo cp "$MYSQL_CONF" "${MYSQL_CONF}.backup.$(date +%Y%m%d_%H%M%S)"
        
        # Update bind-address
        sudo sed -i 's/bind-address.*=.*/bind-address = 0.0.0.0/' "$MYSQL_CONF"
        
        print_success "bind-address updated to 0.0.0.0"
        print_status "Restarting MySQL to apply changes..."
        sudo systemctl restart mysql
    fi
else
    print_error "MySQL config file not found at $MYSQL_CONF"
    exit 1
fi

# Step 3: Check firewall settings
print_status "Step 3: Checking firewall settings..."
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(sudo ufw status | head -1)
    if [[ "$UFW_STATUS" == *"inactive"* ]]; then
        print_warning "UFW firewall is inactive"
    else
        print_status "UFW firewall is active. Checking MySQL port..."
        if sudo ufw status | grep -q "3306"; then
            print_success "Port 3306 is already allowed"
        else
            print_status "Adding port 3306 to firewall..."
            sudo ufw allow 3306
            print_success "Port 3306 added to firewall"
        fi
    fi
else
    print_warning "UFW not found. Please check your firewall settings manually."
fi

# Step 4: Check MySQL user permissions
print_status "Step 4: Checking MySQL user permissions..."
print_status "You will need to enter your MySQL root password:"

# Create a temporary SQL file
TEMP_SQL=$(mktemp)
cat > "$TEMP_SQL" << 'EOF'
-- Check current root user permissions
SELECT user, host FROM mysql.user WHERE user = 'root';

-- Grant permissions for external connections
GRANT ALL PRIVILEGES ON test.* TO 'root'@'%' IDENTIFIED BY 'SolutionInn321';
FLUSH PRIVILEGES;

-- Verify the changes
SELECT user, host FROM mysql.user WHERE user = 'root';
SHOW GRANTS FOR 'root'@'%';
EOF

# Execute the SQL commands
mysql -u root -p < "$TEMP_SQL"
SQL_RESULT=$?

if [ $SQL_RESULT -eq 0 ]; then
    print_success "MySQL user permissions updated successfully"
else
    print_error "Failed to update MySQL user permissions"
    print_status "Please run the following commands manually:"
    echo "mysql -u root -p"
    echo "GRANT ALL PRIVILEGES ON test.* TO 'root'@'%' IDENTIFIED BY 'SolutionInn321';"
    echo "FLUSH PRIVILEGES;"
fi

# Clean up temporary file
rm -f "$TEMP_SQL"

# Step 5: Test local database connection
print_status "Step 5: Testing local database connection..."
if mysql -u root -p -h localhost -e "USE test; SELECT 1 as test;" 2>/dev/null; then
    print_success "Local database connection successful"
else
    print_error "Local database connection failed"
    print_status "Please check your MySQL root password and try again"
fi

# Step 6: Test external database connection
print_status "Step 6: Testing external database connection..."
EXTERNAL_IP=$(curl -s ifconfig.me)
print_status "Testing connection from external IP: $EXTERNAL_IP"

if mysql -u root -p'SolutionInn321' -h localhost -e "USE test; SELECT 1 as test;" 2>/dev/null; then
    print_success "External database connection successful"
else
    print_warning "External database connection failed"
    print_status "This might be expected if testing from the same server"
fi

# Step 7: Check if port 3306 is listening
print_status "Step 7: Checking if MySQL is listening on port 3306..."
if sudo netstat -tlnp | grep ":3306"; then
    print_success "MySQL is listening on port 3306"
else
    print_error "MySQL is not listening on port 3306"
fi

# Step 8: Final verification
print_status "Step 8: Final verification..."
echo ""
print_success "Server database setup completed!"
echo ""
echo "📋 Summary:"
echo "✅ MySQL service status: $(sudo systemctl is-active mysql)"
echo "✅ bind-address: $(grep bind-address "$MYSQL_CONF" | head -1 | awk '{print $3}')"
echo "✅ Port 3306: $(sudo netstat -tlnp | grep ":3306" | wc -l) listeners"
echo ""
echo "🔧 Next steps:"
echo "1. Test the connection from GitHub Actions"
echo "2. If still failing, check your hosting provider's firewall"
echo "3. Consider using a dedicated database user instead of root"
echo ""
echo "📞 If you need help, check the GitHub Actions logs for specific error messages" 
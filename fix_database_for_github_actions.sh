#!/bin/bash
# Fix Database Configuration for GitHub Actions
# Run this script on your database server (18.235.51.183)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}🔧 FIXING DATABASE FOR GITHUB ACTIONS${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}📅 Time: $(date)${NC}"
    echo -e "${BLUE}🎯 Target: Allow GitHub Actions to connect to MySQL${NC}"
    echo ""
}

print_status() {
    echo -e "${YELLOW}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "This script must be run as root (use sudo)"
    exit 1
fi

print_header

# Step 1: Check MySQL service status
print_status "Step 1: Checking MySQL service status..."
if systemctl is-active --quiet mysql; then
    print_success "MySQL service is running"
else
    print_error "MySQL service is not running"
    print_status "Starting MySQL service..."
    systemctl start mysql
    systemctl enable mysql
    print_success "MySQL service started and enabled"
fi

# Step 2: Check MySQL bind-address configuration
print_status "Step 2: Checking MySQL bind-address configuration..."
MYSQL_CONFIG="/etc/mysql/mysql.conf.d/mysqld.cnf"

if [ -f "$MYSQL_CONFIG" ]; then
    BIND_ADDRESS=$(grep -E "^bind-address" "$MYSQL_CONFIG" | awk '{print $3}' | tr -d ' ')
    
    if [ "$BIND_ADDRESS" = "0.0.0.0" ]; then
        print_success "MySQL bind-address is already set to 0.0.0.0"
    else
        print_warning "MySQL bind-address is set to: $BIND_ADDRESS"
        print_status "Updating bind-address to 0.0.0.0..."
        
        # Backup original config
        cp "$MYSQL_CONFIG" "${MYSQL_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
        
        # Update bind-address
        sed -i 's/^bind-address.*=.*/bind-address = 0.0.0.0/' "$MYSQL_CONFIG"
        
        print_success "MySQL bind-address updated to 0.0.0.0"
        print_status "Restarting MySQL service..."
        systemctl restart mysql
        print_success "MySQL service restarted"
    fi
else
    print_error "MySQL configuration file not found: $MYSQL_CONFIG"
    exit 1
fi

# Step 3: Check and configure firewall
print_status "Step 3: Checking firewall configuration..."
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(ufw status | grep -E "Status: (active|inactive)")
    
    if echo "$UFW_STATUS" | grep -q "active"; then
        print_warning "UFW firewall is active"
        print_status "Checking if port 3306 is allowed..."
        
        if ufw status | grep -q "3306"; then
            print_success "Port 3306 is already allowed in UFW"
        else
            print_status "Adding port 3306 to UFW..."
            ufw allow 3306
            print_success "Port 3306 added to UFW"
        fi
        
        # Add GitHub Actions IP ranges
        print_status "Adding GitHub Actions IP ranges to UFW..."
        ufw allow from 140.82.112.0/20 to any port 3306
        ufw allow from 143.55.64.0/20 to any port 3306
        ufw allow from 185.199.108.0/22 to any port 3306
        ufw allow from 192.30.252.0/22 to any port 3306
        print_success "GitHub Actions IP ranges added to UFW"
    else
        print_warning "UFW firewall is inactive"
    fi
else
    print_warning "UFW not found, checking iptables..."
    if iptables -L | grep -q "3306"; then
        print_success "Port 3306 is allowed in iptables"
    else
        print_status "Adding port 3306 to iptables..."
        iptables -A INPUT -p tcp --dport 3306 -j ACCEPT
        print_success "Port 3306 added to iptables"
    fi
fi

# Step 4: Check MySQL user permissions
print_status "Step 4: Checking MySQL user permissions..."
MYSQL_USER="sqa_user"
MYSQL_DB="solutioninn_testing"

# Create temporary SQL file
TEMP_SQL=$(mktemp)
cat > "$TEMP_SQL" << EOF
-- Check if user exists
SELECT user, host FROM mysql.user WHERE user = '$MYSQL_USER';

-- Grant permissions if user doesn't have external access
GRANT ALL PRIVILEGES ON $MYSQL_DB.* TO '$MYSQL_USER'@'%' IDENTIFIED BY 'Hassan123!@#';
FLUSH PRIVILEGES;

-- Verify permissions
SHOW GRANTS FOR '$MYSQL_USER'@'%';
EOF

# Execute SQL commands
if mysql -u root -p -e "source $TEMP_SQL" 2>/dev/null; then
    print_success "MySQL user permissions updated successfully"
else
    print_error "Failed to update MySQL user permissions"
    print_status "Please run the following commands manually:"
    echo "mysql -u root -p"
    echo "GRANT ALL PRIVILEGES ON $MYSQL_DB.* TO '$MYSQL_USER'@'%' IDENTIFIED BY 'Hassan123!@#';"
    echo "FLUSH PRIVILEGES;"
fi

# Clean up temporary file
rm -f "$TEMP_SQL"

# Step 5: Verify MySQL is listening on all interfaces
print_status "Step 5: Verifying MySQL is listening on all interfaces..."
if netstat -tlnp | grep ":3306" | grep -q "0.0.0.0"; then
    print_success "MySQL is listening on all interfaces (0.0.0.0:3306)"
else
    print_error "MySQL is not listening on all interfaces"
    print_status "Current listening addresses:"
    netstat -tlnp | grep ":3306" || true
fi

# Step 6: Test local connection
print_status "Step 6: Testing local database connection..."
if mysql -u "$MYSQL_USER" -p'Hassan123!@#' -h localhost -e "USE $MYSQL_DB; SELECT 1 as test;" 2>/dev/null; then
    print_success "Local database connection successful"
else
    print_error "Local database connection failed"
    print_status "Please check MySQL credentials and database existence"
fi

# Step 7: Final verification
print_status "Step 7: Final verification..."
echo ""
echo -e "${BLUE}📊 VERIFICATION SUMMARY:${NC}"
echo -e "${BLUE}-" * 40${NC}

# Check MySQL status
if systemctl is-active --quiet mysql; then
    echo -e "${GREEN}✅ MySQL service: Running${NC}"
else
    echo -e "${RED}❌ MySQL service: Not running${NC}"
fi

# Check bind-address
if grep -q "bind-address = 0.0.0.0" "$MYSQL_CONFIG"; then
    echo -e "${GREEN}✅ MySQL bind-address: 0.0.0.0${NC}"
else
    echo -e "${RED}❌ MySQL bind-address: Not configured correctly${NC}"
fi

# Check firewall
if command -v ufw &> /dev/null && ufw status | grep -q "3306"; then
    echo -e "${GREEN}✅ Firewall: Port 3306 allowed${NC}"
else
    echo -e "${YELLOW}⚠️ Firewall: Port 3306 status unknown${NC}"
fi

# Check listening
if netstat -tlnp | grep ":3306" | grep -q "0.0.0.0"; then
    echo -e "${GREEN}✅ MySQL listening: All interfaces${NC}"
else
    echo -e "${RED}❌ MySQL listening: Not on all interfaces${NC}"
fi

echo ""
echo -e "${BLUE}🎯 NEXT STEPS:${NC}"
echo "1. Test external connection from your local machine:"
echo "   mysql -u sqa_user -p'Hassan123!@#' -h 18.235.51.183 solutioninn_testing"
echo ""
echo "2. Run GitHub Actions workflow to test connectivity"
echo ""
echo "3. If still failing, check server logs:"
echo "   sudo tail -f /var/log/mysql/error.log"
echo ""

print_success "Database configuration fix completed!"
print_status "GitHub Actions should now be able to connect to your database." 
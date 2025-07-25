#!/usr/bin/env python3
"""
Remote Database Access Analysis
This script analyzes why remote databases are not accessible from GitHub Actions.
"""

import sys
import os
import socket
import subprocess
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_github_actions_network():
    """Check GitHub Actions network configuration"""
    print("🔍 GitHub Actions Network Analysis")
    print("=" * 50)
    
    print("📡 Checking network configuration...")
    
    # Check if we're in GitHub Actions
    if os.getenv('GITHUB_ACTIONS') == 'true':
        print("✅ Running in GitHub Actions environment")
        
        # Check GitHub Actions IP ranges
        print("\n🌐 GitHub Actions IP Information:")
        try:
            # Get GitHub Actions runner IP
            import requests
            response = requests.get('https://api.ipify.org?format=json', timeout=10)
            runner_ip = response.json()['ip']
            print(f"   Runner IP: {runner_ip}")
        except Exception as e:
            print(f"   Could not get runner IP: {e}")
        
        # Check if we can reach external services
        print("\n🔗 Testing external connectivity:")
        test_hosts = [
            ("google.com", 80),
            ("github.com", 443),
            ("18.235.51.183", 3306),  # Your remote database
            ("solutionsole.com", 3306)  # Alternative database
        ]
        
        for host, port in test_hosts:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    print(f"   ✅ {host}:{port} - ACCESSIBLE")
                else:
                    print(f"   ❌ {host}:{port} - NOT ACCESSIBLE (Error code: {result})")
            except Exception as e:
                print(f"   ❌ {host}:{port} - ERROR: {e}")
    else:
        print("❌ Not running in GitHub Actions environment")

def check_database_server_configuration():
    """Check database server configuration"""
    print("\n🗄️ Database Server Configuration Analysis")
    print("=" * 50)
    
    print("🔧 Analyzing remote database configuration...")
    
    # Check if MySQL server allows external connections
    print("\n📋 MySQL Server Configuration Issues:")
    print("   1. bind-address setting - should be 0.0.0.0 or specific IP")
    print("   2. User permissions - user must have external access")
    print("   3. Firewall settings - port 3306 must be open")
    print("   4. MySQL user host restrictions")
    
    print("\n🔍 Common Solutions:")
    print("   1. Update MySQL bind-address in my.cnf:")
    print("      bind-address = 0.0.0.0")
    print("   2. Grant external access to user:")
    print("      GRANT ALL PRIVILEGES ON *.* TO 'sqa_user'@'%' IDENTIFIED BY 'password';")
    print("   3. Check firewall rules:")
    print("      sudo ufw allow 3306")
    print("   4. Restart MySQL service:")
    print("      sudo systemctl restart mysql")

def check_github_actions_ip_ranges():
    """Check GitHub Actions IP ranges"""
    print("\n🌐 GitHub Actions IP Range Analysis")
    print("=" * 50)
    
    print("📋 GitHub Actions uses dynamic IP ranges:")
    print("   - IPs change frequently")
    print("   - Multiple IP ranges are used")
    print("   - No fixed IP addresses")
    
    print("\n🔍 Solution: Allow all IPs or use specific ranges")
    print("   Option 1: Allow all IPs (less secure):")
    print("      GRANT ALL PRIVILEGES ON *.* TO 'sqa_user'@'%';")
    print("   Option 2: Use GitHub Actions IP ranges (more secure):")
    print("      - Check: https://api.github.com/meta")
    print("      - Update MySQL user permissions accordingly")

def check_alternative_solutions():
    """Check alternative solutions"""
    print("\n💡 Alternative Solutions")
    print("=" * 50)
    
    print("🔧 Option 1: Use GitHub Secrets for Database")
    print("   - Store database credentials in GitHub Secrets")
    print("   - Use environment variables in workflow")
    print("   - More secure credential management")
    
    print("\n🔧 Option 2: Use Database Proxy/SSH Tunnel")
    print("   - Set up SSH tunnel to database server")
    print("   - Connect through localhost tunnel")
    print("   - More secure connection method")
    
    print("\n🔧 Option 3: Use Cloud Database Service")
    print("   - Use AWS RDS, Google Cloud SQL, etc.")
    print("   - Better security and accessibility")
    print("   - Managed database service")
    
    print("\n🔧 Option 4: Use GitHub Actions Database Service")
    print("   - Use MySQL service in GitHub Actions")
    print("   - Local database for testing")
    print("   - No external database needed")

def generate_fix_script():
    """Generate fix script for database server"""
    print("\n🔧 Database Server Fix Script")
    print("=" * 50)
    
    fix_script = """#!/bin/bash
# Database Server Configuration Fix Script

echo "🔧 Fixing database server configuration..."

# 1. Update MySQL bind-address
echo "📋 Updating MySQL bind-address..."
sudo sed -i 's/bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf

# 2. Grant external access to user
echo "👤 Granting external access to sqa_user..."
mysql -u root -p -e "
GRANT ALL PRIVILEGES ON solutioninn_testing.* TO 'sqa_user'@'%' IDENTIFIED BY 'Hassan123!@#';
FLUSH PRIVILEGES;
"

# 3. Allow firewall port
echo "🔥 Configuring firewall..."
sudo ufw allow 3306

# 4. Restart MySQL
echo "🔄 Restarting MySQL service..."
sudo systemctl restart mysql

echo "✅ Database server configuration updated!"
echo "🔍 Test connection from external host..."
"""
    
    print("📝 Save this script and run it on your database server:")
    print(fix_script)

def main():
    """Main analysis function"""
    print("🚀 Remote Database Access Analysis")
    print("=" * 60)
    print(f"📅 Analysis Time: {datetime.now()}")
    print("=" * 60)
    
    # Run all analysis functions
    check_github_actions_network()
    check_database_server_configuration()
    check_github_actions_ip_ranges()
    check_alternative_solutions()
    generate_fix_script()
    
    print("\n" + "=" * 60)
    print("📊 ANALYSIS SUMMARY:")
    print("   The main issue is that your remote database server")
    print("   is not configured to accept connections from GitHub Actions.")
    print("   ")
    print("   🔧 RECOMMENDED FIX:")
    print("   1. Run the fix script on your database server")
    print("   2. Update MySQL bind-address to 0.0.0.0")
    print("   3. Grant external access to sqa_user user")
    print("   4. Configure firewall to allow port 3306")
    print("   5. Restart MySQL service")
    print("   ")
    print("   After applying the fix, GitHub Actions should be able")
    print("   to connect to your remote database and store logs there.")

if __name__ == "__main__":
    main() 
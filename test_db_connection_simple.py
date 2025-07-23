#!/usr/bin/env python3
"""
Simple Database Connection Test
Basic connectivity test with minimal dependencies.
"""

import os
import sys
import socket
import mysql.connector
from datetime import datetime

def test_basic_connectivity():
    """Test basic network connectivity to the database host"""
    host = 'solutionsole.com'
    port = 3306
    
    print(f"🔍 Testing basic connectivity to {host}:{port}...")
    
    try:
        # Test if we can reach the host
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)  # 10 second timeout
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Network connectivity to {host}:{port} successful")
            return True
        else:
            print(f"❌ Network connectivity to {host}:{port} failed")
            return False
            
    except Exception as e:
        print(f"❌ Network test failed: {e}")
        return False

def test_database_connection():
    """Test database connection with minimal configuration"""
    
    DB_CONFIG = {
        'host': 'solutionsole.com',
        'user': 'root',
        'password': 'SolutionInn321',
        'database': 'test',
        'connect_timeout': 5,  # 5 second timeout
        'autocommit': True
    }
    
    try:
        print("🔌 Attempting database connection...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("✅ Database connection successful!")
        
        # Simple test query
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        print(f"✅ Test query successful: {result}")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Simple Database Connection Test")
    print(f"📅 Test Time: {datetime.now()}")
    print(f"🖥️ Environment: {os.getenv('GITHUB_ACTIONS', 'Local')}")
    print(f"🗄️ Target Server: solutionsole.com")
    print("")
    
    # Test 1: Basic network connectivity
    network_ok = test_basic_connectivity()
    
    if not network_ok:
        print("")
        print("🚨 Network connectivity failed!")
        print("🔍 Server database troubleshooting:")
        print("   1. SSH into solutionsole.com and check MySQL status:")
        print("      sudo systemctl status mysql")
        print("   2. Check MySQL bind-address in /etc/mysql/mysql.conf.d/mysqld.cnf:")
        print("      bind-address = 0.0.0.0  # Allow external connections")
        print("   3. Check firewall settings:")
        print("      sudo ufw status")
        print("      sudo ufw allow 3306")
        print("   4. Restart MySQL after changes:")
        print("      sudo systemctl restart mysql")
        return False
    
    print("")
    
    # Test 2: Database connection
    db_ok = test_database_connection()
    
    if not db_ok:
        print("")
        print("🚨 Database connection failed!")
        print("🔍 Server database troubleshooting:")
        print("   1. Check MySQL user permissions:")
        print("      mysql -u root -p")
        print("      SELECT user, host FROM mysql.user WHERE user = 'root';")
        print("   2. Grant external access permissions:")
        print("      GRANT ALL PRIVILEGES ON test.* TO 'root'@'%';")
        print("      FLUSH PRIVILEGES;")
        print("   3. Test local connection on server:")
        print("      mysql -u root -p -h localhost test")
        return False
    
    print("")
    print("🎉 All tests passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
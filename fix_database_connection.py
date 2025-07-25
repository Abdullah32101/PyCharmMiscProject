#!/usr/bin/env python3
"""
Database Connection Troubleshooting Script
Helps diagnose and fix database connection issues for GitHub Actions.
"""

import os
import sys
import subprocess
import socket
from datetime import datetime


def check_network_connectivity():
    """Check if we can reach the database server"""
    print("🔍 Checking Network Connectivity...")
    print("=" * 50)
    
    host = "18.235.51.183"
    port = 3306
    
    try:
        # Try to connect to the database port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Network connectivity to {host}:{port} is working")
            return True
        else:
            print(f"❌ Cannot connect to {host}:{port}")
            print(f"🔧 Error code: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Network connectivity test failed: {e}")
        return False


def check_database_config():
    """Check database configuration"""
    print("\n🔍 Checking Database Configuration...")
    print("=" * 50)
    
    config = {
        'host': '18.235.51.183',
        'user': 'sqa_user',
        'password': 'Hassan123!@#',
        'database': 'solutioninn_testing'
    }
    
    print(f"📋 Database Configuration:")
    print(f"   Host: {config['host']}")
    print(f"   User: {config['user']}")
    print(f"   Database: {config['database']}")
    print(f"   Password: {'*' * len(config['password'])}")
    
    # Check if db_config.py exists
    if os.path.exists('db/db_config.py'):
        print("✅ db/db_config.py file exists")
    else:
        print("❌ db/db_config.py file not found")
        return False
    
    return True


def test_mysql_connection():
    """Test MySQL connection directly"""
    print("\n🔍 Testing MySQL Connection...")
    print("=" * 50)
    
    try:
        # Try to connect using mysql command line
        cmd = [
            'mysql', '-h', '18.235.51.183', '-u', 'sqa_user', 
            '-pHassan123!@#', '-e', 'SELECT 1;'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ MySQL connection successful")
            return True
        else:
            print(f"❌ MySQL connection failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ MySQL connection timed out")
        return False
    except FileNotFoundError:
        print("⚠️ MySQL client not installed, skipping direct test")
        return False
    except Exception as e:
        print(f"❌ MySQL connection test failed: {e}")
        return False


def test_python_connection():
    """Test Python database connection"""
    print("\n🔍 Testing Python Database Connection...")
    print("=" * 50)
    
    try:
        import mysql.connector
        
        config = {
            'host': '18.235.51.183',
            'user': 'sqa_user',
            'password': 'Hassan123!@#',
            'database': 'solutioninn_testing',
            'connect_timeout': 10
        }
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        print("✅ Python database connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Python database connection failed: {e}")
        return False


def provide_troubleshooting_steps():
    """Provide troubleshooting steps"""
    print("\n🔧 Troubleshooting Steps")
    print("=" * 50)
    
    print("1. 🔥 Check Firewall Settings:")
    print("   SSH into your database server (18.235.51.183)")
    print("   Run: sudo ufw status")
    print("   If port 3306 is blocked, run: sudo ufw allow 3306")
    
    print("\n2. 🗄️ Check MySQL Configuration:")
    print("   Check MySQL bind-address:")
    print("   sudo grep bind-address /etc/mysql/mysql.conf.d/mysqld.cnf")
    print("   Ensure it shows: bind-address = 0.0.0.0")
    
    print("\n3. 🔄 Restart MySQL Service:")
    print("   sudo systemctl restart mysql")
    print("   sudo systemctl status mysql")
    
    print("\n4. 👤 Check User Permissions:")
    print("   Connect to MySQL as root:")
    print("   mysql -u root -p")
    print("   GRANT ALL PRIVILEGES ON solutioninn_testing.* TO 'sqa_user'@'%';")
    print("   FLUSH PRIVILEGES;")
    
    print("\n5. 🌐 Check Network Configuration:")
    print("   Ensure your server allows external connections")
    print("   Check if the server is behind a NAT or proxy")
    
    print("\n6. 🔍 Alternative Solutions:")
    print("   - Use a different database server")
    print("   - Set up a local database for testing")
    print("   - Use a cloud database service")


def create_local_test_config():
    """Create a local test configuration"""
    print("\n🔧 Creating Local Test Configuration...")
    print("=" * 50)
    
    # Create a simple test config that doesn't require external database
    test_config = '''# Local Test Configuration
# This configuration allows tests to run without external database

DB_CONFIG = {
    'host': 'localhost',
    'user': 'test_user',
    'password': 'test_password',
    'database': 'test_db'
}

# For GitHub Actions, you might want to use a different approach
if os.getenv('GITHUB_ACTIONS'):
    print("⚠️ Running in GitHub Actions - database storage disabled")
    DB_CONFIG = None
'''
    
    try:
        with open('db/test_config.py', 'w') as f:
            f.write(test_config)
        print("✅ Created db/test_config.py for local testing")
    except Exception as e:
        print(f"❌ Failed to create test config: {e}")


def main():
    """Main troubleshooting function"""
    print("🔧 Database Connection Troubleshooting")
    print("=" * 60)
    print(f"📅 Time: {datetime.now()}")
    print(f"🖥️ Environment: {'GitHub Actions' if os.getenv('GITHUB_ACTIONS') else 'Local'}")
    print("=" * 60)
    
    # Run all checks
    network_ok = check_network_connectivity()
    config_ok = check_database_config()
    mysql_ok = test_mysql_connection()
    python_ok = test_python_connection()
    
    # Summary
    print("\n📊 Troubleshooting Summary")
    print("=" * 50)
    print(f"🌐 Network Connectivity: {'✅' if network_ok else '❌'}")
    print(f"📋 Configuration: {'✅' if config_ok else '❌'}")
    print(f"🗄️ MySQL Connection: {'✅' if mysql_ok else '❌'}")
    print(f"🐍 Python Connection: {'✅' if python_ok else '❌'}")
    
    if all([network_ok, config_ok, mysql_ok, python_ok]):
        print("\n🎉 All checks passed! Database should be working.")
    else:
        print("\n❌ Some checks failed. See troubleshooting steps below.")
        provide_troubleshooting_steps()
        create_local_test_config()
    
    print("\n💡 Recommendations:")
    if os.getenv('GITHUB_ACTIONS'):
        print("1. For GitHub Actions, consider using a cloud database service")
        print("2. Or set up a database server that allows external connections")
        print("3. Use environment variables for database credentials")
    else:
        print("1. Check your local MySQL installation")
        print("2. Ensure the database server is running")
        print("3. Verify network connectivity to the server")


if __name__ == "__main__":
    main() 
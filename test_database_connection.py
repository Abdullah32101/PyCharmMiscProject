#!/usr/bin/env python3
"""
Simple Database Connection Test
Tests connectivity to the database server.
"""

import socket
import mysql.connector
from datetime import datetime


def test_network_connectivity():
    """Test basic network connectivity"""
    print("🔍 Testing Network Connectivity...")
    print("=" * 40)
    
    host = "18.235.51.183"
    port = 3306
    
    try:
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


def test_mysql_connection():
    """Test MySQL connection"""
    print("\n🔍 Testing MySQL Connection...")
    print("=" * 40)
    
    config = {
        'host': '18.235.51.183',
        'user': 'sqa_user',
        'password': 'Hassan123!@#',
        'database': 'solutioninn_testing',
        'connect_timeout': 10
    }
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        print("✅ MySQL connection successful")
        print(f"📊 Test query result: {result}")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_database_operations():
    """Test basic database operations"""
    print("\n🔍 Testing Database Operations...")
    print("=" * 40)
    
    config = {
        'host': '18.235.51.183',
        'user': 'sqa_user',
        'password': 'Hassan123!@#',
        'database': 'solutioninn_testing',
        'connect_timeout': 10
    }
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Test creating a table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id INT AUTO_INCREMENT PRIMARY KEY,
                test_time DATETIME,
                status VARCHAR(50)
            )
        """)
        
        # Test inserting data
        cursor.execute("""
            INSERT INTO connection_test (test_time, status) 
            VALUES (%s, %s)
        """, (datetime.now(), "connection_test"))
        
        # Test selecting data
        cursor.execute("SELECT COUNT(*) FROM connection_test")
        count = cursor.fetchone()[0]
        
        # Test updating data
        cursor.execute("""
            UPDATE connection_test 
            SET status = 'updated' 
            WHERE status = 'connection_test'
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✅ Database operations successful")
        print(f"📊 Records in test table: {count}")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Database operations failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Main test function"""
    print("🔧 Database Connection Test")
    print("=" * 50)
    print(f"📅 Time: {datetime.now()}")
    print(f"🌐 Target: 18.235.51.183:3306")
    print("=" * 50)
    
    # Run all tests
    network_ok = test_network_connectivity()
    mysql_ok = test_mysql_connection()
    operations_ok = test_database_operations()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    print(f"🌐 Network Connectivity: {'✅' if network_ok else '❌'}")
    print(f"🗄️ MySQL Connection: {'✅' if mysql_ok else '❌'}")
    print(f"🔧 Database Operations: {'✅' if operations_ok else '❌'}")
    
    if all([network_ok, mysql_ok, operations_ok]):
        print("\n🎉 All tests passed! Database is working correctly.")
        print("✅ Your test suites should now be able to connect to the database.")
    else:
        print("\n❌ Some tests failed. Please fix the database server configuration.")
        print("\n🔧 To fix the database server, run these commands on 18.235.51.183:")
        print("1. SSH into the server: ssh root@18.235.51.183")
        print("2. Run the fix script: sudo bash fix_server_database.sh")
        print("3. Or manually fix:")
        print("   - sudo ufw allow 3306")
        print("   - Edit /etc/mysql/mysql.conf.d/mysqld.cnf")
        print("   - Set bind-address = 0.0.0.0")
        print("   - sudo systemctl restart mysql")
        print("   - Create user and grant permissions")


if __name__ == "__main__":
    main() 
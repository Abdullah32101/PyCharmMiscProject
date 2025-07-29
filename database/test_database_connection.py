#!/usr/bin/env python3
"""
Database Connection Test Script
Tests database connectivity with flexible configuration
"""

import os
import sys
import time
import socket
import mysql.connector
from mysql.connector import Error
from db.db_config import get_database_config, is_github_actions

def test_network_connectivity(host, port, timeout=5):
    """Test basic network connectivity"""
    print(f"🔍 Testing Network Connectivity...")
    print("=" * 40)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
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

def test_mysql_connection(config):
    """Test MySQL connection with the given configuration"""
    print(f"🔍 Testing MySQL Connection...")
    print("=" * 40)
    
    try:
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            print("✅ MySQL connection successful")
            print(f"📊 Test query result: {result}")
            return True
        else:
            print("❌ MySQL connection failed")
            return False
            
    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

def test_database_operations(config):
    """Test basic database operations"""
    print(f"🔍 Testing Database Operations...")
    print("=" * 40)
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Test creating a table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS connection_test (
            id INT AUTO_INCREMENT PRIMARY KEY,
            test_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(50)
        )
        """
        cursor.execute(create_table_query)
        
        # Test inserting data
        insert_query = "INSERT INTO connection_test (status) VALUES (%s)"
        cursor.execute(insert_query, ("connection_test",))
        connection.commit()
        
        # Test reading data
        cursor.execute("SELECT COUNT(*) FROM connection_test")
        count = cursor.fetchone()[0]
        
        cursor.close()
        connection.close()
        
        print("✅ Database operations successful")
        print(f"📊 Records in test table: {count}")
        return True
        
    except Error as e:
        print(f"❌ Database operations failed: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 Database Connection Test")
    print("=" * 50)
    print(f"📅 Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get database configuration
    config = get_database_config()
    
    print(f"🌐 Target: {config['host']}:{config['port']}")
    print("=" * 50)
    
    # Test network connectivity
    network_ok = test_network_connectivity(config['host'], config['port'])
    
    # Test MySQL connection
    mysql_ok = test_mysql_connection(config)
    
    # Test database operations
    operations_ok = test_database_operations(config)
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    print(f"🌐 Network Connectivity: {'✅' if network_ok else '❌'}")
    print(f"🗄️ MySQL Connection: {'✅' if mysql_ok else '❌'}")
    print(f"🔧 Database Operations: {'✅' if operations_ok else '❌'}")
    
    if all([network_ok, mysql_ok, operations_ok]):
        print("\n🎉 All tests passed! Database is working correctly.")
        print("✅ Your test suites should now be able to connect to the database.")
        return 0
    else:
        print("\n❌ Some tests failed. Check the configuration and network connectivity.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 
#!/usr/bin/env python3
"""
Remote Database Connection Test
This script tests connection to remote databases and shows detailed information.
"""

import sys
import os
import socket
import mysql.connector
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_network_connectivity(host, port, timeout=10):
    """Test basic network connectivity"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"   ❌ Network error: {e}")
        return False

def test_mysql_connection(host, user, password, database, port=3306):
    """Test MySQL connection"""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            autocommit=True,
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return True, result
    except Exception as e:
        return False, str(e)

def test_database_operations(host, user, password, database, port=3306):
    """Test database operations"""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            autocommit=True,
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # Test table creation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id INT AUTO_INCREMENT PRIMARY KEY,
                test_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                test_message VARCHAR(255)
            )
        """)
        
        # Test insert
        cursor.execute("""
            INSERT INTO connection_test (test_message) 
            VALUES (%s)
        """, (f"Connection test at {datetime.now()}",))
        
        # Test select
        cursor.execute("SELECT COUNT(*) FROM connection_test")
        count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return True, count
    except Exception as e:
        return False, str(e)

def main():
    """Main test function"""
    print("🚀 Remote Database Connection Test")
    print("=" * 60)
    print(f"📅 Test Time: {datetime.now()}")
    print(f"🖥️ Environment: {'GitHub Actions' if os.getenv('GITHUB_ACTIONS') else 'Local'}")
    print("=" * 60)
    
    # Database configurations to test
    databases = [
        {
            "name": "Primary Remote Database",
            "host": "18.235.51.183",
            "user": "sqa_user",
            "password": "Hassan123!@#",
            "database": "solutioninn_testing",
            "port": 3306
        },
        {
            "name": "Alternative Remote Database",
            "host": "solutionsole.com",
            "user": "root",
            "password": "SolutionInn321",
            "database": "test",
            "port": 3306
        },
        {
            "name": "Local Test Database",
            "host": "127.0.0.1",
            "user": "root",
            "password": "root",
            "database": "test_results",
            "port": 3306
        }
    ]
    
    working_databases = []
    
    for db in databases:
        print(f"\n🔍 Testing: {db['name']}")
        print(f"   Host: {db['host']}:{db['port']}")
        print(f"   Database: {db['database']}")
        print(f"   User: {db['user']}")
        
        # Test 1: Network connectivity
        print("   📡 Testing network connectivity...")
        if test_network_connectivity(db['host'], db['port']):
            print("   ✅ Network connectivity: WORKING")
            
            # Test 2: MySQL connection
            print("   🗄️ Testing MySQL connection...")
            mysql_ok, mysql_result = test_mysql_connection(
                db['host'], db['user'], db['password'], db['database'], db['port']
            )
            
            if mysql_ok:
                print(f"   ✅ MySQL connection: WORKING (Result: {mysql_result})")
                
                # Test 3: Database operations
                print("   🔧 Testing database operations...")
                ops_ok, ops_result = test_database_operations(
                    db['host'], db['user'], db['password'], db['database'], db['port']
                )
                
                if ops_ok:
                    print(f"   ✅ Database operations: WORKING (Records: {ops_result})")
                    working_databases.append(db)
                    print(f"   🎉 {db['name']} is FULLY WORKING!")
                else:
                    print(f"   ❌ Database operations: FAILED - {ops_result}")
            else:
                print(f"   ❌ MySQL connection: FAILED - {mysql_result}")
        else:
            print("   ❌ Network connectivity: FAILED")
        
        print("   " + "-" * 40)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 CONNECTION TEST SUMMARY:")
    print(f"   Databases Tested: {len(databases)}")
    print(f"   Working Databases: {len(working_databases)}")
    
    if working_databases:
        print("\n✅ WORKING DATABASES:")
        for db in working_databases:
            print(f"   - {db['name']} ({db['host']}:{db['port']})")
        
        print("\n🎉 At least one database is working!")
        print("   Your test suite can use any of the working databases.")
    else:
        print("\n❌ NO DATABASES ARE WORKING!")
        print("   Please check:")
        print("   - Network connectivity")
        print("   - Database credentials")
        print("   - Firewall settings")
        print("   - Database server status")
    
    return len(working_databases) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
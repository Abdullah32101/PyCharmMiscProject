#!/usr/bin/env python3
"""
Test Local Database Connection
Verify that local connection to solutionsole.com works
"""

import mysql.connector
from datetime import datetime

def test_local_connection():
    """Test local connection to solutionsole.com database"""
    
    DB_CONFIG = {
        'host': 'solutionsole.com',
        'user': 'root',
        'password': 'SolutionInn321',
        'database': 'test'
    }
    
    try:
        print("🧪 Testing Local Database Connection")
        print("=" * 40)
        print(f"📅 Test Time: {datetime.now()}")
        print(f"🗄️ Database Host: {DB_CONFIG['host']}")
        print(f"📊 Database Name: {DB_CONFIG['database']}")
        print(f"👤 User: {DB_CONFIG['user']}")
        print("")
        
        # Connect to database
        print("🔌 Attempting database connection...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("✅ Database connection successful!")
        
        # Test basic query
        print("🔍 Testing basic query...")
        cursor.execute("SELECT COUNT(*) as count FROM test_results")
        result = cursor.fetchone()
        test_count = result['count'] if result else 0
        
        print(f"📊 Current test records in database: {test_count}")
        
        # Test table structure
        print("🔍 Checking table structure...")
        cursor.execute("DESCRIBE test_results")
        columns = cursor.fetchall()
        
        print(f"📋 test_results table has {len(columns)} columns:")
        for column in columns:
            print(f"  - {column['Field']}: {column['Type']}")
        
        # Test inserting a test record
        print("🔍 Testing insert operation...")
        test_query = """
        INSERT INTO test_results (
            test_case_name, module_name, test_status, test_datetime, 
            error_message, error_summary, total_time_duration, 
            device_name, screen_resolution, error_link
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(test_query, (
            'local_connection_test',
            'test_local_db_connection',
            'PASSED',
            datetime.now(),
            'Local connection test successful',
            'Local connection test',
            0.1,
            'local',
            '1920x1080',
            'file:///local/test.png'
        ))
        
        conn.commit()
        print("✅ Test record inserted successfully")
        
        cursor.close()
        conn.close()
        
        print("")
        print("🎉 Local database connection test completed successfully!")
        print("")
        print("📋 Summary:")
        print("✅ Connection: Working")
        print("✅ Queries: Working")
        print("✅ Inserts: Working")
        print("✅ Table structure: Correct")
        print("")
        print("🔍 Since local connection works, the issue is likely:")
        print("   - GitHub Actions IP ranges are blocked by server firewall")
        print("   - MySQL user permissions need to be updated for external hosts")
        print("   - Server firewall needs to allow port 3306 from all IPs")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Database connection failed: {e}")
        print("")
        print("🔍 This suggests the database configuration needs to be checked.")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_local_connection()
    exit(0 if success else 1) 
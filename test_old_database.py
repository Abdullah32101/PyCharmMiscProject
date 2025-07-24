#!/usr/bin/env python3
"""
Test Old Database Connection
"""

import mysql.connector

# Old database configuration
OLD_DB_CONFIG = {
    "host": "solutionsole.com",
    "user": "root",
    "password": "SolutionInn321",
    "database": "test",
}

def test_old_connection():
    """Test connection to old database"""
    try:
        print("🔌 Testing old database connection...")
        conn = mysql.connector.connect(**OLD_DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Test basic query
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        print("✅ Old database connection successful")
        
        # Check if test_results table exists
        cursor.execute("SHOW TABLES LIKE 'test_results'")
        result = cursor.fetchone()
        
        if result:
            print("✅ test_results table found in old database")
            
            # Get record count
            cursor.execute("SELECT COUNT(*) as count FROM test_results")
            count_result = cursor.fetchone()
            record_count = count_result['count'] if count_result else 0
            print(f"📊 Old database has {record_count} test results records")
            
        else:
            print("❌ test_results table not found in old database")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Old database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_old_connection() 
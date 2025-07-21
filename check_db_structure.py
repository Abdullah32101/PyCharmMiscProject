#!/usr/bin/env python3
"""
Script to check database structure and verify error_link column
"""

import mysql.connector
from db.db_config import DB_CONFIG

def check_database_structure():
    """Check if error_link column exists in test_results table"""
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("DESCRIBE test_results")
        columns = cursor.fetchall()
        
        print("📋 Current test_results table structure:")
        print("-" * 50)
        
        error_link_exists = False
        for column in columns:
            if isinstance(column, (list, tuple)) and len(column) >= 3:
                column_name = str(column[0])
                column_type = str(column[1])
                column_null = str(column[2]) if column[2] else ""
                print(f"  - {column_name}: {column_type} {column_null}")
                
                if column_name == 'error_link':
                    error_link_exists = True
        
        print("-" * 50)
        
        if error_link_exists:
            print("✅ error_link column exists in test_results table")
        else:
            print("❌ error_link column NOT found in test_results table")
        
        # Check recent test results
        cursor.execute("SELECT test_case_name, test_status, error_link FROM test_results ORDER BY id DESC LIMIT 5")
        results = cursor.fetchall()
        
        print("\n📊 Recent test results:")
        print("-" * 50)
        for result in results:
            if isinstance(result, (list, tuple)) and len(result) >= 3:
                test_name = str(result[0])
                status = str(result[1])
                error_link = str(result[2]) if result[2] else "None"
                print(f"  - {test_name}: {status} | Error Link: {error_link}")
            else:
                print(f"  - {result}")
        
        cursor.close()
        conn.close()
        
        return error_link_exists
        
    except Exception as e:
        print(f"❌ Error checking database structure: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking Database Structure")
    print("=" * 50)
    check_database_structure() 
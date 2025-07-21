#!/usr/bin/env python3
"""
Add new columns to test_results table:
1. total_time_duration - stores test execution duration
2. device_name - stores device type (mobile/desktop)
"""

import mysql.connector
from db.db_config import DB_CONFIG

def add_test_columns():
    """Add total_time_duration and device_name columns to test_results table"""
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(buffered=True)
    
    try:
        # Check if total_time_duration column exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'test_results' 
            AND COLUMN_NAME = 'total_time_duration'
        """)
        
        result = cursor.fetchone()
        count = result[0] if result else 0
        if count == 0:
            # Add total_time_duration column
            cursor.execute("""
                ALTER TABLE test_results 
                ADD COLUMN total_time_duration DECIMAL(10,3) NULL COMMENT 'Test execution time in seconds'
            """)
            print("✅ Added total_time_duration column to test_results table")
        else:
            print("✅ total_time_duration column already exists in test_results table")
        
        # Check if device_name column exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'test_results' 
            AND COLUMN_NAME = 'device_name'
        """)
        
        result = cursor.fetchone()
        count = result[0] if result else 0
        if count == 0:
            # Add device_name column
            cursor.execute("""
                ALTER TABLE test_results 
                ADD COLUMN device_name VARCHAR(50) NULL COMMENT 'Device type (mobile/desktop/tablet)'
            """)
            print("✅ Added device_name column to test_results table")
        else:
            print("✅ device_name column already exists in test_results table")
        
        conn.commit()
        print("✅ Database schema updated successfully!")
        
    except Exception as e:
        print(f"❌ Error updating database schema: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_test_columns() 
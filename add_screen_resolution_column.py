#!/usr/bin/env python3
"""
Add screen_resolution column to test_results table
"""

import mysql.connector
from db.db_config import DB_CONFIG


def add_screen_resolution_column():
    """Add screen_resolution column to test_results table"""
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Check if screen_resolution column exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'test_results' 
            AND COLUMN_NAME = 'screen_resolution'
        """)
        
        result = cursor.fetchone()
        count = result[0] if result else 0
        if count == 0:
            # Add screen_resolution column
            cursor.execute("""
                ALTER TABLE test_results 
                ADD COLUMN screen_resolution VARCHAR(50) NULL COMMENT 'Screen resolution (e.g., 1920x1080, 375x812)'
            """)
            print("✅ Added screen_resolution column to test_results table")
        else:
            print("✅ screen_resolution column already exists in test_results table")
        
        conn.commit()
        print("✅ Database schema updated successfully!")
        
    except Exception as e:
        print(f"❌ Error updating database schema: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_screen_resolution_column() 
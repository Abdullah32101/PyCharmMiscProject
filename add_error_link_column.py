#!/usr/bin/env python3
"""
Script to add error_link column to existing test_results table
"""

import mysql.connector
from db.db_config import DB_CONFIG
import os

def add_error_link_column():
    """Add error_link column to test_results table if it doesn't exist"""
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'test_results' 
            AND COLUMN_NAME = 'error_link'
        """)
        
        column_exists = cursor.fetchone()
        
        if not column_exists:
            # Add the new column
            alter_query = """
            ALTER TABLE test_results 
            ADD COLUMN error_link VARCHAR(500) NULL 
            COMMENT 'URL link to screenshot showing affected screen'
            """
            
            cursor.execute(alter_query)
            conn.commit()
            print("✅ Successfully added error_link column to test_results table")
        else:
            print("ℹ️ error_link column already exists in test_results table")
        
        # Verify the column was added
        cursor.execute("DESCRIBE test_results")
        columns = cursor.fetchall()
        
        print("\n📋 Current test_results table structure:")
        for column in columns:
            if isinstance(column, (list, tuple)) and len(column) >= 3:
                column_name = str(column[0])
                column_type = str(column[1])
                column_null = str(column[2]) if column[2] else ""
                print(f"  - {column_name}: {column_type} {column_null}")
            else:
                print(f"  - {column}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error adding error_link column: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    add_error_link_column() 
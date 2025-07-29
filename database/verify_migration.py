#!/usr/bin/env python3
"""
Verify Migration Success
"""

import mysql.connector
from db.db_config import DB_CONFIG

def verify_migration():
    """Verify that the migration was successful"""
    try:
        print("🔍 Verifying migration...")
        
        # Connect to new database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Check record count in new database
        cursor.execute("SELECT COUNT(*) as count FROM test_results")
        new_count = cursor.fetchone()['count']
        
        print(f"📊 New database has {new_count} test results records")
        
        if new_count > 0:
            print("✅ Migration appears to be successful!")
            
            # Show some sample records
            cursor.execute("SELECT test_case_name, test_status, test_datetime FROM test_results ORDER BY id DESC LIMIT 5")
            recent_records = cursor.fetchall()
            
            print("\n📋 Recent test results:")
            for i, record in enumerate(recent_records, 1):
                print(f"   {i}. {record['test_case_name']} - {record['test_status']} ({record['test_datetime']})")
        else:
            print("❌ No records found in new database")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")

if __name__ == "__main__":
    verify_migration() 
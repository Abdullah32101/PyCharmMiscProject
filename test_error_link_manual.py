#!/usr/bin/env python3
"""
Manual test to verify error link storage and retrieval
"""

import mysql.connector
from db.db_config import DB_CONFIG
from datetime import datetime

def test_error_link_manual():
    """Manually test error link storage and retrieval"""
    
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Test data
        test_name = "manual_error_link_test"
        error_link = "file:///test/path/screenshot.png"
        
        # Insert test result with error link
        insert_query = """
        INSERT INTO test_results (
            test_case_name, module_name, test_status, test_datetime, 
            error_message, error_summary, total_time_duration, 
            device_name, screen_resolution, error_link
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            test_name,
            "manual_test",
            "FAILED",
            datetime.now(),
            "Manual test error message",
            "Manual test error",
            1.5,
            "desktop",
            "1920x1080",
            error_link
        ))
        
        conn.commit()
        print(f"[✅] Inserted test result with error link: {error_link}")
        
        # Query the inserted record
        select_query = """
        SELECT test_case_name, test_status, error_link 
        FROM test_results 
        WHERE test_case_name = %s 
        ORDER BY id DESC 
        LIMIT 1
        """
        
        cursor.execute(select_query, (test_name,))
        result = cursor.fetchone()
        
        if result:
            print(f"[🔍] Retrieved test result:")
            print(f"  - Test Name: {result['test_case_name']}")
            print(f"  - Status: {result['test_status']}")
            print(f"  - Error Link: {result['error_link']}")
            
            if result['error_link'] == error_link:
                print("[✅] Error link storage and retrieval working correctly!")
                return True
            else:
                print(f"[❌] Error link mismatch: expected {error_link}, got {result['error_link']}")
                return False
        else:
            print("[❌] No test result found")
            return False
            
    except Exception as e:
        print(f"[❌] Error in manual test: {e}")
        return False
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

def check_all_error_links():
    """Check all test results with error links"""
    
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Query all test results with error links
        select_query = """
        SELECT test_case_name, test_status, error_link, test_datetime
        FROM test_results 
        WHERE error_link IS NOT NULL AND error_link != ''
        ORDER BY test_datetime DESC
        """
        
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        print(f"\n📊 Test results with error links ({len(results)} found):")
        print("-" * 60)
        
        for result in results:
            print(f"  - {result['test_case_name']}: {result['test_status']}")
            print(f"    Error Link: {result['error_link']}")
            print(f"    DateTime: {result['test_datetime']}")
            print()
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"[❌] Error checking error links: {e}")

if __name__ == "__main__":
    print("🧪 Manual Error Link Test")
    print("=" * 50)
    
    # Run manual test
    success = test_error_link_manual()
    
    if success:
        print("\n🎉 Manual test passed!")
    else:
        print("\n❌ Manual test failed!")
    
    # Check all error links
    check_all_error_links() 
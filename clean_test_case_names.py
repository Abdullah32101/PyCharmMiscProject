#!/usr/bin/env python3
"""
Script to clean up test case names in the database by removing device information
"""

import mysql.connector
from db.db_config import DB_CONFIG
import re

def clean_test_case_names():
    """Clean up test case names by removing device information"""
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Get all test results with device information in test case names
        select_query = """
        SELECT id, test_case_name 
        FROM test_results 
        WHERE test_case_name LIKE '%[%]%'
        ORDER BY id
        """
        
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        print(f"🔍 Found {len(results)} test results with device information in names")
        print("=" * 60)
        
        cleaned_count = 0
        
        for result in results:
            if isinstance(result, (list, tuple)) and len(result) >= 2:
                test_id = int(result[0])
                original_name = str(result[1])
                
                # Remove device information from test case name
                # Pattern: test_name[device] -> test_name
                cleaned_name = re.sub(r'\[.*?\]', '', original_name)
                
                # Remove any trailing spaces or underscores
                cleaned_name = cleaned_name.strip(' _')
                
                print(f"ID: {test_id}")
                print(f"  Original: {original_name}")
                print(f"  Cleaned:  {cleaned_name}")
                
                # Update the database
                update_query = """
                UPDATE test_results 
                SET test_case_name = %s 
                WHERE id = %s
                """
                
                cursor.execute(update_query, (cleaned_name, test_id))
                cleaned_count += 1
        
        # Commit the changes
        conn.commit()
        
        print("=" * 60)
        print(f"✅ Successfully cleaned {cleaned_count} test case names")
        
        # Show some examples of cleaned results
        cursor.execute("""
        SELECT test_case_name, test_status, device_name, screen_resolution 
        FROM test_results 
        ORDER BY id DESC 
        LIMIT 10
        """)
        
        recent_results = cursor.fetchall()
        
        print("\n📊 Recent test results after cleaning:")
        print("-" * 60)
        for result in recent_results:
            if isinstance(result, (list, tuple)) and len(result) >= 4:
                test_name = str(result[0]) if result[0] else "unknown"
                status = str(result[1]) if result[1] else "unknown"
                device = str(result[2]) if result[2] else "unknown"
                resolution = str(result[3]) if result[3] else "unknown"
                print(f"  - {test_name}: {status} | Device: {device} | Resolution: {resolution}")
        
        cursor.close()
        conn.close()
        
        return cleaned_count
        
    except Exception as e:
        print(f"❌ Error cleaning test case names: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return 0

def verify_cleanup():
    """Verify that no test case names contain device information"""
    try:
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check for any remaining test case names with device information
        check_query = """
        SELECT COUNT(*) 
        FROM test_results 
        WHERE test_case_name LIKE '%[%]%'
        """
        
        cursor.execute(check_query)
        count_result = cursor.fetchone()
        count = int(count_result[0]) if count_result and count_result[0] else 0
        
        if count == 0:
            print("✅ Verification passed: No test case names contain device information")
        else:
            print(f"⚠️ Warning: {count} test case names still contain device information")
            
            # Show the problematic names
            cursor.execute("""
            SELECT test_case_name 
            FROM test_results 
            WHERE test_case_name LIKE '%[%]%'
            LIMIT 5
            """)
            
            problematic = cursor.fetchall()
            print("Problematic names:")
            for name in problematic:
                if isinstance(name, (list, tuple)) and len(name) > 0:
                    print(f"  - {name[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")

if __name__ == "__main__":
    print("🧹 Cleaning Test Case Names")
    print("=" * 50)
    
    # Clean the test case names
    cleaned_count = clean_test_case_names()
    
    if cleaned_count > 0:
        print(f"\n🔍 Verifying cleanup...")
        verify_cleanup()
    
    print("\n🎉 Test case name cleanup completed!") 
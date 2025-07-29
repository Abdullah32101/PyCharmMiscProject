#!/usr/bin/env python3
"""
Check Database Status
Simple script to check current database status and recent test results.
"""

import mysql.connector
from datetime import datetime

def check_database_status():
    """Check current database status and recent test results"""
    
    DB_CONFIG = {
        'host': 'solutionsole.com',
        'user': 'root',
        'password': 'SolutionInn321',
        'database': 'test'
    }
    
    try:
        print("🔍 Checking Database Status")
        print("=" * 40)
        print(f"📅 Check Time: {datetime.now()}")
        print(f"🗄️ Database: {DB_CONFIG['host']}")
        print("")
        
        # Connect to database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        print("✅ Database connection successful!")
        
        # Check total test records
        cursor.execute("SELECT COUNT(*) as count FROM test_results")
        result = cursor.fetchone()
        total_records = result['count'] if result else 0
        
        print(f"📊 Total test records: {total_records}")
        
        # Check recent test results (last 5)
        cursor.execute("""
            SELECT test_case_name, test_status, created_at, device_name, screen_resolution 
            FROM test_results 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        recent_tests = cursor.fetchall()
        
        print(f"\n📋 Recent Test Results (Last 5):")
        print("-" * 60)
        
        if recent_tests:
            for test in recent_tests:
                status_icon = "✅" if test['test_status'] == 'PASSED' else "❌"
                device_icon = "🖥️" if "desktop" in str(test['device_name']).lower() else "📱"
                print(f"{status_icon} {test['test_case_name']}")
                print(f"   Status: {test['test_status']}")
                print(f"   Device: {device_icon} {test['device_name']} ({test['screen_resolution']})")
                print(f"   Time: {test['created_at']}")
                print("")
        else:
            print("No test records found.")
        
        # Check test statistics
        cursor.execute("""
            SELECT 
                test_status,
                COUNT(*) as count
            FROM test_results 
            GROUP BY test_status
        """)
        stats = cursor.fetchall()
        
        print("📈 Test Statistics:")
        print("-" * 30)
        for stat in stats:
            icon = "✅" if stat['test_status'] == 'PASSED' else "❌"
            percentage = (stat['count'] / total_records * 100) if total_records > 0 else 0
            print(f"{icon} {stat['test_status']}: {stat['count']} ({percentage:.1f}%)")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Database status check completed!")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Database connection failed: {e}")
        print(f"🔍 Error Code: {e.errno}")
        print(f"🔍 Error Message: {e.msg}")
        
        # Provide troubleshooting information
        print("\n🔧 TROUBLESHOOTING SUGGESTIONS:")
        print("-" * 40)
        print("1. Check if database server is running")
        print("2. Verify firewall allows connections from GitHub Actions")
        print("3. Check if database accepts remote connections")
        print("4. Verify credentials and database name")
        print("5. Check network connectivity")
        
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"🔍 Error Type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    check_database_status() 
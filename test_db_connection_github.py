#!/usr/bin/env python3
"""
Test Database Connection for GitHub Actions
Simple script to verify database connectivity in CI/CD environment.
"""

import os
import sys
import signal
import mysql.connector
from datetime import datetime

def timeout_handler(signum, frame):
    """Handle timeout signal"""
    print("❌ Database connection timed out after 30 seconds")
    print("🔍 Possible issues:")
    print("   - 18.235.51.183 is not accessible from GitHub Actions")
    print("   - Database server is down or not responding")
    print("   - Firewall blocking connections from GitHub IP ranges")
    sys.exit(1)

def test_github_db_connection():
    """Test database connection in GitHub Actions environment with timeout"""
    
    # Set timeout for database connection (30 seconds)
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(30)
    
    # Database configuration for GitHub Actions
    DB_CONFIG = {
        'host': '18.235.51.183',
        'user': 'sqa_user',
        'password': 'Hassan123!@#',
        'database': 'solutioninn_testing',
        'connect_timeout': 10,  # 10 second connection timeout
        'autocommit': True
    }
    
    try:
        print("🔧 Testing database connection in GitHub Actions...")
        print(f"📅 Test Time: {datetime.now()}")
        print(f"🖥️ Environment: {os.getenv('GITHUB_ACTIONS', 'Local')}")
        print(f"🗄️ Database Host: {DB_CONFIG['host']}")
        print(f"📊 Database Name: {DB_CONFIG['database']}")
        print(f"⏱️ Timeout: 30 seconds")
        print("")
        
        # Connect to database
        print("🔌 Attempting database connection...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Cancel the alarm since connection succeeded
        signal.alarm(0)
        
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
        
        cursor.close()
        conn.close()
        
        print("")
        print("🎉 Database connection test completed successfully!")
        return True
        
    except mysql.connector.Error as e:
        signal.alarm(0)  # Cancel alarm
        print(f"❌ Database connection failed: {e}")
        print("")
        print("🔍 Troubleshooting tips:")
        print("1. Check if 18.235.51.183 is accessible from GitHub Actions")
        print("2. Verify database credentials are correct")
        print("3. Ensure database server allows external connections")
        print("4. Check firewall settings on the database server")
        print("5. Verify MySQL is running and accepting connections on port 3306")
        return False
        
    except Exception as e:
        signal.alarm(0)  # Cancel alarm
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_github_db_connection()
    sys.exit(0 if success else 1) 
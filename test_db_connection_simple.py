#!/usr/bin/env python3
"""
Simple Database Connection Test
This script tests the database connection and verifies that logs can be stored.
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Test database connection and basic logging"""
    print("🔧 Testing Database Connection and Logging")
    print("=" * 50)
    
    try:
        from db.db_helper import MySQLHelper
        
        # Initialize database helper
        print("📡 Connecting to database...")
        db_helper = MySQLHelper()
        
        # Create test results table if it doesn't exist
        print("📋 Creating test results table...")
        db_helper.create_test_results_table()
        
        # Get current test count
        initial_results = db_helper.get_test_results(limit=10)
        initial_count = len(initial_results)
        print(f"📊 Current test results in database: {initial_count}")
        
        # Store a test log entry
        test_message = f"""
Database Connection Test
Timestamp: {datetime.now()}
Purpose: Verify database logging functionality
Status: PASSED
Environment: GitHub Actions
        """
        
        print("💾 Storing test log in database...")
        db_helper.store_test_result_in_tables(
            test_case_name="database_connection_test",
            module_name="test_db_connection_simple",
            test_status="PASSED",
            error_message=test_message,
            device_name="github_actions",
            screen_resolution="ci_environment"
        )
        
        # Get updated test count
        updated_results = db_helper.get_test_results(limit=10)
        updated_count = len(updated_results)
        print(f"📊 Updated test results in database: {updated_count}")
        
        # Verify the entry was added
        if updated_count > initial_count:
            print("✅ Database logging is WORKING!")
            print(f"   - Successfully added {updated_count - initial_count} new test result(s)")
            
            # Show the latest entry
            latest_result = updated_results[0] if updated_results else None
            if latest_result:
                print(f"   - Latest test: {latest_result['test_case_name']} ({latest_result['test_status']})")
                print(f"   - Timestamp: {latest_result['test_datetime']}")
            
            db_helper.close()
            return True
        else:
            print("❌ Database logging is NOT WORKING!")
            print("   - No new test results were added to database")
            db_helper.close()
            return False
            
    except Exception as e:
        print(f"❌ Database connection ERROR: {type(e).__name__} - {e}")
        return False

if __name__ == "__main__":
    print("🚀 Database Connection Test")
    print("=" * 40)
    
    success = test_database_connection()
    
    if success:
        print("\n🎉 Database connection and logging test PASSED!")
        print("   Your database integration is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️ Database connection and logging test FAILED!")
        print("   Please check your database configuration.")
        sys.exit(1) 
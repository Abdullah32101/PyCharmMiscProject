#!/usr/bin/env python3
"""
Database Initialization Script
Creates the test_results table in the database.
"""

import sys
from db.db_helper import MySQLHelper


def init_database():
    """Initialize the database with the test_results table"""
    try:
        print("🔧 Initializing database...")

        db_helper = MySQLHelper()

        # Create the test_results table
        db_helper.create_test_results_table()

        # Test the connection and table
        print("🔍 Testing database connection...")
        stats = db_helper.get_test_statistics()
        if stats is not None:
            print("✅ Database connection successful!")
            print(f"   Current test records: {stats['total_tests']}")
        else:
            print("⚠️ Database connection successful but no statistics available.")

        db_helper.close()
        print("✅ Database initialization completed successfully!")

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("Please check your database configuration in db/db_config.py")
        print("🔍 Error details:")
        print(f"   - Error type: {type(e).__name__}")
        print(f"   - Error message: {str(e)}")
        print("⚠️ This is a critical error - database connection failed")
        sys.exit(1)  # Exit with error code to indicate failure


if __name__ == "__main__":
    init_database()

#!/usr/bin/env python3
"""
Database Schema Update Script
Adds the error_summary column to the existing test_results table.
"""

from db.db_helper import MySQLHelper


def update_database_schema():
    """Update the database schema to add error_summary column"""
    try:
        print("🔧 Updating database schema...")

        db_helper = MySQLHelper()

        # Check if error_summary column already exists
        check_column_query = """
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'test' 
        AND TABLE_NAME = 'test_results' 
        AND COLUMN_NAME = 'error_summary'
        """

        db_helper.cursor.execute(check_column_query)
        column_exists = db_helper.cursor.fetchone()

        if column_exists:
            print("✅ error_summary column already exists in test_results table")
        else:
            # Add the error_summary column
            add_column_query = """
            ALTER TABLE test_results 
            ADD COLUMN error_summary VARCHAR(255) AFTER error_message
            """

            db_helper.cursor.execute(add_column_query)
            db_helper.conn.commit()
            print("✅ Added error_summary column to test_results table")

        # Test the connection
        print("🔍 Testing database connection...")
        stats = db_helper.get_test_statistics()
        if stats is not None:
            print("✅ Database connection successful!")
            print(f"   Current test records: {stats['total_tests']}")
        else:
            print("⚠️ Database connection successful but no statistics available.")

        db_helper.close()
        print("✅ Database schema update completed successfully!")

    except Exception as e:
        print(f"❌ Database schema update failed: {e}")
        print("Please check your database configuration in db/db_config.py")


if __name__ == "__main__":
    update_database_schema()

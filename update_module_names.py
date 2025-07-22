#!/usr/bin/env python3
"""
Module Names Update Script
Updates existing module names in the database to remove 'test.' prefix.
"""

from db.db_helper import MySQLHelper


def update_module_names():
    """Update existing module names to remove 'test.' prefix"""
    try:
        print("🔧 Updating module names in database...")

        db_helper = MySQLHelper()

        # Get all module names that start with 'test.' or 'tests.test_'
        select_query = """
        SELECT DISTINCT module_name 
        FROM test_results 
        WHERE module_name LIKE 'test.%' OR module_name LIKE 'tests.test_%'
        """

        db_helper.cursor.execute(select_query)
        old_module_names = db_helper.cursor.fetchall()

        if not old_module_names:
            print("✅ No module names need updating")
            return

        print(f"Found {len(old_module_names)} module names to update:")

        # Update each module name
        for row in old_module_names:
            old_name = row["module_name"]
            if old_name.startswith("tests.test_"):
                new_name = old_name[12:]  # Remove 'tests.test_' prefix
            elif old_name.startswith("test."):
                new_name = old_name[5:]  # Remove 'test.' prefix
            else:
                new_name = old_name

            update_query = """
            UPDATE test_results 
            SET module_name = %s 
            WHERE module_name = %s
            """

            db_helper.cursor.execute(update_query, (new_name, old_name))
            print(f"   {old_name} → {new_name}")

        db_helper.conn.commit()
        print(f"✅ Updated {len(old_module_names)} module names successfully")

        # Show updated results
        print("\n📊 Updated Test Results:")
        db_helper.cursor.execute(
            "SELECT DISTINCT module_name FROM test_results ORDER BY module_name"
        )
        updated_modules = db_helper.cursor.fetchall()

        for row in updated_modules:
            print(f"   - {row['module_name']}")

        db_helper.close()
        print("✅ Module names update completed successfully!")

    except Exception as e:
        print(f"❌ Module names update failed: {e}")
        print("Please check your database configuration in db/db_config.py")


if __name__ == "__main__":
    update_module_names()

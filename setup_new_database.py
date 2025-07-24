#!/usr/bin/env python3
"""
Setup New Database Script
Creates all required tables in the new database (solutioninn_testing)
"""

from db.db_helper import MySQLHelper
from create_tables import TableCreator


class NewDatabaseSetup:
    def __init__(self):
        self.db_helper = MySQLHelper()
        self.table_creator = TableCreator()

    def setup_database(self):
        """Set up the complete database with all required tables"""
        print("🚀 Setting up new database (solutioninn_testing)...")
        print("=" * 60)

        try:
            # Test connection
            print("🔌 Testing database connection...")
            self.db_helper.cursor.execute("SELECT 1")
            print("✅ Database connection successful")

            # Create all tables
            print("\n📋 Creating all required tables...")
            success = self.table_creator.create_all_tables()

            if success:
                print("\n✅ Database setup completed successfully!")
                print("📊 Showing table information...")
                self.table_creator.show_table_info()
            else:
                print("❌ Database setup failed")

            return success

        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            return False

    def verify_test_results_table(self):
        """Verify that the test_results table exists and has the correct structure"""
        try:
            print("\n🔍 Verifying test_results table...")
            
            # Check if table exists
            self.db_helper.cursor.execute("SHOW TABLES LIKE 'test_results'")
            result = self.db_helper.cursor.fetchone()
            
            if not result:
                print("❌ test_results table not found")
                return False
            
            print("✅ test_results table exists")
            
            # Check table structure
            self.db_helper.cursor.execute("DESCRIBE test_results")
            columns = self.db_helper.cursor.fetchall()
            
            print(f"📋 Table has {len(columns)} columns:")
            for col in columns:
                print(f"   - {col['Field']} ({col['Type']})")
            
            # Check if table has data
            self.db_helper.cursor.execute("SELECT COUNT(*) as count FROM test_results")
            count_result = self.db_helper.cursor.fetchone()
            record_count = count_result['count'] if count_result else 0
            
            print(f"📊 Table contains {record_count} records")
            
            return True
            
        except Exception as e:
            print(f"❌ Error verifying test_results table: {e}")
            return False

    def close(self):
        """Close database connections"""
        try:
            # Clear any unread results
            if self.db_helper.cursor:
                try:
                    self.db_helper.cursor.fetchall()
                except:
                    pass
            self.db_helper.close()
            self.table_creator.close()
        except Exception as e:
            print(f"Warning: Error during cleanup: {e}")


def main():
    """Main setup function"""
    setup = NewDatabaseSetup()
    
    try:
        # Set up the database
        if setup.setup_database():
            # Verify the test_results table
            setup.verify_test_results_table()
            
            print("\n🎉 New database is ready for use!")
            print("✅ All tables created successfully")
            print("✅ Database configuration updated")
            print("\n📝 Next steps:")
            print("   1. Run 'python migrate_test_results.py' to import data from old database")
            print("   2. Test your applications with the new database")
            print("   3. Update any CI/CD configurations if needed")
        else:
            print("❌ Database setup failed")
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
    
    finally:
        setup.close()


if __name__ == "__main__":
    main() 
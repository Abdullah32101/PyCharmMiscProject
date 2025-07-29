#!/usr/bin/env python3
"""
Migration Script: Import test_results table from old database to new database
"""

import mysql.connector
from datetime import datetime

# Old database configuration
OLD_DB_CONFIG = {
    "host": "solutionsole.com",
    "user": "root",
    "password": "SolutionInn321",
    "database": "test",
}

# New database configuration
NEW_DB_CONFIG = {
    "host": "18.235.51.183",
    "user": "sqa_user",
    "password": "Hassan123!@#",
    "database": "solutioninn_testing",
}


class TestResultsMigrator:
    def __init__(self):
        self.old_conn = None
        self.new_conn = None
        self.old_cursor = None
        self.new_cursor = None

    def connect_to_databases(self):
        """Connect to both old and new databases"""
        try:
            print("🔌 Connecting to old database...")
            self.old_conn = mysql.connector.connect(**OLD_DB_CONFIG)
            self.old_cursor = self.old_conn.cursor(dictionary=True)
            print("✅ Connected to old database")

            print("🔌 Connecting to new database...")
            self.new_conn = mysql.connector.connect(**NEW_DB_CONFIG)
            self.new_cursor = self.new_conn.cursor(dictionary=True)
            print("✅ Connected to new database")

            return True
        except Exception as e:
            print(f"❌ Error connecting to databases: {e}")
            return False

    def create_test_results_table_in_new_db(self):
        """Create the test_results table in the new database"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            test_case_name VARCHAR(255) NOT NULL,
            module_name VARCHAR(255) NOT NULL,
            test_status ENUM('PASSED', 'FAILED', 'SKIPPED', 'ERROR') NOT NULL,
            test_datetime DATETIME NOT NULL,
            error_message TEXT,
            error_summary VARCHAR(255),
            total_time_duration DECIMAL(10,3) NULL COMMENT 'Test execution time in seconds',
            device_name VARCHAR(50) NULL COMMENT 'Device type (mobile/desktop/tablet)',
            screen_resolution VARCHAR(50) NULL COMMENT 'Screen resolution (e.g., 1920x1080, 375x812)',
            error_link VARCHAR(500) NULL COMMENT 'URL link to screenshot showing affected screen',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            self.new_cursor.execute(create_table_query)
            self.new_conn.commit()
            print("✅ Test results table created in new database")
            return True
        except Exception as e:
            print(f"❌ Error creating test results table: {e}")
            self.new_conn.rollback()
            return False

    def check_old_table_exists(self):
        """Check if test_results table exists in old database"""
        try:
            self.old_cursor.execute("SHOW TABLES LIKE 'test_results'")
            result = self.old_cursor.fetchone()
            if result:
                print("✅ Test results table found in old database")
                return True
            else:
                print("❌ Test results table not found in old database")
                return False
        except Exception as e:
            print(f"❌ Error checking old table: {e}")
            return False

    def get_old_table_count(self):
        """Get the number of records in the old test_results table"""
        try:
            self.old_cursor.execute("SELECT COUNT(*) as count FROM test_results")
            result = self.old_cursor.fetchone()
            return result['count'] if result else 0
        except Exception as e:
            print(f"❌ Error getting old table count: {e}")
            return 0

    def migrate_data(self, batch_size=1000):
        """Migrate data from old database to new database in batches"""
        try:
            # Get total count
            total_records = self.get_old_table_count()
            print(f"📊 Total records to migrate: {total_records}")

            if total_records == 0:
                print("ℹ️ No records to migrate")
                return True

            # Get all records from old database
            self.old_cursor.execute("SELECT * FROM test_results ORDER BY id")
            
            migrated_count = 0
            batch_count = 0

            while True:
                batch = self.old_cursor.fetchmany(batch_size)
                if not batch:
                    break

                batch_count += 1
                print(f"📦 Processing batch {batch_count} ({len(batch)} records)...")

                # Insert batch into new database
                for record in batch:
                    try:
                        insert_query = """
                        INSERT INTO test_results (
                            test_case_name, module_name, test_status, test_datetime,
                            error_message, error_summary, total_time_duration,
                            device_name, screen_resolution, error_link, created_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        
                        self.new_cursor.execute(insert_query, (
                            record['test_case_name'],
                            record['module_name'],
                            record['test_status'],
                            record['test_datetime'],
                            record.get('error_message'),
                            record.get('error_summary'),
                            record.get('total_time_duration'),
                            record.get('device_name'),
                            record.get('screen_resolution'),
                            record.get('error_link'),
                            record.get('created_at', datetime.now())
                        ))
                        
                        migrated_count += 1
                    except Exception as e:
                        print(f"❌ Error migrating record {record.get('id', 'unknown')}: {e}")
                        continue

                # Commit batch
                self.new_conn.commit()
                print(f"✅ Batch {batch_count} completed. Total migrated: {migrated_count}")

            print(f"🎉 Migration completed! {migrated_count}/{total_records} records migrated")
            return migrated_count == total_records

        except Exception as e:
            print(f"❌ Error during migration: {e}")
            self.new_conn.rollback()
            return False

    def verify_migration(self):
        """Verify that the migration was successful"""
        try:
            # Check record count in new database
            self.new_cursor.execute("SELECT COUNT(*) as count FROM test_results")
            new_count = self.new_cursor.fetchone()['count']
            
            # Check record count in old database
            old_count = self.get_old_table_count()
            
            print(f"\n📊 Migration Verification:")
            print(f"   Old database records: {old_count}")
            print(f"   New database records: {new_count}")
            
            if new_count == old_count:
                print("✅ Migration verification successful!")
                return True
            else:
                print("❌ Migration verification failed - record counts don't match")
                return False
                
        except Exception as e:
            print(f"❌ Error during verification: {e}")
            return False

    def close_connections(self):
        """Close all database connections"""
        if self.old_cursor:
            self.old_cursor.close()
        if self.new_cursor:
            self.new_cursor.close()
        if self.old_conn:
            self.old_conn.close()
        if self.new_conn:
            self.new_conn.close()
        print("🔌 Database connections closed")


def main():
    """Main migration function"""
    print("🚀 Starting test_results table migration...")
    print("=" * 60)
    
    migrator = TestResultsMigrator()
    
    try:
        # Step 1: Connect to databases
        if not migrator.connect_to_databases():
            return False
        
        # Step 2: Check if old table exists
        if not migrator.check_old_table_exists():
            print("❌ Cannot proceed without old test_results table")
            return False
        
        # Step 3: Create table in new database
        if not migrator.create_test_results_table_in_new_db():
            print("❌ Cannot create table in new database")
            return False
        
        # Step 4: Migrate data
        if not migrator.migrate_data():
            print("❌ Data migration failed")
            return False
        
        # Step 5: Verify migration
        if not migrator.verify_migration():
            print("❌ Migration verification failed")
            return False
        
        print("\n🎉 Migration completed successfully!")
        print("✅ Your new database is now ready to use")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    finally:
        migrator.close_connections()


if __name__ == "__main__":
    main() 
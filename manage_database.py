#!/usr/bin/env python3
"""
Database Management Utility
A comprehensive tool to manage and view data in all database tables.
"""

from db.db_helper import MySQLHelper
import sys
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_helper = MySQLHelper()
    
    def show_all_tables(self):
        """Show all tables in the database"""
        try:
            self.db_helper.cursor.execute("SHOW TABLES")
            tables = self.db_helper.cursor.fetchall()
            
            print("\n📋 Database Tables:")
            print("=" * 50)
            
            for i, table in enumerate(tables, 1):
                table_name = list(table.values())[0]
                print(f"{i}. {table_name}")
            
            return [list(table.values())[0] for table in tables]
        
        except Exception as e:
            print(f"❌ Error showing tables: {e}")
            return []
    
    def show_table_data(self, table_name, limit=10):
        """Show data from a specific table"""
        try:
            # Get table structure
            self.db_helper.cursor.execute(f"DESCRIBE {table_name}")
            columns = self.db_helper.cursor.fetchall()
            
            print(f"\n📊 Table: {table_name}")
            print("=" * 60)
            
            # Get data
            self.db_helper.cursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT {limit}")
            rows = self.db_helper.cursor.fetchall()
            
            if not rows:
                print("No data found in this table.")
                return
            
            # Print column headers
            column_names = [col['Field'] for col in columns]
            header = " | ".join(f"{name[:15]:<15}" for name in column_names)
            print(header)
            print("-" * len(header))
            
            # Print data rows
            for row in rows:
                row_data = []
                for col in column_names:
                    value = row[col]
                    if value is None:
                        value = "NULL"
                    elif isinstance(value, datetime):
                        value = value.strftime('%Y-%m-%d %H:%M')
                    else:
                        value = str(value)
                    row_data.append(f"{value[:15]:<15}")
                print(" | ".join(row_data))
            
            print(f"\nTotal rows: {len(rows)}")
            
        except Exception as e:
            print(f"❌ Error showing table data: {e}")
    
    def get_table_count(self, table_name):
        """Get row count for a table"""
        try:
            self.db_helper.cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            result = self.db_helper.cursor.fetchone()
            return result['count'] if result else 0
        except Exception as e:
            print(f"❌ Error getting count for {table_name}: {e}")
            return 0
    
    def show_database_summary(self):
        """Show summary of all tables"""
        try:
            tables = self.show_all_tables()
            
            print("\n📈 Database Summary:")
            print("=" * 50)
            
            total_records = 0
            for table_name in tables:
                count = self.get_table_count(table_name)
                total_records += count
                print(f"📋 {table_name}: {count} records")
            
            print(f"\n📊 Total Records: {total_records}")
            
        except Exception as e:
            print(f"❌ Error showing database summary: {e}")
    
    def search_data(self, table_name, search_term, column=None):
        """Search for data in a table"""
        try:
            if column:
                query = f"SELECT * FROM {table_name} WHERE {column} LIKE %s"
                params = (f"%{search_term}%",)
            else:
                # Search in all text columns
                self.db_helper.cursor.execute(f"DESCRIBE {table_name}")
                columns = self.db_helper.cursor.fetchall()
                text_columns = [col['Field'] for col in columns if 'varchar' in col['Type'].lower() or 'text' in col['Type'].lower()]
                
                if not text_columns:
                    print("❌ No searchable text columns found in this table.")
                    return
                
                conditions = " OR ".join([f"{col} LIKE %s" for col in text_columns])
                query = f"SELECT * FROM {table_name} WHERE {conditions}"
                params = tuple([f"%{search_term}%"] * len(text_columns))
            
            self.db_helper.cursor.execute(query, params)
            results = self.db_helper.cursor.fetchall()
            
            print(f"\n🔍 Search Results for '{search_term}' in {table_name}:")
            print("=" * 60)
            
            if not results:
                print("No results found.")
                return
            
            for i, row in enumerate(results, 1):
                print(f"\nResult {i}:")
                for key, value in row.items():
                    if value is not None:
                        print(f"  {key}: {value}")
            
            print(f"\nTotal results: {len(results)}")
            
        except Exception as e:
            print(f"❌ Error searching data: {e}")
    
    def insert_sample_data(self):
        """Insert sample data into tables"""
        try:
            print("\n🔧 Inserting sample data...")
            
            # Insert sample users
            users_data = [
                ('john_doe', 'john@example.com', 'hashed_password_123', 'John', 'Doe', 'Harvard University', 'student'),
                ('jane_smith', 'jane@example.com', 'hashed_password_456', 'Jane', 'Smith', 'MIT', 'instructor'),
                ('admin_user', 'admin@example.com', 'hashed_password_789', 'Admin', 'User', 'System', 'admin')
            ]
            
            for user_data in users_data:
                self.db_helper.cursor.execute("""
                    INSERT IGNORE INTO users (username, email, password_hash, first_name, last_name, university, user_type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, user_data)
            
            # Insert sample books
            books_data = [
                ('Introduction to Computer Science', 'John Smith', '978-0123456789', 'Tech Books Inc', 2023, 49.99, 'A comprehensive guide to computer science fundamentals', 'Computer Science'),
                ('Advanced Mathematics', 'Dr. Sarah Johnson', '978-0987654321', 'Math Publishers', 2022, 79.99, 'Advanced mathematical concepts and applications', 'Mathematics'),
                ('Business Management', 'Michael Brown', '978-1122334455', 'Business Press', 2023, 59.99, 'Modern business management strategies', 'Business')
            ]
            
            for book_data in books_data:
                self.db_helper.cursor.execute("""
                    INSERT IGNORE INTO books (title, author, isbn, publisher, publication_year, price, description, category)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, book_data)
            
            self.db_helper.conn.commit()
            print("✅ Sample data inserted successfully!")
            
        except Exception as e:
            print(f"❌ Error inserting sample data: {e}")
            self.db_helper.conn.rollback()
    
    def close(self):
        """Close database connection"""
        self.db_helper.close()

def print_help():
    """Print help information"""
    print("""
🔧 Database Management Utility

Usage: python manage_database.py [command] [options]

Commands:
  summary              - Show database summary
  tables               - List all tables
  view <table> [limit] - View data from a specific table
  search <table> <term> [column] - Search for data in a table
  sample               - Insert sample data
  help                 - Show this help message

Examples:
  python manage_database.py summary
  python manage_database.py tables
  python manage_database.py view users 5
  python manage_database.py search books "computer"
  python manage_database.py search users "john" email
  python manage_database.py sample
""")

def main():
    """Main function"""
    try:
        manager = DatabaseManager()
        
        if len(sys.argv) < 2:
            print_help()
            return
        
        command = sys.argv[1].lower()
        
        if command == "help":
            print_help()
        
        elif command == "summary":
            manager.show_database_summary()
        
        elif command == "tables":
            manager.show_all_tables()
        
        elif command == "view":
            if len(sys.argv) < 3:
                print("❌ Please specify a table name: python manage_database.py view <table_name>")
                return
            
            table_name = sys.argv[2]
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            manager.show_table_data(table_name, limit)
        
        elif command == "search":
            if len(sys.argv) < 4:
                print("❌ Please specify table and search term: python manage_database.py search <table> <term>")
                return
            
            table_name = sys.argv[2]
            search_term = sys.argv[3]
            column = sys.argv[4] if len(sys.argv) > 4 else None
            manager.search_data(table_name, search_term, column)
        
        elif command == "sample":
            manager.insert_sample_data()
        
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
        
        manager.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your database configuration in db/db_config.py")

if __name__ == "__main__":
    main() 
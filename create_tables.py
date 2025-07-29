#!/usr/bin/env python3
"""
Create Additional Tables Script
Creates 4 additional tables in the test database.
"""

from db.db_helper import MySQLHelper


class TableCreator:
    def __init__(self):
        self.db_helper = MySQLHelper()

    def create_users_table(self):
        """Create users table"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            university VARCHAR(255),
            user_type ENUM('student', 'instructor', 'admin') DEFAULT 'student',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        try:
            self.db_helper.cursor.execute(create_table_query)
            self.db_helper.conn.commit()
            print("✅ Users table created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating users table: {e}")
            self.db_helper.conn.rollback()
            return False

    def create_books_table(self):
        """Create books table"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            author VARCHAR(255),
            isbn VARCHAR(20) UNIQUE,
            publisher VARCHAR(255),
            publication_year INT,
            price DECIMAL(10,2),
            description TEXT,
            cover_image_url VARCHAR(500),
            category VARCHAR(100),
            is_available BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        try:
            self.db_helper.cursor.execute(create_table_query)
            self.db_helper.conn.commit()
            print("✅ Books table created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating books table: {e}")
            self.db_helper.conn.rollback()
            return False

    def create_orders_table(self):
        """Create orders table"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_number VARCHAR(50) UNIQUE NOT NULL,
            user_id INT NOT NULL,
            book_id INT,
            order_type ENUM('book_purchase', 'monthly_plan', 'six_month_plan', 'onetime_plan') NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            payment_method ENUM('credit_card', 'paypal', 'free') DEFAULT 'credit_card',
            payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
            order_status ENUM('pending', 'processing', 'completed', 'cancelled') DEFAULT 'pending',
            billing_address TEXT,
            shipping_address TEXT,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_date TIMESTAMP NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE SET NULL
        )
        """
        try:
            self.db_helper.cursor.execute(create_table_query)
            self.db_helper.conn.commit()
            print("✅ Orders table created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating orders table: {e}")
            self.db_helper.conn.rollback()
            return False

    def create_subscriptions_table(self):
        """Create subscriptions table"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            subscription_type ENUM('monthly', 'six_month', 'annual') NOT NULL,
            status ENUM('active', 'cancelled', 'expired', 'pending') DEFAULT 'pending',
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            auto_renew BOOLEAN DEFAULT FALSE,
            payment_method ENUM('credit_card', 'paypal') DEFAULT 'credit_card',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
        try:
            self.db_helper.cursor.execute(create_table_query)
            self.db_helper.conn.commit()
            print("✅ Subscriptions table created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating subscriptions table: {e}")
            self.db_helper.conn.rollback()
            return False

    def create_all_tables(self):
        """Create all 4 tables"""
        print("🔧 Creating 4 additional tables in test database...")
        print("=" * 60)

        tables = [
            ("Users Table", self.create_users_table),
            ("Books Table", self.create_books_table),
            ("Orders Table", self.create_orders_table),
            ("Subscriptions Table", self.create_subscriptions_table),
        ]

        success_count = 0
        total_tables = len(tables)

        for table_name, create_func in tables:
            print(f"\n📋 Creating {table_name}...")
            if create_func():
                success_count += 1
            else:
                print(f"❌ Failed to create {table_name}")

        print("\n" + "=" * 60)
        print(f"📊 Results: {success_count}/{total_tables} tables created successfully")

        if success_count == total_tables:
            print("🎉 All tables created successfully!")
        else:
            print("⚠️ Some tables failed to create. Check the error messages above.")

        return success_count == total_tables

    def show_table_info(self):
        """Show information about all tables"""
        try:
            # Get all tables
            self.db_helper.cursor.execute("SHOW TABLES")
            tables = self.db_helper.cursor.fetchall()

            print("\n📋 Database Tables:")
            print("=" * 40)

            for table in tables:
                table_name = list(table.values())[0]
                print(f"✅ {table_name}")

                # Get table structure
                self.db_helper.cursor.execute(f"DESCRIBE {table_name}")
                columns = self.db_helper.cursor.fetchall()

                print(f"   Columns ({len(columns)}):")
                for col in columns:
                    print(f"     - {col['Field']} ({col['Type']})")
                print()

        except Exception as e:
            print(f"❌ Error showing table info: {e}")

    def close(self):
        """Close database connection"""
        self.db_helper.close()


def main():
    """Main function to create tables"""
    try:
        creator = TableCreator()

        # Create all tables
        success = creator.create_all_tables()

        if success:
            # Show table information
            creator.show_table_info()

        creator.close()

    except Exception as e:
        print(f"❌ Database operation failed: {e}")
        print("Please check your database configuration in db/db_config.py")


if __name__ == "__main__":
    main()

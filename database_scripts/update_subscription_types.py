#!/usr/bin/env python3
"""
Update Subscription Types Script
Updates the database schema to support all subscription types including three_month, popular, and onetime plans.
"""

from db.db_helper import MySQLHelper


class SubscriptionTypeUpdater:
    def __init__(self):
        self.db_helper = MySQLHelper()

    def update_subscription_types(self):
        """Update subscription table to support all subscription types"""
        print("🔧 Updating subscription types in database...")
        print("=" * 60)

        try:
            # Update subscriptions table to support new types
            self._update_subscriptions_table()
            
            # Update orders table to support new order types
            self._update_orders_table()
            
            print("✅ Subscription types updated successfully!")
            return True

        except Exception as e:
            print(f"❌ Error updating subscription types: {e}")
            self.db_helper.conn.rollback()
            return False

    def _update_subscriptions_table(self):
        """Update subscriptions table to support new subscription types"""
        print("📋 Updating subscriptions table...")
        
        try:
            # First, let's check if we need to modify the ENUM
            self.db_helper.cursor.execute("""
                SELECT COLUMN_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'subscriptions' 
                AND COLUMN_NAME = 'subscription_type'
            """)
            
            result = self.db_helper.cursor.fetchone()
            if result:
                current_enum = result['COLUMN_TYPE']
                print(f"   Current subscription_type ENUM: {current_enum}")
                
                # Check if we need to update
                if 'three_month' not in current_enum or 'popular' not in current_enum or 'onetime' not in current_enum:
                    print("   Updating subscription_type ENUM...")
                    
                    # Create a temporary table with new structure
                    self.db_helper.cursor.execute("""
                        CREATE TABLE subscriptions_new (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            user_id INT NOT NULL,
                            subscription_type ENUM('monthly', 'three_month', 'six_month', 'popular', 'onetime', 'annual') NOT NULL,
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
                    """)
                    
                    # Copy existing data
                    self.db_helper.cursor.execute("""
                        INSERT INTO subscriptions_new 
                        SELECT * FROM subscriptions
                    """)
                    
                    # Drop old table and rename new one
                    self.db_helper.cursor.execute("DROP TABLE subscriptions")
                    self.db_helper.cursor.execute("ALTER TABLE subscriptions_new RENAME TO subscriptions")
                    
                    print("   ✅ Subscriptions table updated with new types")
                else:
                    print("   ✅ Subscriptions table already supports new types")
            else:
                print("   ⚠️ Could not check current subscription_type structure")

        except Exception as e:
            print(f"   ❌ Error updating subscriptions table: {e}")
            raise

    def _update_orders_table(self):
        """Update orders table to support new order types"""
        print("📋 Updating orders table...")
        
        try:
            # Check current order_type ENUM
            self.db_helper.cursor.execute("""
                SELECT COLUMN_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'orders' 
                AND COLUMN_NAME = 'order_type'
            """)
            
            result = self.db_helper.cursor.fetchone()
            if result:
                current_enum = result['COLUMN_TYPE']
                print(f"   Current order_type ENUM: {current_enum}")
                
                # Check if we need to update
                if 'three_month_plan' not in current_enum or 'popular_plan' not in current_enum:
                    print("   Updating order_type ENUM...")
                    
                    # Create a temporary table with new structure
                    self.db_helper.cursor.execute("""
                        CREATE TABLE orders_new (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            order_number VARCHAR(50) UNIQUE NOT NULL,
                            user_id INT NOT NULL,
                            book_id INT,
                            order_type ENUM('book_purchase', 'monthly_plan', 'three_month_plan', 'six_month_plan', 'popular_plan', 'onetime_plan') NOT NULL,
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
                    """)
                    
                    # Copy existing data
                    self.db_helper.cursor.execute("""
                        INSERT INTO orders_new 
                        SELECT * FROM orders
                    """)
                    
                    # Drop old table and rename new one
                    self.db_helper.cursor.execute("DROP TABLE orders")
                    self.db_helper.cursor.execute("ALTER TABLE orders_new RENAME TO orders")
                    
                    print("   ✅ Orders table updated with new types")
                else:
                    print("   ✅ Orders table already supports new types")
            else:
                print("   ⚠️ Could not check current order_type structure")

        except Exception as e:
            print(f"   ❌ Error updating orders table: {e}")
            raise

    def show_updated_schema(self):
        """Show the updated database schema"""
        print("\n📊 Updated Database Schema:")
        print("=" * 40)
        
        try:
            # Show subscriptions table structure
            print("\n📋 Subscriptions Table:")
            self.db_helper.cursor.execute("DESCRIBE subscriptions")
            columns = self.db_helper.cursor.fetchall()
            for col in columns:
                print(f"   - {col['Field']}: {col['Type']}")
            
            # Show orders table structure
            print("\n📋 Orders Table:")
            self.db_helper.cursor.execute("DESCRIBE orders")
            columns = self.db_helper.cursor.fetchall()
            for col in columns:
                print(f"   - {col['Field']}: {col['Type']}")

        except Exception as e:
            print(f"❌ Error showing schema: {e}")

    def close(self):
        """Close database connection"""
        self.db_helper.close()


def main():
    """Main function to update subscription types"""
    try:
        updater = SubscriptionTypeUpdater()

        # Update subscription types
        success = updater.update_subscription_types()

        if success:
            # Show updated schema
            updater.show_updated_schema()
            
            print("\n🎉 Subscription types update completed!")
            print("✅ All subscription types now supported:")
            print("   - monthly")
            print("   - three_month")
            print("   - six_month")
            print("   - popular")
            print("   - onetime")
            print("   - annual")
        else:
            print("❌ Subscription types update failed")

        updater.close()

    except Exception as e:
        print(f"❌ Update operation failed: {e}")
        print("Please check your database configuration in db/db_config.py")


if __name__ == "__main__":
    main() 
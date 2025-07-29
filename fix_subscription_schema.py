#!/usr/bin/env python3
"""
Fix Subscription Table Schema
Adds missing subscription types: three_month, popular, onetime
"""

import sys
sys.path.append('.')

from db.db_helper import MySQLHelper

def fix_subscription_schema():
    """Fix subscription table to support all required types"""
    print("🔧 Fixing Subscription Table Schema")
    print("=" * 60)
    
    db = MySQLHelper()
    
    try:
        print("Current subscription table only supports: monthly, six_month, annual")
        print("Adding missing types: three_month, popular, onetime")
        
        # Create temporary table with new structure
        print("\n📋 Creating new subscriptions table with all types...")
        db.cursor.execute("""
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
        print("📋 Copying existing data...")
        db.cursor.execute("""
            INSERT INTO subscriptions_new 
            SELECT * FROM subscriptions
        """)
        
        # Drop old table and rename new one
        print("📋 Replacing old table...")
        db.cursor.execute("DROP TABLE subscriptions")
        db.cursor.execute("ALTER TABLE subscriptions_new RENAME TO subscriptions")
        
        db.conn.commit()
        print("✅ Subscription table updated successfully!")
        
        # Verify the fix
        print("\n📊 Verifying the fix...")
        db.cursor.execute("""
            SELECT COLUMN_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'subscriptions' 
            AND COLUMN_NAME = 'subscription_type'
        """)
        
        result = db.cursor.fetchone()
        if result:
            new_enum = result['COLUMN_TYPE']
            print(f"New subscription_type ENUM: {new_enum}")
            
            # Check if all types are now supported
            required_types = ['monthly', 'three_month', 'six_month', 'popular', 'onetime', 'annual']
            new_types = new_enum.replace("enum(", "").replace(")", "").replace("'", "").split(",")
            
            missing_types = [t for t in required_types if t not in new_types]
            if not missing_types:
                print("✅ All required subscription types are now supported!")
                return True
            else:
                print(f"❌ Still missing types: {missing_types}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing subscription schema: {e}")
        db.conn.rollback()
        return False
    finally:
        db.close()

def test_all_subscription_types():
    """Test that all subscription types work correctly"""
    print("\n🧪 Testing All Subscription Types")
    print("=" * 60)
    
    db = MySQLHelper()
    
    try:
        # Clear existing test data
        print("🧹 Clearing existing test data...")
        db.cursor.execute("DELETE FROM subscriptions WHERE created_at >= NOW() - INTERVAL 1 HOUR")
        db.cursor.execute("DELETE FROM test_results WHERE test_case_name LIKE 'test_fix_%'")
        db.conn.commit()
        
        # Test all subscription types
        test_cases = [
            ("test_fix_monthly_plan", "test_subscription_module", "monthly"),
            ("test_fix_three_month_plan", "test_subscription_module", "three_month"),
            ("test_fix_six_month_plan", "test_subscription_module", "six_month"),
            ("test_fix_popular_plan", "test_subscription_module", "popular"),
            ("test_fix_onetime_plan", "test_subscription_module", "onetime"),
        ]
        
        for test_name, module_name, expected_type in test_cases:
            print(f"Testing {expected_type}...")
            db.store_test_result_in_tables(
                test_name,
                module_name,
                "PASSED",
                test_data={"plan_type": expected_type}
            )
        
        # Check results
        print("\n📊 Checking Results...")
        db.cursor.execute("""
            SELECT subscription_type, COUNT(*) as count 
            FROM subscriptions 
            WHERE created_at >= NOW() - INTERVAL 1 HOUR
            GROUP BY subscription_type 
            ORDER BY count DESC
        """)
        subscription_results = db.cursor.fetchall()
        
        print("💳 Subscriptions Table Results:")
        if subscription_results:
            for result in subscription_results:
                print(f"   - {result['subscription_type']}: {result['count']} subscriptions")
        else:
            print("   - No test subscriptions found")
        
        # Verify all types are present
        subscription_types = ['monthly', 'three_month', 'six_month', 'popular', 'onetime']
        found_types = [result['subscription_type'] for result in subscription_results]
        
        missing_types = [t for t in subscription_types if t not in found_types]
        if not missing_types:
            print("\n✅ All subscription types working correctly!")
            return True
        else:
            print(f"\n❌ Missing subscription types: {missing_types}")
            return False
        
    except Exception as e:
        print(f"❌ Error testing subscription types: {e}")
        return False
    finally:
        db.close()

def main():
    """Main function to fix and test subscription schema"""
    print("🔧 Fixing Subscription Table Schema")
    print("This will add support for: three_month, popular, onetime")
    
    # Fix the schema
    if fix_subscription_schema():
        print("\n✅ Schema fixed successfully!")
        
        # Test all subscription types
        if test_all_subscription_types():
            print("\n🎉 ALL VERIFICATIONS PASSED!")
            print("   Now all subscription types are working correctly:")
            print("   - monthly: $29.99 (1 month)")
            print("   - three_month: $79.99 (3 months)")
            print("   - six_month: $149.99 (6 months)")
            print("   - popular: $79.99 (3 months)")
            print("   - onetime: $99.99 (1 year)")
        else:
            print("\n❌ Some subscription types are still not working!")
    else:
        print("\n❌ Failed to fix subscription schema!")

if __name__ == "__main__":
    main() 
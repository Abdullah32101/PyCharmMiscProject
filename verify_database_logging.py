#!/usr/bin/env python3
"""
Verify Database Logging - Complete Check
Ensures all subscription types are working correctly
"""

import sys
sys.path.append('.')

from db.db_helper import MySQLHelper

def verify_database_logging():
    """Verify that all database logging is working correctly"""
    print("🔍 Verifying Database Logging - Complete Check")
    print("=" * 60)
    
    db = MySQLHelper()
    
    try:
        # Step 1: Check subscription table schema
        print("\n📋 Step 1: Checking Subscription Table Schema")
        print("-" * 40)
        
        db.cursor.execute("""
            SELECT COLUMN_TYPE 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = DATABASE() 
            AND TABLE_NAME = 'subscriptions' 
            AND COLUMN_NAME = 'subscription_type'
        """)
        
        result = db.cursor.fetchone()
        if result:
            current_enum = result['COLUMN_TYPE']
            print(f"Current subscription_type ENUM: {current_enum}")
            
            # Check what types are supported
            required_types = ['monthly', 'three_month', 'six_month', 'popular', 'onetime', 'annual']
            current_types = current_enum.replace("enum(", "").replace(")", "").replace("'", "").split(",")
            
            print(f"Supported types: {current_types}")
            print(f"Required types: {required_types}")
            
            missing_types = [t for t in required_types if t not in current_types]
            if missing_types:
                print(f"❌ Missing types: {missing_types}")
                print("   This needs to be fixed!")
                return False
            else:
                print("✅ All required subscription types are supported!")
        
        # Step 2: Clear existing test data
        print("\n🧹 Step 2: Clearing Existing Test Data")
        print("-" * 40)
        
        db.cursor.execute("DELETE FROM orders WHERE order_number LIKE 'TEST-VERIFY-%'")
        db.cursor.execute("DELETE FROM subscriptions WHERE created_at >= NOW() - INTERVAL 1 HOUR")
        db.cursor.execute("DELETE FROM test_results WHERE test_case_name LIKE 'test_verify_%'")
        db.conn.commit()
        print("✅ Test data cleared")
        
        # Step 3: Test all subscription types
        print("\n🧪 Step 3: Testing All Subscription Types")
        print("-" * 40)
        
        test_cases = [
            ("test_verify_monthly_plan", "test_subscription_module", "monthly"),
            ("test_verify_three_month_plan", "test_subscription_module", "three_month"),
            ("test_verify_six_month_plan", "test_subscription_module", "six_month"),
            ("test_verify_popular_plan", "test_subscription_module", "popular"),
            ("test_verify_onetime_plan", "test_subscription_module", "onetime"),
        ]
        
        for test_name, module_name, expected_type in test_cases:
            print(f"Testing {expected_type}...")
            db.store_test_result_in_tables(
                test_name,
                module_name,
                "PASSED",
                test_data={"plan_type": expected_type}
            )
        
        # Step 4: Test book purchase
        print("\n📚 Step 4: Testing Book Purchase")
        print("-" * 40)
        
        db.store_test_result_in_tables(
            "test_verify_book_purchase",
            "test_book_module",
            "PASSED",
            test_data={"book_title": "Test Book"}
        )
        
        # Step 5: Check results
        print("\n📊 Step 5: Checking Results")
        print("-" * 40)
        
        # Check orders table
        print("\n🛒 Orders Table Results:")
        db.cursor.execute("""
            SELECT order_type, COUNT(*) as count 
            FROM orders 
            WHERE order_date >= NOW() - INTERVAL 1 HOUR
            GROUP BY order_type 
            ORDER BY count DESC
        """)
        order_results = db.cursor.fetchall()
        if order_results:
            for result in order_results:
                print(f"   - {result['order_type']}: {result['count']} orders")
        else:
            print("   - No test orders found")
        
        # Check subscriptions table
        print("\n💳 Subscriptions Table Results:")
        db.cursor.execute("""
            SELECT subscription_type, COUNT(*) as count 
            FROM subscriptions 
            WHERE created_at >= NOW() - INTERVAL 1 HOUR
            GROUP BY subscription_type 
            ORDER BY count DESC
        """)
        subscription_results = db.cursor.fetchall()
        if subscription_results:
            for result in subscription_results:
                print(f"   - {result['subscription_type']}: {result['count']} subscriptions")
        else:
            print("   - No test subscriptions found")
        
        # Step 6: Verify correct logic
        print("\n✅ Step 6: Verification")
        print("-" * 40)
        
        # Check if book purchase is in orders only
        book_in_orders = any(result['order_type'] == 'book_purchase' for result in order_results)
        if book_in_orders:
            print("   ✅ Book purchase correctly stored in orders table")
        else:
            print("   ❌ Book purchase not found in orders table")
        
        # Check if all subscription types are present
        subscription_types = ['monthly', 'three_month', 'six_month', 'popular', 'onetime']
        found_types = [result['subscription_type'] for result in subscription_results]
        
        missing_subscription_types = [t for t in subscription_types if t not in found_types]
        if not missing_subscription_types:
            print("   ✅ All subscription types correctly stored in subscriptions table")
        else:
            print(f"   ❌ Missing subscription types: {missing_subscription_types}")
        
        # Check that subscriptions are NOT in orders table
        subscription_orders = [result for result in order_results if 'plan' in result['order_type']]
        if not subscription_orders:
            print("   ✅ No subscription plans stored in orders table (correct)")
        else:
            print(f"   ❌ Found {len(subscription_orders)} subscription orders in orders table (incorrect)")
        
        # Check total counts
        total_orders = sum(result['count'] for result in order_results)
        total_subscriptions = sum(result['count'] for result in subscription_results)
        
        print(f"   📊 Total orders: {total_orders} (should be 1)")
        print(f"   📊 Total subscriptions: {total_subscriptions} (should be 5)")
        
        # Step 7: Final summary
        print("\n🎯 Step 7: Final Summary")
        print("-" * 40)
        
        success = True
        
        if total_orders == 1 and book_in_orders:
            print("   ✅ Book purchase logging: CORRECT")
        else:
            print("   ❌ Book purchase logging: INCORRECT")
            success = False
        
        if total_subscriptions == 5 and not missing_subscription_types:
            print("   ✅ Subscription logging: CORRECT")
        else:
            print("   ❌ Subscription logging: INCORRECT")
            success = False
        
        if not subscription_orders:
            print("   ✅ No duplicate storage: CORRECT")
        else:
            print("   ❌ No duplicate storage: INCORRECT")
            success = False
        
        if success:
            print("\n🎉 ALL VERIFICATIONS PASSED!")
            print("   Database logging is working correctly according to requirements:")
            print("   - Orders table: Book purchases only")
            print("   - Subscriptions table: All payment plans only")
        else:
            print("\n❌ SOME VERIFICATIONS FAILED!")
            print("   Please check the issues above and fix them.")
        
        return success
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    verify_database_logging() 
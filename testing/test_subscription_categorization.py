#!/usr/bin/env python3
"""
Test Subscription Categorization
This script tests that the new subscription categorization is working correctly.
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.db_helper import MySQLHelper


def test_subscription_categorization():
    """Test that subscription categorization is working correctly"""
    print("🧪 Testing Subscription Categorization")
    print("=" * 50)
    
    try:
        db_helper = MySQLHelper()
        
        # Test cases to verify
        test_cases = [
            # Book purchase tests - should only go to orders table
            {
                "name": "book_purchase_test",
                "module": "test_book_purchase",
                "expected_order_type": "book_purchase",
                "expected_subscription": False
            },
            {
                "name": "test_book_page_load_and_click",
                "module": "test_book_purchase",
                "expected_order_type": "book_purchase",
                "expected_subscription": False
            },
            
            # Subscription tests - should go to both orders and subscriptions tables
            {
                "name": "monthly_plan_test",
                "module": "test_monthly_plan",
                "expected_order_type": "monthly_plan",
                "expected_subscription": True,
                "expected_subscription_type": "monthly"
            },
            {
                "name": "six_month_plan_test",
                "module": "test_six_month_plan",
                "expected_order_type": "six_month_plan",
                "expected_subscription": True,
                "expected_subscription_type": "six_month"
            },
            {
                "name": "three_month_plan_test",
                "module": "test_three_month_plan",
                "expected_order_type": "three_month_plan",
                "expected_subscription": True,
                "expected_subscription_type": "three_month"
            },
            {
                "name": "popular_plan_test",
                "module": "test_popular_plan",
                "expected_order_type": "popular_plan",
                "expected_subscription": True,
                "expected_subscription_type": "popular"
            },
            {
                "name": "onetime_plan_test",
                "module": "test_onetime_plan",
                "expected_order_type": "onetime_plan",
                "expected_subscription": True,
                "expected_subscription_type": "onetime"
            }
        ]
        
        print(f"📋 Testing {len(test_cases)} test cases...")
        print()
        
        passed_tests = 0
        total_tests = len(test_cases)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"🔍 Test {i}/{total_tests}: {test_case['name']}")
            
            # Store test result
            db_helper.store_test_result_in_tables(
                test_case_name=test_case['name'],
                module_name=test_case['module'],
                test_status="PASSED",
                error_message=f"Test case {test_case['name']} - {datetime.now()}",
                device_name="categorization_test",
                screen_resolution="test_environment"
            )
            
            # Verify the results
            success = verify_test_categorization(db_helper, test_case)
            
            if success:
                print(f"   ✅ PASSED")
                passed_tests += 1
            else:
                print(f"   ❌ FAILED")
            
            print()
        
        print("=" * 50)
        print(f"📊 Results: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All categorization tests passed!")
            print("✅ Book purchases are correctly stored only in orders table")
            print("✅ All subscription types are correctly stored in subscriptions table")
        else:
            print("⚠️ Some categorization tests failed")
        
        db_helper.close()
        return passed_tests == total_tests
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def verify_test_categorization(db_helper, test_case):
    """Verify that a test case was categorized correctly"""
    try:
        # Get the most recent order for this test
        db_helper.cursor.execute("""
            SELECT order_type, amount, payment_status 
            FROM orders 
            WHERE order_number LIKE 'TEST-%' 
            ORDER BY order_date DESC 
            LIMIT 1
        """)
        
        order_result = db_helper.cursor.fetchone()
        
        # Get the most recent subscription for this test
        db_helper.cursor.execute("""
            SELECT subscription_type, amount, status 
            FROM subscriptions 
            ORDER BY created_at DESC 
            LIMIT 1
        """)
        
        subscription_result = db_helper.cursor.fetchone()
        
        # Verify order categorization
        if order_result:
            order_type = order_result['order_type']
            expected_order_type = test_case['expected_order_type']
            
            if order_type != expected_order_type:
                print(f"   ❌ Order type mismatch: expected '{expected_order_type}', got '{order_type}'")
                return False
            else:
                print(f"   ✅ Order type correct: {order_type}")
        else:
            print(f"   ❌ No order found for test case")
            return False
        
        # Verify subscription categorization
        if test_case['expected_subscription']:
            if subscription_result:
                subscription_type = subscription_result['subscription_type']
                expected_subscription_type = test_case['expected_subscription_type']
                
                if subscription_type != expected_subscription_type:
                    print(f"   ❌ Subscription type mismatch: expected '{expected_subscription_type}', got '{subscription_type}'")
                    return False
                else:
                    print(f"   ✅ Subscription type correct: {subscription_type}")
            else:
                print(f"   ❌ Expected subscription but none found")
                return False
        else:
            if subscription_result:
                print(f"   ❌ Unexpected subscription found: {subscription_result['subscription_type']}")
                return False
            else:
                print(f"   ✅ No subscription (as expected)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Verification error: {e}")
        return False


def show_database_summary():
    """Show a summary of the database contents"""
    print("\n📊 Database Summary:")
    print("=" * 30)
    
    try:
        db_helper = MySQLHelper()
        
        # Count orders by type
        db_helper.cursor.execute("""
            SELECT order_type, COUNT(*) as count 
            FROM orders 
            GROUP BY order_type 
            ORDER BY count DESC
        """)
        
        order_counts = db_helper.cursor.fetchall()
        print("\n📋 Orders by Type:")
        for order in order_counts:
            print(f"   - {order['order_type']}: {order['count']}")
        
        # Count subscriptions by type
        db_helper.cursor.execute("""
            SELECT subscription_type, COUNT(*) as count 
            FROM subscriptions 
            GROUP BY subscription_type 
            ORDER BY count DESC
        """)
        
        subscription_counts = db_helper.cursor.fetchall()
        print("\n📋 Subscriptions by Type:")
        for subscription in subscription_counts:
            print(f"   - {subscription['subscription_type']}: {subscription['count']}")
        
        # Count test results
        db_helper.cursor.execute("SELECT COUNT(*) as count FROM test_results")
        test_count = db_helper.cursor.fetchone()['count']
        print(f"\n📋 Total Test Results: {test_count}")
        
        db_helper.close()
        
    except Exception as e:
        print(f"❌ Error showing summary: {e}")


def main():
    """Main function"""
    print("🚀 Subscription Categorization Test")
    print("=" * 50)
    
    # Run the categorization test
    success = test_subscription_categorization()
    
    if success:
        # Show database summary
        show_database_summary()
        
        print("\n🎉 Categorization test completed successfully!")
        print("✅ All test results are now properly categorized:")
        print("   - Book purchases → orders table only")
        print("   - All subscription types → both orders and subscriptions tables")
    else:
        print("\n❌ Categorization test failed")
        print("Please check the database configuration and table structure")


if __name__ == "__main__":
    main() 
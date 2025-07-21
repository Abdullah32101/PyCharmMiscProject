#!/usr/bin/env python3
"""
Comprehensive Test Results Viewer
Shows test results from all database tables with detailed analysis.
"""

from db.db_helper import MySQLHelper
from datetime import datetime
import sys

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def print_subheader(title):
    """Print a formatted subheader"""
    print(f"\n📋 {title}")
    print("-" * 50)

class ComprehensiveResultsViewer:
    def __init__(self):
        self.db_helper = MySQLHelper()
    
    def show_test_results_summary(self):
        """Show comprehensive test results summary"""
        print_header("COMPREHENSIVE TEST RESULTS SUMMARY")
        
        # Get test results statistics
        stats = self.db_helper.get_test_statistics()
        if stats:
            total = stats['total_tests']
            passed = stats['passed_tests']
            failed = stats['failed_tests']
            skipped = stats['skipped_tests']
            error = stats['error_tests']
            
            print(f"📊 Overall Test Statistics:")
            print(f"   Total Tests: {total}")
            print(f"   ✅ Passed: {passed} ({passed/total*100:.1f}%)" if total > 0 else "   ✅ Passed: 0")
            print(f"   ❌ Failed: {failed} ({failed/total*100:.1f}%)" if total > 0 else "   ❌ Failed: 0")
            print(f"   ⏭️ Skipped: {skipped} ({skipped/total*100:.1f}%)" if total > 0 else "   ⏭️ Skipped: 0")
            print(f"   ⚠️ Errors: {error} ({error/total*100:.1f}%)" if total > 0 else "   ⚠️ Errors: 0")
        
        # Show data from all tables
        self.show_table_summaries()
    
    def show_table_summaries(self):
        """Show summaries from all tables"""
        print_subheader("Database Table Summaries")
        
        # Test Results Table
        self.show_test_results_count()
        
        # Users Table
        self.show_users_summary()
        
        # Books Table
        self.show_books_summary()
        
        # Orders Table
        self.show_orders_summary()
        
        # Subscriptions Table
        self.show_subscriptions_summary()
    
    def show_test_results_count(self):
        """Show test results count"""
        try:
            self.db_helper.cursor.execute("SELECT COUNT(*) as count FROM test_results")
            result = self.db_helper.cursor.fetchone()
            count = result['count'] if result else 0
            print(f"📋 test_results: {count} records")
        except Exception as e:
            print(f"❌ Error getting test_results count: {e}")
    
    def show_users_summary(self):
        """Show users table summary"""
        try:
            # Total users
            self.db_helper.cursor.execute("SELECT COUNT(*) as count FROM users")
            result = self.db_helper.cursor.fetchone()
            total_users = result['count'] if result else 0
            
            # Users by type
            self.db_helper.cursor.execute("""
                SELECT user_type, COUNT(*) as count 
                FROM users 
                GROUP BY user_type
            """)
            user_types = self.db_helper.cursor.fetchall()
            
            print(f"👥 users: {total_users} total users")
            for user_type in user_types:
                print(f"   - {user_type['user_type']}: {user_type['count']}")
                
        except Exception as e:
            print(f"❌ Error getting users summary: {e}")
    
    def show_books_summary(self):
        """Show books table summary"""
        try:
            # Total books
            self.db_helper.cursor.execute("SELECT COUNT(*) as count FROM books")
            result = self.db_helper.cursor.fetchone()
            total_books = result['count'] if result else 0
            
            # Available books
            self.db_helper.cursor.execute("SELECT COUNT(*) as count FROM books WHERE is_available = TRUE")
            result = self.db_helper.cursor.fetchone()
            available_books = result['count'] if result else 0
            
            print(f"📚 books: {total_books} total books ({available_books} available)")
            
        except Exception as e:
            print(f"❌ Error getting books summary: {e}")
    
    def show_orders_summary(self):
        """Show orders table summary"""
        try:
            # Total orders
            self.db_helper.cursor.execute("SELECT COUNT(*) as count FROM orders")
            result = self.db_helper.cursor.fetchone()
            total_orders = result['count'] if result else 0
            
            # Orders by type
            self.db_helper.cursor.execute("""
                SELECT order_type, COUNT(*) as count 
                FROM orders 
                GROUP BY order_type
            """)
            order_types = self.db_helper.cursor.fetchall()
            
            # Orders by status
            self.db_helper.cursor.execute("""
                SELECT order_status, COUNT(*) as count 
                FROM orders 
                GROUP BY order_status
            """)
            order_statuses = self.db_helper.cursor.fetchall()
            
            print(f"🛒 orders: {total_orders} total orders")
            print("   By Type:")
            for order_type in order_types:
                print(f"     - {order_type['order_type']}: {order_type['count']}")
            print("   By Status:")
            for status in order_statuses:
                print(f"     - {status['order_status']}: {status['count']}")
                
        except Exception as e:
            print(f"❌ Error getting orders summary: {e}")
    
    def show_subscriptions_summary(self):
        """Show subscriptions table summary"""
        try:
            # Total subscriptions
            self.db_helper.cursor.execute("SELECT COUNT(*) as count FROM subscriptions")
            result = self.db_helper.cursor.fetchone()
            total_subs = result['count'] if result else 0
            
            # Subscriptions by type
            self.db_helper.cursor.execute("""
                SELECT subscription_type, COUNT(*) as count 
                FROM subscriptions 
                GROUP BY subscription_type
            """)
            sub_types = self.db_helper.cursor.fetchall()
            
            # Subscriptions by status
            self.db_helper.cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM subscriptions 
                GROUP BY status
            """)
            sub_statuses = self.db_helper.cursor.fetchall()
            
            print(f"📅 subscriptions: {total_subs} total subscriptions")
            print("   By Type:")
            for sub_type in sub_types:
                print(f"     - {sub_type['subscription_type']}: {sub_type['count']}")
            print("   By Status:")
            for status in sub_statuses:
                print(f"     - {status['status']}: {status['count']}")
                
        except Exception as e:
            print(f"❌ Error getting subscriptions summary: {e}")
    
    def show_recent_test_activity(self, limit=10):
        """Show recent test activity across all tables"""
        print_header(f"RECENT TEST ACTIVITY (Last {limit})")
        
        try:
            # Get recent test results
            self.db_helper.cursor.execute("""
                SELECT tr.*, 
                       u.username as user_name,
                       o.order_number,
                       s.subscription_type
                FROM test_results tr
                LEFT JOIN users u ON u.username LIKE 'test_user%'
                LEFT JOIN orders o ON o.order_number LIKE 'TEST-%'
                LEFT JOIN subscriptions s ON s.user_id = u.id
                ORDER BY tr.test_datetime DESC
                LIMIT %s
            """, (limit,))
            
            results = self.db_helper.cursor.fetchall()
            
            if not results:
                print("No recent test activity found.")
                return
            
            print(f"{'Test Case':<30} {'Module':<20} {'Status':<10} {'DateTime':<20} {'Order/Sub':<15}")
            print("-" * 100)
            
            for result in results:
                test_name = result['test_case_name'][:29]
                module_name = result['module_name'][:19]
                status_emoji = {
                    'PASSED': '✅',
                    'FAILED': '❌',
                    'SKIPPED': '⏭️',
                    'ERROR': '⚠️'
                }.get(result['test_status'], '❓')
                
                test_datetime = result['test_datetime'].strftime('%Y-%m-%d %H:%M') if result['test_datetime'] else 'N/A'
                order_sub = result['order_number'] or result['subscription_type'] or 'N/A'
                
                print(f"{test_name:<30} {module_name:<20} {status_emoji} {result['test_status']:<8} {test_datetime:<20} {order_sub:<15}")
                
        except Exception as e:
            print(f"❌ Error showing recent activity: {e}")
    
    def show_test_type_breakdown(self):
        """Show breakdown of tests by type"""
        print_header("TEST TYPE BREAKDOWN")
        
        try:
            # Analyze test names to categorize them
            self.db_helper.cursor.execute("""
                SELECT 
                    CASE 
                        WHEN test_case_name LIKE '%book%' OR module_name LIKE '%book%' THEN 'Book Tests'
                        WHEN test_case_name LIKE '%monthly%' OR module_name LIKE '%monthly%' THEN 'Monthly Plan Tests'
                        WHEN test_case_name LIKE '%six_month%' OR module_name LIKE '%six_month%' THEN 'Six Month Plan Tests'
                        WHEN test_case_name LIKE '%onetime%' OR module_name LIKE '%onetime%' THEN 'Onetime Plan Tests'
                        WHEN test_case_name LIKE '%user%' OR module_name LIKE '%user%' THEN 'User Tests'
                        ELSE 'Other Tests'
                    END as test_category,
                    COUNT(*) as total_tests,
                    SUM(CASE WHEN test_status = 'PASSED' THEN 1 ELSE 0 END) as passed_tests,
                    SUM(CASE WHEN test_status = 'FAILED' THEN 1 ELSE 0 END) as failed_tests
                FROM test_results
                GROUP BY test_category
                ORDER BY total_tests DESC
            """)
            
            categories = self.db_helper.cursor.fetchall()
            
            if not categories:
                print("No test categories found.")
                return
            
            print(f"{'Test Category':<20} {'Total':<8} {'Passed':<8} {'Failed':<8} {'Success Rate':<12}")
            print("-" * 60)
            
            for category in categories:
                total = category['total_tests']
                passed = category['passed_tests']
                failed = category['failed_tests']
                success_rate = (passed / total * 100) if total > 0 else 0
                
                print(f"{category['test_category']:<20} {total:<8} {passed:<8} {failed:<8} {success_rate:.1f}%")
                
        except Exception as e:
            print(f"❌ Error showing test type breakdown: {e}")
    
    def show_failed_tests_details(self):
        """Show detailed information about failed tests"""
        print_header("FAILED TESTS DETAILS")
        
        try:
            self.db_helper.cursor.execute("""
                SELECT tr.*, 
                       u.username as user_name,
                       o.order_number,
                       o.order_type,
                       s.subscription_type
                FROM test_results tr
                LEFT JOIN users u ON u.username LIKE 'test_user%'
                LEFT JOIN orders o ON o.order_number LIKE 'TEST-%'
                LEFT JOIN subscriptions s ON s.user_id = u.id
                WHERE tr.test_status IN ('FAILED', 'ERROR')
                ORDER BY tr.test_datetime DESC
            """)
            
            failed_tests = self.db_helper.cursor.fetchall()
            
            if not failed_tests:
                print("No failed tests found.")
                return
            
            for i, test in enumerate(failed_tests, 1):
                print(f"\n🔍 Failed Test {i}:")
                print(f"   Test Case: {test['test_case_name']}")
                print(f"   Module: {test['module_name']}")
                print(f"   Status: {test['test_status']}")
                print(f"   DateTime: {test['test_datetime']}")
                if test['error_message']:
                    print(f"   Error: {test['error_message'][:200]}...")
                if test['order_number']:
                    print(f"   Related Order: {test['order_number']} ({test['order_type']})")
                if test['subscription_type']:
                    print(f"   Related Subscription: {test['subscription_type']}")
                print("-" * 50)
                
        except Exception as e:
            print(f"❌ Error showing failed tests details: {e}")
    
    def close(self):
        """Close database connection"""
        self.db_helper.close()

def print_help():
    """Print help information"""
    print("""
🔍 Comprehensive Test Results Viewer

Usage: python view_comprehensive_results.py [command]

Commands:
  summary              - Show comprehensive test results summary
  recent [limit]       - Show recent test activity
  breakdown            - Show test type breakdown
  failed               - Show failed tests details
  help                 - Show this help message

Examples:
  python view_comprehensive_results.py summary
  python view_comprehensive_results.py recent 20
  python view_comprehensive_results.py breakdown
  python view_comprehensive_results.py failed
""")

def main():
    """Main function"""
    try:
        viewer = ComprehensiveResultsViewer()
        
        if len(sys.argv) < 2:
            print_help()
            return
        
        command = sys.argv[1].lower()
        
        if command == "help":
            print_help()
        
        elif command == "summary":
            viewer.show_test_results_summary()
        
        elif command == "recent":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            viewer.show_recent_test_activity(limit)
        
        elif command == "breakdown":
            viewer.show_test_type_breakdown()
        
        elif command == "failed":
            viewer.show_failed_tests_details()
        
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
        
        viewer.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your database configuration in db/db_config.py")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Test New Database Connection Script
Verifies that the new database is working correctly
"""

from db.db_helper import MySQLHelper
from datetime import datetime


class NewDatabaseTester:
    def __init__(self):
        self.db_helper = MySQLHelper()

    def test_connection(self):
        """Test basic database connection"""
        try:
            print("🔌 Testing database connection...")
            self.db_helper.cursor.execute("SELECT 1")
            result = self.db_helper.cursor.fetchone()
            print("✅ Database connection successful")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False

    def test_table_access(self):
        """Test access to all tables"""
        try:
            print("\n📋 Testing table access...")
            
            # Get all tables
            self.db_helper.cursor.execute("SHOW TABLES")
            tables = self.db_helper.cursor.fetchall()
            
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"   - {table_name}")
            
            return True
        except Exception as e:
            print(f"❌ Table access test failed: {e}")
            return False

    def test_test_results_table(self):
        """Test the test_results table specifically"""
        try:
            print("\n🔍 Testing test_results table...")
            
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
            
            print(f"📋 Table structure ({len(columns)} columns):")
            for col in columns:
                print(f"   - {col['Field']} ({col['Type']})")
            
            # Check record count
            self.db_helper.cursor.execute("SELECT COUNT(*) as count FROM test_results")
            count_result = self.db_helper.cursor.fetchone()
            record_count = count_result['count'] if count_result else 0
            
            print(f"📊 Table contains {record_count} records")
            
            return True
        except Exception as e:
            print(f"❌ test_results table test failed: {e}")
            return False

    def test_insert_functionality(self):
        """Test inserting a test record"""
        try:
            print("\n📝 Testing insert functionality...")
            
            # Insert a test record
            test_data = {
                'test_case_name': 'test_new_database_connection',
                'module_name': 'database_test',
                'test_status': 'PASSED',
                'error_message': None,
                'total_time_duration': 0.123,
                'device_name': 'desktop',
                'screen_resolution': '1920x1080',
                'error_link': None
            }
            
            self.db_helper.insert_test_result(**test_data)
            print("✅ Test record inserted successfully")
            
            # Verify the record was inserted
            self.db_helper.cursor.execute(
                "SELECT * FROM test_results WHERE test_case_name = 'test_new_database_connection' ORDER BY id DESC LIMIT 1"
            )
            result = self.db_helper.cursor.fetchone()
            
            if result:
                print("✅ Test record verified in database")
                return True
            else:
                print("❌ Test record not found in database")
                return False
                
        except Exception as e:
            print(f"❌ Insert functionality test failed: {e}")
            return False

    def test_query_functionality(self):
        """Test querying test results"""
        try:
            print("\n🔍 Testing query functionality...")
            
            # Get recent test results
            results = self.db_helper.get_test_results(limit=5)
            
            print(f"✅ Retrieved {len(results)} recent test results")
            
            if results:
                print("📋 Sample results:")
                for i, result in enumerate(results[:3], 1):
                    print(f"   {i}. {result['test_case_name']} - {result['test_status']} ({result['test_datetime']})")
            
            return True
        except Exception as e:
            print(f"❌ Query functionality test failed: {e}")
            return False

    def test_statistics_functionality(self):
        """Test getting test statistics"""
        try:
            print("\n📊 Testing statistics functionality...")
            
            stats = self.db_helper.get_test_statistics()
            
            if stats:
                print("✅ Test statistics retrieved:")
                print(f"   - Total tests: {stats['total_tests']}")
                print(f"   - Passed: {stats['passed_tests']}")
                print(f"   - Failed: {stats['failed_tests']}")
                print(f"   - Skipped: {stats['skipped_tests']}")
                print(f"   - Errors: {stats['error_tests']}")
            else:
                print("⚠️ No statistics available")
            
            return True
        except Exception as e:
            print(f"❌ Statistics functionality test failed: {e}")
            return False

    def run_all_tests(self):
        """Run all database tests"""
        print("🧪 Running new database tests...")
        print("=" * 60)
        
        tests = [
            ("Connection Test", self.test_connection),
            ("Table Access Test", self.test_table_access),
            ("Test Results Table Test", self.test_test_results_table),
            ("Insert Functionality Test", self.test_insert_functionality),
            ("Query Functionality Test", self.test_query_functionality),
            ("Statistics Functionality Test", self.test_statistics_functionality),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running {test_name}...")
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        
        print("\n" + "=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! New database is working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the errors above.")
        
        return passed == total

    def close(self):
        """Close database connection"""
        self.db_helper.close()


def main():
    """Main test function"""
    tester = NewDatabaseTester()
    
    try:
        success = tester.run_all_tests()
        
        if success:
            print("\n✅ New database integration is complete and working!")
            print("🚀 You can now use the new database for your tests.")
        else:
            print("\n❌ Database integration has issues. Please fix them before proceeding.")
            
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
    
    finally:
        tester.close()


if __name__ == "__main__":
    main() 
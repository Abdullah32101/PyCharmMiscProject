#!/usr/bin/env python3
"""
Test Database Integration
A simple script to test the database integration functionality.
"""

import pytest

from db.db_helper import MySQLHelper


def test_database_connection():
    """Test database connection and table creation"""
    try:
        db_helper = MySQLHelper()
        db_helper.create_test_results_table()
        print("✅ Database connection successful")
        db_helper.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_insert_test_result():
    """Test inserting a test result"""
    try:
        db_helper = MySQLHelper()

        # Insert a test result
        db_helper.insert_test_result(
            test_case_name="test_database_integration",
            module_name="test_db_integration",
            test_status="PASSED",
            error_message=None,
        )

        # Get statistics to verify
        stats = db_helper.get_test_statistics()
        if not (stats and "total_tests" in stats and stats["total_tests"] > 0):
            print("❌ No test records found")
            return False
            
        print("✅ Test result insertion successful")
        db_helper.close()
        return True
    except Exception as e:
        print(f"❌ Test result insertion failed: {e}")
        return False


def test_get_test_result():
    """Test retrieving test results"""
    try:
        db_helper = MySQLHelper()
        results = db_helper.get_test_results(limit=10)
        print(f"✅ Retrieved {len(results)} test results")
        if not isinstance(results, list):
            print("❌ Results should be a list")
            return False
        db_helper.close()
        return True
    except Exception as e:
        print(f"❌ Get test results failed: {e}")
        return False


def main():
    """Run all database integration tests"""
    print("🔧 Testing Database Integration...")
    print("=" * 50)

    tests = [
        ("Database Connection", test_database_connection),
        ("Insert Test Result", test_insert_test_result),
        ("Get Test Results", test_get_test_result),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED")

    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All database integration tests passed!")
        print("Your database integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check your database configuration.")

    return passed == total


if __name__ == "__main__":
    main()

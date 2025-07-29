#!/usr/bin/env python3
"""
Test Results Viewer
A utility script to view and analyze test results stored in the database.
"""

import sys
from datetime import datetime

from db.db_helper import MySQLHelper


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_test_results(results):
    """Print test results in a formatted table"""
    if not results:
        print("No test results found.")
        return

    print(
        f"{'ID':<4} {'Test Case Name':<18} {'Module':<10} {'Status':<8} {'Duration':<8} {'Device':<8} {'Resolution':<12} {'DateTime':<16} {'Error Summary':<20}"
    )
    print("-" * 130)

    for result in results:
        test_datetime = (
            result["test_datetime"].strftime("%Y-%m-%d %H:%M")
            if result["test_datetime"]
            else "N/A"
        )
        status_emoji = {
            "PASSED": "✅",
            "FAILED": "❌",
            "SKIPPED": "⏭️",
            "ERROR": "⚠️",
        }.get(result["test_status"], "❓")

        # Format duration
        duration = result.get("total_time_duration")
        if duration:
            if duration < 60:
                duration_str = f"{duration:.1f}s"
            else:
                minutes = int(duration // 60)
                seconds = duration % 60
                duration_str = f"{minutes}m{seconds:.1f}s"
        else:
            duration_str = "N/A"

        # Format device name
        device_name = result.get("device_name", "unknown") or "unknown"
        if device_name == "desktop":
            device_emoji = "🖥️"
        elif "iPhone" in device_name or "Pixel" in device_name:
            device_emoji = "📱"
        elif "iPad" in device_name:
            device_emoji = "📱"
        else:
            device_emoji = "❓"

        # Format screen resolution
        screen_resolution = result.get("screen_resolution", "unknown") or "unknown"
        if screen_resolution == "unknown":
            resolution_str = "N/A"
        else:
            resolution_str = screen_resolution

        error_summary = result.get("error_summary", "") or ""
        if len(error_summary) > 18:
            error_summary = error_summary[:15] + "..."

        print(
            f"{result['id']:<4} {result['test_case_name'][:17]:<18} {result['module_name'][:9]:<10} {status_emoji} {result['test_status']:<6} {duration_str:<8} {device_emoji} {device_name[:6]:<6} {resolution_str:<12} {test_datetime:<16} {error_summary:<20}"
        )


def print_statistics(stats):
    """Print test statistics"""
    if not stats:
        print("No statistics available.")
        return

    total = stats["total_tests"]
    passed = stats["passed_tests"]
    failed = stats["failed_tests"]
    skipped = stats["skipped_tests"]
    error = stats["error_tests"]

    print(f"\n📊 Test Statistics:")
    print(f"   Total Tests: {total}")
    print(
        f"   ✅ Passed: {passed} ({passed/total*100:.1f}%)"
        if total > 0
        else "   ✅ Passed: 0"
    )
    print(
        f"   ❌ Failed: {failed} ({failed/total*100:.1f}%)"
        if total > 0
        else "   ❌ Failed: 0"
    )
    print(
        f"   ⏭️ Skipped: {skipped} ({skipped/total*100:.1f}%)"
        if total > 0
        else "   ⏭️ Skipped: 0"
    )
    print(
        f"   ⚠️ Errors: {error} ({error/total*100:.1f}%)"
        if total > 0
        else "   ⚠️ Errors: 0"
    )


def show_failed_tests(db_helper):
    """Show only failed tests"""
    print_header("FAILED TESTS")

    # Get failed tests
    failed_query = """
    SELECT * FROM test_results 
    WHERE test_status IN ('FAILED', 'ERROR')
    ORDER BY test_datetime DESC
    """

    try:
        db_helper.cursor.execute(failed_query)
        failed_results = db_helper.cursor.fetchall()
        print_test_results(failed_results)

        # Show error details for failed tests
        if failed_results:
            print_header("FAILED TEST DETAILS")
            for result in failed_results:
                print(f"\n🔍 Test: {result['test_case_name']}")
                print(f"   Module: {result['module_name']}")
                print(f"   Status: {result['test_status']}")
                print(f"   DateTime: {result['test_datetime']}")
                if result.get("error_summary"):
                    print(f"   Error Summary: {result['error_summary']}")
                if result["error_message"]:
                    print(f"   Full Error: {result['error_message'][:200]}...")
                print("-" * 40)

    except Exception as e:
        print(f"❌ Error fetching failed tests: {e}")


def show_recent_tests(db_helper, limit=20):
    """Show recent test results"""
    print_header(f"RECENT TEST RESULTS (Last {limit})")
    results = db_helper.get_test_results(limit)
    print_test_results(results)


def show_module_breakdown(db_helper):
    """Show test results breakdown by module"""
    print_header("TEST RESULTS BY MODULE")

    module_query = """
    SELECT 
        module_name,
        COUNT(*) as total_tests,
        SUM(CASE WHEN test_status = 'PASSED' THEN 1 ELSE 0 END) as passed_tests,
        SUM(CASE WHEN test_status = 'FAILED' THEN 1 ELSE 0 END) as failed_tests,
        SUM(CASE WHEN test_status = 'SKIPPED' THEN 1 ELSE 0 END) as skipped_tests,
        SUM(CASE WHEN test_status = 'ERROR' THEN 1 ELSE 0 END) as error_tests
    FROM test_results
    GROUP BY module_name
    ORDER BY total_tests DESC
    """

    try:
        db_helper.cursor.execute(module_query)
        module_results = db_helper.cursor.fetchall()

        if not module_results:
            print("No test results found.")
            return

        print(
            f"{'Module Name':<25} {'Total':<8} {'Passed':<8} {'Failed':<8} {'Skipped':<8} {'Errors':<8}"
        )
        print("-" * 75)

        for result in module_results:
            total = result["total_tests"]
            passed = result["passed_tests"]
            failed = result["failed_tests"]
            skipped = result["skipped_tests"]
            error = result["error_tests"]

            print(
                f"{result['module_name'][:24]:<25} {total:<8} {passed:<8} {failed:<8} {skipped:<8} {error:<8}"
            )

    except Exception as e:
        print(f"❌ Error fetching module breakdown: {e}")


def main():
    """Main function to run the test results viewer"""
    try:
        db_helper = MySQLHelper()

        if len(sys.argv) > 1:
            command = sys.argv[1].lower()

            if command == "failed":
                show_failed_tests(db_helper)
            elif command == "stats":
                stats = db_helper.get_test_statistics()
                print_statistics(stats)
            elif command == "modules":
                show_module_breakdown(db_helper)
            elif command == "recent":
                limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
                show_recent_tests(db_helper, limit)
            else:
                print(
                    "❌ Unknown command. Available commands: failed, stats, modules, recent [limit]"
                )
        else:
            # Default: show recent tests and statistics
            show_recent_tests(db_helper)
            stats = db_helper.get_test_statistics()
            print_statistics(stats)

        db_helper.close()

    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        print("Make sure your database is running and configuration is correct.")


if __name__ == "__main__":
    main()

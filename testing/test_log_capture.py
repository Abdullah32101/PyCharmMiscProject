#!/usr/bin/env python3
"""
Test Log Capture System
Tests the comprehensive log capture functionality.
"""

import os
import sys
from datetime import datetime

from capture_all_test_logs import ComprehensiveLogCapture


def test_log_capture():
    """Test the log capture system"""
    print("🧪 Testing Log Capture System")
    print("=" * 50)
    
    try:
        # Initialize capture system
        capture = ComprehensiveLogCapture()
        
        # Test capturing logs
        print("📋 Testing log capture functionality...")
        capture.capture_all_logs()
        
        # Test database connection
        print("\n📋 Testing database connection...")
        results = capture.db_helper.get_test_results(limit=5)
        
        if results:
            print(f"✅ Found {len(results)} test results in database")
            for result in results:
                print(f"   - {result['test_case_name']} ({result['test_status']})")
        else:
            print("⚠️ No test results found in database")
        
        # Test statistics
        print("\n📋 Testing statistics...")
        stats = capture.db_helper.get_test_statistics()
        
        if stats:
            print(f"✅ Database statistics:")
            print(f"   Total Tests: {stats['total_tests']}")
            print(f"   Passed: {stats['passed_tests']}")
            print(f"   Failed: {stats['failed_tests']}")
            print(f"   Skipped: {stats['skipped_tests']}")
            print(f"   Errors: {stats['error_tests']}")
        else:
            print("⚠️ Could not retrieve statistics")
        
        # Close connections
        capture.close()
        
        print("\n✅ Log capture test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Log capture test failed: {e}")
        return False


def test_github_actions_parser():
    """Test GitHub Actions log parser"""
    print("\n🧪 Testing GitHub Actions Log Parser")
    print("=" * 50)
    
    try:
        from github_actions_log_parser import GitHubActionsLogParser
        
        # Initialize parser
        parser = GitHubActionsLogParser()
        
        # Test parsing current workflow logs
        print("📋 Testing workflow log parsing...")
        parser.parse_current_workflow_logs()
        
        # Close connections
        parser.close()
        
        print("✅ GitHub Actions parser test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ GitHub Actions parser test failed: {e}")
        return False


def create_test_logs():
    """Create some test log files for testing"""
    print("\n📝 Creating test log files...")
    
    try:
        # Create test log files
        test_logs = [
            ("test_success.log", "Test passed successfully\nStatus: PASSED\nDuration: 2.5s"),
            ("test_failure.log", "Test failed with error\nStatus: FAILED\nError: Element not found"),
            ("pytest_output.log", "pytest test_file.py::test_function PASSED\npytest test_file.py::test_another FAILED"),
            ("coverage_report.log", "Coverage report generated\nTotal coverage: 85%\nMissing lines: 15")
        ]
        
        for filename, content in test_logs:
            with open(filename, 'w') as f:
                f.write(content)
            print(f"✅ Created {filename}")
        
        # Create test report directory
        os.makedirs("test_reports", exist_ok=True)
        
        # Create HTML test report
        html_report = """
        <html>
        <head><title>Test Report</title></head>
        <body>
        <h1>Test Results</h1>
        <p>Passed: 5</p>
        <p>Failed: 2</p>
        <p>Errors: 0</p>
        </body>
        </html>
        """
        
        with open("test_reports/report.html", 'w') as f:
            f.write(html_report)
        print("✅ Created test_reports/report.html")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating test logs: {e}")
        return False


def cleanup_test_logs():
    """Clean up test log files"""
    print("\n🧹 Cleaning up test log files...")
    
    try:
        test_files = [
            "test_success.log",
            "test_failure.log", 
            "pytest_output.log",
            "coverage_report.log"
        ]
        
        for filename in test_files:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"✅ Removed {filename}")
        
        # Remove test reports directory
        if os.path.exists("test_reports"):
            import shutil
            shutil.rmtree("test_reports")
            print("✅ Removed test_reports directory")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning up test logs: {e}")
        return False


def main():
    """Main test function"""
    print("🔧 Test Log Capture System")
    print("=" * 60)
    
    try:
        # Create test logs
        if not create_test_logs():
            print("❌ Failed to create test logs")
            return False
        
        # Test log capture
        if not test_log_capture():
            print("❌ Log capture test failed")
            return False
        
        # Test GitHub Actions parser
        if not test_github_actions_parser():
            print("❌ GitHub Actions parser test failed")
            return False
        
        # Clean up
        if not cleanup_test_logs():
            print("❌ Failed to clean up test logs")
            return False
        
        print("\n🎉 All tests passed successfully!")
        print("✅ Log capture system is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
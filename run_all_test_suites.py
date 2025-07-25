#!/usr/bin/env python3
"""
Comprehensive Test Suite Runner
Runs all test suites and stores results in database.
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

from db.db_helper import MySQLHelper


class TestSuiteRunner:
    def __init__(self):
        self.db_helper = MySQLHelper()
        self.test_results = []
        self.start_time = datetime.now()
        
    def run_all_test_suites(self):
        """Run all test suites and store results"""
        print("🚀 Running All Test Suites")
        print("=" * 60)
        
        # Define all test suites
        test_suites = [
            {
                'name': 'Smoke Tests',
                'file': 'tests/test_ci_smoke.py',
                'description': 'Fast CI smoke tests for basic functionality'
            },
            {
                'name': 'One-Time Book Purchase',
                'file': 'tests/test_one_time_book_purchase.py',
                'description': 'One-time book purchase workflow tests'
            },
            {
                'name': 'Monthly Plan Tests',
                'file': 'tests/test_purchase_membership_question_by_monthly_plan.py',
                'description': 'Monthly subscription plan tests'
            },
            {
                'name': 'One-Time Plan Tests',
                'file': 'tests/test_purchase_membership_question_by_one_time_plan.py',
                'description': 'One-time subscription plan tests'
            },
            {
                'name': 'Three Month Popular Plan Tests',
                'file': 'tests/test_purchase_membership_question_by_three_month_popular_plan.py',
                'description': 'Three-month popular subscription plan tests'
            },
            {
                'name': 'Six Month Plan Tests',
                'file': 'tests/test_purchase_membership_questions_by_six_month_plan.py',
                'description': 'Six-month subscription plan tests'
            }
        ]
        
        # Run each test suite
        for suite in test_suites:
            self._run_test_suite(suite)
        
        # Run additional test files
        self._run_additional_tests()
        
        # Generate summary
        self._generate_summary()
        
    def _run_test_suite(self, suite):
        """Run individual test suite"""
        print(f"\n📋 Running {suite['name']}...")
        print(f"📄 File: {suite['file']}")
        print(f"📝 Description: {suite['description']}")
        
        start_time = time.time()
        
        try:
            # Run pytest with detailed output
            result = subprocess.run([
                'python', '-m', 'pytest', suite['file'],
                '-v', '--tb=short', '--timeout=300'
            ], capture_output=True, text=True, timeout=600)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Determine test status
            if result.returncode == 0:
                test_status = "PASSED"
                print(f"✅ {suite['name']} - PASSED ({duration:.2f}s)")
            else:
                test_status = "FAILED"
                print(f"❌ {suite['name']} - FAILED ({duration:.2f}s)")
            
            # Store result in database
            self._store_test_result(
                test_case_name=f"test_suite_{suite['name'].lower().replace(' ', '_')}",
                module_name=suite['file'],
                test_status=test_status,
                error_message=f"Test Suite: {suite['name']}\nDescription: {suite['description']}\nDuration: {duration:.2f}s\n\nOutput:\n{result.stdout}\n\nErrors:\n{result.stderr}",
                total_time_duration=duration,
                device_name="github_actions" if os.getenv('GITHUB_ACTIONS') else "local_environment",
                screen_resolution="ci_environment" if os.getenv('GITHUB_ACTIONS') else "local_system"
            )
            
            # Store in results list
            self.test_results.append({
                'name': suite['name'],
                'status': test_status,
                'duration': duration,
                'output': result.stdout,
                'errors': result.stderr
            })
            
        except subprocess.TimeoutExpired:
            test_status = "ERROR"
            duration = time.time() - start_time
            error_message = f"Test suite {suite['name']} timed out after {duration:.2f}s"
            
            print(f"⏰ {suite['name']} - TIMEOUT ({duration:.2f}s)")
            
            self._store_test_result(
                test_case_name=f"test_suite_{suite['name'].lower().replace(' ', '_')}",
                module_name=suite['file'],
                test_status=test_status,
                error_message=error_message,
                total_time_duration=duration,
                device_name="github_actions" if os.getenv('GITHUB_ACTIONS') else "local_environment",
                screen_resolution="ci_environment" if os.getenv('GITHUB_ACTIONS') else "local_system"
            )
            
            self.test_results.append({
                'name': suite['name'],
                'status': test_status,
                'duration': duration,
                'output': '',
                'errors': error_message
            })
            
        except Exception as e:
            test_status = "ERROR"
            duration = time.time() - start_time
            error_message = f"Error running {suite['name']}: {str(e)}"
            
            print(f"💥 {suite['name']} - ERROR ({duration:.2f}s)")
            
            self._store_test_result(
                test_case_name=f"test_suite_{suite['name'].lower().replace(' ', '_')}",
                module_name=suite['file'],
                test_status=test_status,
                error_message=error_message,
                total_time_duration=duration,
                device_name="github_actions" if os.getenv('GITHUB_ACTIONS') else "local_environment",
                screen_resolution="ci_environment" if os.getenv('GITHUB_ACTIONS') else "local_system"
            )
            
            self.test_results.append({
                'name': suite['name'],
                'status': test_status,
                'duration': duration,
                'output': '',
                'errors': error_message
            })
    
    def _run_additional_tests(self):
        """Run additional test files"""
        print(f"\n📋 Running Additional Tests...")
        
        additional_tests = [
            'test_db_integration.py',
            'test_error_link_simple.py',
            'test_ci_cd_trigger.py'
        ]
        
        for test_file in additional_tests:
            if os.path.exists(test_file):
                self._run_single_test(test_file)
    
    def _run_single_test(self, test_file):
        """Run a single test file"""
        print(f"📄 Running {test_file}...")
        
        start_time = time.time()
        
        try:
            result = subprocess.run([
                'python', test_file
            ], capture_output=True, text=True, timeout=300)
            
            end_time = time.time()
            duration = end_time - start_time
            
            test_status = "PASSED" if result.returncode == 0 else "FAILED"
            
            print(f"{'✅' if test_status == 'PASSED' else '❌'} {test_file} - {test_status} ({duration:.2f}s)")
            
            self._store_test_result(
                test_case_name=f"additional_test_{Path(test_file).stem}",
                module_name=test_file,
                test_status=test_status,
                error_message=f"Test File: {test_file}\nDuration: {duration:.2f}s\n\nOutput:\n{result.stdout}\n\nErrors:\n{result.stderr}",
                total_time_duration=duration,
                device_name="github_actions" if os.getenv('GITHUB_ACTIONS') else "local_environment",
                screen_resolution="ci_environment" if os.getenv('GITHUB_ACTIONS') else "local_system"
            )
            
        except Exception as e:
            duration = time.time() - start_time
            error_message = f"Error running {test_file}: {str(e)}"
            
            print(f"💥 {test_file} - ERROR ({duration:.2f}s)")
            
            self._store_test_result(
                test_case_name=f"additional_test_{Path(test_file).stem}",
                module_name=test_file,
                test_status="ERROR",
                error_message=error_message,
                total_time_duration=duration,
                device_name="github_actions" if os.getenv('GITHUB_ACTIONS') else "local_environment",
                screen_resolution="ci_environment" if os.getenv('GITHUB_ACTIONS') else "local_system"
            )
    
    def _store_test_result(self, test_case_name, module_name, test_status, error_message=None,
                          total_time_duration=None, device_name=None, screen_resolution=None, error_link=None):
        """Store test result in database"""
        try:
            self.db_helper.store_test_result_in_tables(
                test_case_name=test_case_name,
                module_name=module_name,
                test_status=test_status,
                error_message=error_message,
                total_time_duration=total_time_duration,
                device_name=device_name or "test_runner",
                screen_resolution=screen_resolution or "test_execution",
                error_link=error_link
            )
            
        except Exception as e:
            print(f"❌ Error storing test result: {e}")
    
    def _generate_summary(self):
        """Generate test execution summary"""
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        print(f"\n📊 Test Execution Summary")
        print("=" * 60)
        print(f"⏱️ Total Duration: {total_duration:.2f}s")
        print(f"📅 Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📅 End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🧪 Test Suites Run: {len(self.test_results)}")
        
        # Count results by status
        passed = sum(1 for r in self.test_results if r['status'] == 'PASSED')
        failed = sum(1 for r in self.test_results if r['status'] == 'FAILED')
        errors = sum(1 for r in self.test_results if r['status'] == 'ERROR')
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"💥 Errors: {errors}")
        
        # Store summary in database
        summary_message = f"""Test Execution Summary:
Total Duration: {total_duration:.2f}s
Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
Test Suites Run: {len(self.test_results)}
Passed: {passed}
Failed: {failed}
Errors: {errors}

Detailed Results:
"""
        
        for result in self.test_results:
            summary_message += f"- {result['name']}: {result['status']} ({result['duration']:.2f}s)\n"
        
        self._store_test_result(
            test_case_name="test_execution_summary",
            module_name="test_suite_runner",
            test_status="PASSED" if failed == 0 and errors == 0 else "FAILED",
            error_message=summary_message,
            total_time_duration=total_duration,
            device_name="github_actions" if os.getenv('GITHUB_ACTIONS') else "local_environment",
            screen_resolution="ci_environment" if os.getenv('GITHUB_ACTIONS') else "local_system"
        )
        
        print(f"\n🎉 Test execution completed!")
        print(f"📊 Results stored in database: {passed + failed + errors} test suites")
        
        # Show recent database results
        self._show_recent_results()
    
    def _show_recent_results(self):
        """Show recent test results from database"""
        try:
            results = self.db_helper.get_test_results(limit=10)
            
            print(f"\n📋 Recent Database Results:")
            print("-" * 40)
            
            for result in results:
                status_emoji = "✅" if result['test_status'] == 'PASSED' else "❌" if result['test_status'] == 'FAILED' else "💥"
                print(f"{status_emoji} {result['test_case_name']} - {result['test_status']} ({result['module_name']})")
            
        except Exception as e:
            print(f"❌ Error showing recent results: {e}")
    
    def close(self):
        """Close database connection"""
        self.db_helper.close()


def main():
    """Main function"""
    try:
        print("🔧 Comprehensive Test Suite Runner")
        print("=" * 60)
        
        # Initialize test runner
        runner = TestSuiteRunner()
        
        # Run all test suites
        runner.run_all_test_suites()
        
        # Close connections
        runner.close()
        
        print(f"\n🎉 All test suites executed and results stored in database!")
        
    except Exception as e:
        print(f"❌ Test suite execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
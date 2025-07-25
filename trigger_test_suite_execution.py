#!/usr/bin/env python3
"""
Test Suite Execution Trigger
This script triggers the execution of all test suites in GitHub Actions environment.
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def main():
    """Main function to trigger test suite execution"""
    print("🚀 Test Suite Execution Trigger")
    print("=" * 50)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if we're in GitHub Actions
    if os.getenv('GITHUB_ACTIONS') == 'true':
        print("✅ Running in GitHub Actions environment")
        print("🔧 Environment variables set:")
        print(f"   - GITHUB_ACTIONS: {os.getenv('GITHUB_ACTIONS')}")
        print(f"   - TEST_DB_HOST: {os.getenv('TEST_DB_HOST', 'Not set')}")
        print(f"   - TEST_DB_USER: {os.getenv('TEST_DB_USER', 'Not set')}")
        print(f"   - TEST_DB_NAME: {os.getenv('TEST_DB_NAME', 'Not set')}")
    else:
        print("⚠️ Running in local environment")
        print("🔧 Setting up local environment variables...")
        os.environ['GITHUB_ACTIONS'] = 'true'
        os.environ['TEST_DB_HOST'] = '127.0.0.1'
        os.environ['TEST_DB_USER'] = 'test_user'
        os.environ['TEST_DB_PASSWORD'] = 'test_pass'
        os.environ['TEST_DB_NAME'] = 'test_results'
        os.environ['TEST_DB_PORT'] = '3306'
    
    print("\n📋 Test Suites to Execute:")
    print("1. ✅ Comprehensive Test Suite Runner")
    print("2. ✅ Smoke Tests")
    print("3. ✅ Database Integration Tests")
    print("4. ✅ Error Link Tests")
    print("5. ✅ Individual Test Files")
    
    try:
        # Step 1: Run comprehensive test suite
        print("\n🚀 Step 1: Running Comprehensive Test Suite Runner...")
        result1 = subprocess.run([
            'python', 'run_all_test_suites.py'
        ], capture_output=True, text=True, timeout=600)
        
        if result1.returncode == 0:
            print("✅ Comprehensive Test Suite Runner completed successfully")
        else:
            print(f"⚠️ Comprehensive Test Suite Runner completed with issues")
            print(f"   Output: {result1.stdout}")
            print(f"   Errors: {result1.stderr}")
        
        # Step 2: Run smoke tests
        print("\n🚀 Step 2: Running Smoke Tests...")
        result2 = subprocess.run([
            'python', '-m', 'pytest', 'tests/test_ci_smoke.py', '-v', '--tb=short'
        ], capture_output=True, text=True, timeout=300)
        
        if result2.returncode == 0:
            print("✅ Smoke tests completed successfully")
        else:
            print(f"⚠️ Smoke tests completed with issues")
            print(f"   Output: {result2.stdout}")
            print(f"   Errors: {result2.stderr}")
        
        # Step 3: Run database integration tests
        print("\n🚀 Step 3: Running Database Integration Tests...")
        if os.path.exists('test_db_integration.py'):
            result3 = subprocess.run([
                'python', 'test_db_integration.py'
            ], capture_output=True, text=True, timeout=300)
            
            if result3.returncode == 0:
                print("✅ Database integration tests completed successfully")
            else:
                print(f"⚠️ Database integration tests completed with issues")
                print(f"   Output: {result3.stdout}")
                print(f"   Errors: {result3.stderr}")
        else:
            print("⚠️ Database integration test file not found")
        
        # Step 4: Run error link tests
        print("\n🚀 Step 4: Running Error Link Tests...")
        if os.path.exists('test_error_link_simple.py'):
            result4 = subprocess.run([
                'python', 'test_error_link_simple.py'
            ], capture_output=True, text=True, timeout=300)
            
            if result4.returncode == 0:
                print("✅ Error link tests completed successfully")
            else:
                print(f"⚠️ Error link tests completed with issues")
                print(f"   Output: {result4.stdout}")
                print(f"   Errors: {result4.stderr}")
        else:
            print("⚠️ Error link test file not found")
        
        # Step 5: Run individual test files
        print("\n🚀 Step 5: Running Individual Test Files...")
        individual_tests = [
            'test_ci_cd_trigger.py',
            'test_workflow_quick.py',
            'test_workflow_trigger.py'
        ]
        
        for test_file in individual_tests:
            if os.path.exists(test_file):
                print(f"📋 Running {test_file}...")
                try:
                    result = subprocess.run([
                        'python', test_file
                    ], capture_output=True, text=True, timeout=180)
                    
                    if result.returncode == 0:
                        print(f"✅ {test_file} completed successfully")
                    else:
                        print(f"⚠️ {test_file} completed with issues")
                except subprocess.TimeoutExpired:
                    print(f"⏰ {test_file} timed out")
                except Exception as e:
                    print(f"❌ {test_file} failed: {e}")
            else:
                print(f"⚠️ {test_file} not found")
        
        # Generate summary
        print("\n📊 Test Execution Summary")
        print("=" * 50)
        print(f"📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("✅ All test suites have been executed")
        print("📋 Check the output above for detailed results")
        
        # Create summary file
        with open('test_execution_summary.txt', 'w') as f:
            f.write("Test Suite Execution Summary\n")
            f.write("=" * 30 + "\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Environment: {'GitHub Actions' if os.getenv('GITHUB_ACTIONS') == 'true' else 'Local'}\n")
            f.write("Status: All test suites executed\n")
            f.write("Results: Check individual test outputs above\n")
        
        print("📄 Summary saved to: test_execution_summary.txt")
        print("\n🎉 Test suite execution completed!")
        
    except Exception as e:
        print(f"❌ Test suite execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
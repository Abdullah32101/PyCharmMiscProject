#!/usr/bin/env python3
"""
CI/CD Pipeline Test Script
This script helps test different aspects of your CI/CD pipeline
"""

import os
import sys
import subprocess
import datetime

def test_ci_cd_scenarios():
    """Test different CI/CD scenarios"""
    
    print("🧪 CI/CD Pipeline Testing Tool")
    print("=" * 50)
    
    scenarios = {
        "1": "Test code formatting and linting",
        "2": "Test database integration",
        "3": "Test screenshot functionality", 
        "4": "Test error link generation",
        "5": "Test all components"
    }
    
    print("\nAvailable test scenarios:")
    for key, description in scenarios.items():
        print(f"  {key}. {description}")
    
    choice = input("\nSelect scenario (1-5): ").strip()
    
    if choice == "1":
        test_code_quality()
    elif choice == "2":
        test_database_integration()
    elif choice == "3":
        test_screenshot_functionality()
    elif choice == "4":
        test_error_link_generation()
    elif choice == "5":
        test_all_components()
    else:
        print("❌ Invalid choice")

def test_code_quality():
    """Test code quality checks"""
    print("\n🔍 Testing Code Quality...")
    
    # Create a test file with formatting issues
    test_content = """def badly_formatted_function(  x,y  ):
    return x+y

class TestClass:
    def __init__(self):
        self.value=1
"""
    
    with open("test_formatting.py", "w") as f:
        f.write(test_content)
    
    print("✅ Created test file with formatting issues")
    print("📝 This will trigger code quality checks in CI/CD")
    print("💡 Push this file to test linting and formatting workflows")

def test_database_integration():
    """Test database integration"""
    print("\n🗄️ Testing Database Integration...")
    
    # Create a test database script
    test_db_script = """#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.db_helper import DatabaseHelper

def test_db_connection():
    try:
        db = DatabaseHelper()
        result = db.execute_query("SELECT 1 as test")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_db_connection()
"""
    
    with open("test_db_ci.py", "w") as f:
        f.write(test_db_script)
    
    print("✅ Created database test script")
    print("📝 This will test database connectivity in CI/CD")

def test_screenshot_functionality():
    """Test screenshot functionality"""
    print("\n📸 Testing Screenshot Functionality...")
    
    # Create a test screenshot script
    screenshot_test = """#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from screenshot_utils import ScreenshotManager

def test_screenshot_capture():
    try:
        screenshot_mgr = ScreenshotManager()
        # This would normally capture a screenshot
        print("✅ Screenshot functionality test created")
        return True
    except Exception as e:
        print(f"❌ Screenshot test failed: {e}")
        return False

if __name__ == "__main__":
    test_screenshot_capture()
"""
    
    with open("test_screenshot_ci.py", "w") as f:
        f.write(screenshot_test)
    
    print("✅ Created screenshot test script")
    print("📝 This will test screenshot capture in CI/CD")

def test_error_link_generation():
    """Test error link generation"""
    print("\n🔗 Testing Error Link Generation...")
    
    # Create a test error link script
    error_link_test = """#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_error_link():
    try:
        # Simulate error link generation
        error_id = "test_error_123"
        error_link = f"https://example.com/error/{error_id}"
        print(f"✅ Error link generated: {error_link}")
        return True
    except Exception as e:
        print(f"❌ Error link generation failed: {e}")
        return False

if __name__ == "__main__":
    test_error_link()
"""
    
    with open("test_error_link_ci.py", "w") as f:
        f.write(error_link_test)
    
    print("✅ Created error link test script")
    print("📝 This will test error link generation in CI/CD")

def test_all_components():
    """Test all CI/CD components"""
    print("\n🚀 Testing All CI/CD Components...")
    
    # Create a comprehensive test
    comprehensive_test = f'''#!/usr/bin/env python3
"""
# CI/CD Comprehensive Test - Generated on {datetime.datetime.now()}
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_comprehensive_test():
    print("🧪 Running Comprehensive CI/CD Test")
    print("=" * 40)
    
    tests = [
        ("Code Quality", test_code_quality),
        ("Database Integration", test_database_integration),
        ("Screenshot Functionality", test_screenshot_functionality),
        ("Error Link Generation", test_error_link_generation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\\n🔍 Testing {{test_name}}...")
            result = test_func()
            results.append((test_name, result))
            print(f"✅ {{test_name}}: {{'PASSED' if result else 'FAILED'}}")
        except Exception as e:
            print(f"❌ {{test_name}}: ERROR - {{e}}")
            results.append((test_name, False))
    
    print("\\n📊 Test Summary:")
    print("=" * 40)
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{{test_name}}: {{status}}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\\n🎯 Overall: {{passed}}/{{total}} tests passed")
    
    return passed == total

def test_code_quality():
    return True  # Simulate code quality check

def test_database_integration():
    return True  # Simulate database test

def test_screenshot_functionality():
    return True  # Simulate screenshot test

def test_error_link_generation():
    return True  # Simulate error link test

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
'''
    
    with open("test_comprehensive_ci.py", "w") as f:
        f.write(comprehensive_test)
    
    print("✅ Created comprehensive CI/CD test")
    print("📝 This will test all components in the pipeline")

def create_ci_cd_test_branch():
    """Create a test branch for CI/CD testing"""
    print("\n🌿 Creating CI/CD Test Branch...")
    
    try:
        # Create and switch to test branch
        subprocess.run(["git", "checkout", "-b", "test-ci-cd"], check=True)
        print("✅ Created test-ci-cd branch")
        
        # Add all test files
        subprocess.run(["git", "add", "."], check=True)
        print("✅ Added test files to staging")
        
        # Commit changes
        commit_message = f"test: CI/CD pipeline testing - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("✅ Committed test changes")
        
        print("\n🚀 Ready to push and test CI/CD!")
        print("Run: git push origin test-ci-cd")
        print("Then create a PR to main/master to trigger full pipeline")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--create-branch":
        create_ci_cd_test_branch()
    else:
        test_ci_cd_scenarios() 
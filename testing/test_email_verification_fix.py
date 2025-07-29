#!/usr/bin/env python3
"""
Test Script: GitHub Actions Email Verification Fix
This script helps verify that the email verification issue is resolved.
"""

import os
import sys
import subprocess
from datetime import datetime

def print_header():
    """Print a formatted header."""
    print("=" * 60)
    print("🔧 GitHub Actions Email Verification Fix Test")
    print("=" * 60)
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def check_git_config():
    """Check Git configuration for email settings."""
    print("🔍 Checking Git Configuration...")
    
    try:
        # Check user email
        result = subprocess.run(['git', 'config', 'user.email'], 
                              capture_output=True, text=True, check=True)
        email = result.stdout.strip()
        print(f"✅ Git User Email: {email}")
        
        # Check user name
        result = subprocess.run(['git', 'config', 'user.name'], 
                              capture_output=True, text=True, check=True)
        name = result.stdout.strip()
        print(f"✅ Git User Name: {name}")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git configuration error: {e}")
        return False

def check_workflow_files():
    """Check if workflow files have the necessary permissions."""
    print("\n🔍 Checking Workflow Files...")
    
    workflow_files = [
        '.github/workflows/scheduled-tests.yml',
        '.github/workflows/test-automation.yml',
        '.github/workflows/deploy-staging.yml'
    ]
    
    all_good = True
    
    for workflow_file in workflow_files:
        if os.path.exists(workflow_file):
            print(f"✅ Found: {workflow_file}")
            
            # Check for enhanced permissions
            with open(workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'actions: read' in content and 'security-events: write' in content:
                    print(f"   ✅ Enhanced permissions found")
                else:
                    print(f"   ⚠️ Enhanced permissions not found")
                    all_good = False
                
                # Check for concurrency control
                if 'concurrency:' in content:
                    print(f"   ✅ Concurrency control found")
                else:
                    print(f"   ⚠️ Concurrency control not found")
                    all_good = False
        else:
            print(f"❌ Missing: {workflow_file}")
            all_good = False
    
    return all_good

def check_database_config():
    """Check database configuration."""
    print("\n🔍 Checking Database Configuration...")
    
    db_config_file = 'db/db_config.py'
    if os.path.exists(db_config_file):
        print(f"✅ Database config found: {db_config_file}")
        
        # Check if it contains the correct configuration
        with open(db_config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'solutionsole.com' in content:
                print("   ✅ Remote database configuration found")
                return True
            else:
                print("   ⚠️ Remote database configuration not found")
                return False
    else:
        print(f"❌ Database config missing: {db_config_file}")
        return False

def provide_next_steps():
    """Provide next steps for testing."""
    print("\n" + "=" * 60)
    print("🚀 Next Steps to Test the Fix")
    print("=" * 60)
    
    print("\n1️⃣ **Verify Your GitHub Email Address:**")
    print("   • Go to: https://github.com/settings/emails")
    print("   • Ensure your email is verified (green checkmark)")
    print("   • If not verified, click 'Verify email address'")
    
    print("\n2️⃣ **Test Manual Workflow Trigger:**")
    print("   • Go to: https://github.com/Abdullah32101/PyCharmMiscProject/actions")
    print("   • Click 'Scheduled Test Runner'")
    print("   • Click 'Run workflow'")
    print("   • Select 'database' for quick test")
    print("   • Click 'Run workflow'")
    
    print("\n3️⃣ **Test Push Trigger:**")
    print("   • Make a small change to any file")
    print("   • Commit and push to trigger workflow")
    print("   • Monitor the workflow run")
    
    print("\n4️⃣ **Check Repository Settings:**")
    print("   • Go to: https://github.com/Abdullah32101/PyCharmMiscProject/settings")
    print("   • Navigate to: Actions → General")
    print("   • Ensure 'Allow all actions' is selected")
    print("   • Check 'Read and write permissions'")
    
    print("\n5️⃣ **Expected Results:**")
    print("   ✅ No email verification errors")
    print("   ✅ Workflow runs successfully")
    print("   ✅ Database connection works (if server accessible)")
    print("   ✅ Test results stored and artifacts uploaded")

def main():
    """Main test function."""
    print_header()
    
    # Run all checks
    git_ok = check_git_config()
    workflow_ok = check_workflow_files()
    db_ok = check_database_config()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    print(f"Git Configuration: {'✅ PASS' if git_ok else '❌ FAIL'}")
    print(f"Workflow Files: {'✅ PASS' if workflow_ok else '❌ FAIL'}")
    print(f"Database Config: {'✅ PASS' if db_ok else '❌ FAIL'}")
    
    if git_ok and workflow_ok and db_ok:
        print("\n🎉 All checks passed! Your setup looks good.")
        print("Follow the next steps to test the email verification fix.")
    else:
        print("\n⚠️ Some checks failed. Please address the issues above.")
    
    provide_next_steps()

if __name__ == "__main__":
    main() 
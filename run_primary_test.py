#!/usr/bin/env python3
"""
Simple script to run the six month plan primary test
"""
import subprocess
import sys
import os

def run_primary_test():
    """Run the six month plan primary test"""
    print("🚀 Running Six Month Plan Primary Test...")
    print("=" * 50)
    
    try:
        # Run the test
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_purchase_membership_questions_by_six_month_plan.py",
            "-k", "primary", 
            "-v"
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        # Print output
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print("=" * 50)
        print(f"Exit Code: {result.returncode}")
        
        if result.returncode == 0:
            print("✅ Test PASSED!")
        else:
            print("❌ Test FAILED!")
            
    except Exception as e:
        print(f"❌ Error running test: {e}")

if __name__ == "__main__":
    run_primary_test() 
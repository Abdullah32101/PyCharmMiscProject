#!/usr/bin/env python3
"""
Quick test to verify dropdown fix for monthly plan test
"""

import os
import sys

import pytest


def test_monthly_plan_dropdown_fix():
    """Test the monthly plan with the fixed dropdown methods"""

    print("[🔧] Testing monthly plan with dropdown fix...")

    # Set environment variable to indicate mobile testing
    os.environ["MOBILE_TEST"] = "true"

    # Run pytest with the monthly plan test
    pytest_args = [
        "tests/test_purchase_membership_question_by_monthly_plan.py::test_purchase_membership_question_by_monthly_plan_flow",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--capture=no",  # Show print statements
        "-s",  # Don't capture stdout/stderr
        "-k",
        "primary",  # Only run primary stage
    ]

    # Run pytest and capture the exit code
    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        print("[✅] Monthly plan test with dropdown fix completed successfully!")
        return True
    else:
        print(f"[❌] Monthly plan test failed with exit code: {exit_code}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("DROPDOWN FIX VERIFICATION TEST")
    print("=" * 60)

    success = test_monthly_plan_dropdown_fix()

    if success:
        print("\n[🎉] Dropdown fix verification passed!")
        sys.exit(0)
    else:
        print("\n[❌] Dropdown fix verification failed!")
        sys.exit(1)

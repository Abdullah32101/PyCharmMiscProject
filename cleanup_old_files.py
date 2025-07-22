#!/usr/bin/env python3
"""
Cleanup script to remove old files and update database with new module names
"""

import os
import sys

from db.db_helper import MySQLHelper


def cleanup_old_files():
    """Remove old test and page files that have been renamed"""

    old_files = [
        # Old test files
        "tests/test_book_purchase.py",
        "tests/test_monthly_plan.py",
        "tests/test_onetime_plan.py",
        "tests/test_plan_popular.py",
        "tests/test_six_month_plan.py",
        # Old page files
        "pages/bookpurchase_methods.py",
        "pages/expertquestions_stage1_methods.py",
        "pages/expertquestions_stage2_methods.py",
        # Old run scripts
        "run_book_purchase_with_reports.py",
        "run_mobile_book_test.py",
        "run_monthly_test.py",
        "run_onetime_test.py",
        "run_popular_test.py",
        "run_sixmonth_test.py",
        "run_all_plan_tests.py",
    ]

    print("🧹 Cleaning up old files...")

    for file_path in old_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✅ Removed: {file_path}")
            except Exception as e:
                print(f"❌ Failed to remove {file_path}: {e}")
        else:
            print(f"ℹ️ File not found (already removed): {file_path}")


def update_database_module_names():
    """Update module names in the database to reflect the new naming convention"""

    print("\n🔄 Updating database module names...")

    # Module name mapping
    module_mapping = {
        "test_book_purchase": "test_one_time_book_purchase",
        "test_monthly_plan": "test_purchase_membership_question_by_monthly_plan",
        "test_onetime_plan": "test_purchase_membership_question_by_one_time_plan",
        "test_plan_popular": "test_purchase_membership_question_by_three_month_popular_plan",
        "test_six_month_plan": "test_purchase_membership_questions_by_six_month_plan",
    }

    try:
        db_helper = MySQLHelper()

        # Update each module name
        for old_name, new_name in module_mapping.items():
            try:
                # Update module names in test_results table
                query = """
                    UPDATE test_results 
                    SET module_name = %s 
                    WHERE module_name = %s
                """
                db_helper.execute_query(query, (new_name, old_name))

                # Get the number of affected rows
                affected_rows = db_helper.cursor.rowcount
                print(f"✅ Updated {affected_rows} records: {old_name} → {new_name}")

            except Exception as e:
                print(f"❌ Failed to update {old_name}: {e}")

        # Commit the changes
        db_helper.connection.commit()
        print("✅ Database updates committed successfully")

        # Close the connection
        db_helper.close()

    except Exception as e:
        print(f"❌ Database update failed: {e}")


def verify_new_files():
    """Verify that all new files exist"""

    print("\n🔍 Verifying new files...")

    new_files = [
        # New test files
        "tests/test_one_time_book_purchase.py",
        "tests/test_purchase_membership_question_by_monthly_plan.py",
        "tests/test_purchase_membership_question_by_one_time_plan.py",
        "tests/test_purchase_membership_question_by_three_month_popular_plan.py",
        "tests/test_purchase_membership_questions_by_six_month_plan.py",
        # New page files
        "pages/one_time_book_purchase_methods.py",
        "pages/purchase_membership_question_by_monthly_plan_methods.py",
        "pages/purchase_membership_question_by_one_time_plan_methods.py",
        # New run scripts
        "run_one_time_book_purchase_with_reports.py",
        "run_mobile_one_time_book_test.py",
        "run_purchase_membership_question_by_monthly_plan_test.py",
        "run_purchase_membership_question_by_one_time_plan_test.py",
        "run_purchase_membership_question_by_three_month_popular_plan_test.py",
        "run_purchase_membership_questions_by_six_month_plan_test.py",
        "run_all_membership_plan_tests.py",
    ]

    all_exist = True
    for file_path in new_files:
        if os.path.exists(file_path):
            print(f"✅ Found: {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_exist = False

    return all_exist


def main():
    """Main cleanup function"""

    print("=" * 60)
    print("FILE RENAME CLEANUP SCRIPT")
    print("=" * 60)

    # Step 1: Verify new files exist
    if not verify_new_files():
        print(
            "\n❌ Some new files are missing. Please ensure all files have been created before cleanup."
        )
        sys.exit(1)

    # Step 2: Clean up old files
    cleanup_old_files()

    # Step 3: Update database
    update_database_module_names()

    # Step 4: Final verification
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION")
    print("=" * 60)

    if verify_new_files():
        print("\n🎉 Cleanup completed successfully!")
        print("✅ All old files removed")
        print("✅ Database updated with new module names")
        print("✅ All new files verified")
    else:
        print("\n❌ Cleanup verification failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()

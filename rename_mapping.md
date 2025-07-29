# File Rename Mapping

## Test Files (tests/)
| Old Name | New Name |
|----------|----------|
| test_book_purchase.py | test_one_time_book_purchase.py |
| test_monthly_plan.py | test_purchase_membership_question_by_monthly_plan.py |
| test_onetime_plan.py | test_purchase_membership_question_by_one_time_plan.py |
| test_plan_popular.py | test_purchase_membership_question_by_three_month_popular_plan.py |
| test_six_month_plan.py | test_purchase_membership_questions_by_six_month_plan.py |

## Page Object Files (pages/)
| Old Name | New Name |
|----------|----------|
| bookpurchase_methods.py | one_time_book_purchase_methods.py |
| expertquestions_stage1_methods.py | purchase_membership_question_by_monthly_plan_methods.py |
| expertquestions_stage2_methods.py | purchase_membership_question_by_one_time_plan_methods.py |

## Run Scripts
| Old Name | New Name |
|----------|----------|
| run_book_purchase_with_reports.py | run_one_time_book_purchase_with_reports.py |
| run_mobile_book_test.py | run_mobile_one_time_book_test.py |
| run_monthly_test.py | run_purchase_membership_question_by_monthly_plan_test.py |
| run_onetime_test.py | run_purchase_membership_question_by_one_time_plan_test.py |
| run_popular_test.py | run_purchase_membership_question_by_three_month_popular_plan_test.py |
| run_sixmonth_test.py | run_purchase_membership_questions_by_six_month_plan_test.py |
| run_all_plan_tests.py | run_all_membership_plan_tests.py |

## Database Updates Needed
- Update test case names in database
- Update module names in database
- Update any references in documentation 
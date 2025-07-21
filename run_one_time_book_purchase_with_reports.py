#!/usr/bin/env python3
"""
One-Time Book Purchase Test Runner with HTML Reports
This script runs the one-time book purchase test on iPad and desktop with detailed HTML reports.
"""

import pytest
import sys
import os
import time
from datetime import datetime

def run_one_time_book_purchase_tests():
    """Run one-time book purchase tests on iPad and desktop with HTML reports"""
    
    # Create reports directory
    reports_dir = "test_reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Generate timestamp for unique report names
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("=" * 80)
    print("ONE-TIME BOOK PURCHASE TEST RUNNER WITH HTML REPORTS")
    print("=" * 80)
    
    # Test configurations
    test_configs = [
        {
            "device": "desktop",
            "description": "Desktop One-Time Book Purchase Test",
            "pytest_args": [
                "tests/test_one_time_book_purchase.py::test_book_page_load_and_click",
                "--html", f"{reports_dir}/one_time_book_purchase_desktop_{timestamp}.html",
                "--self-contained-html",
                "--metadata", "Device", "Desktop",
                "--metadata", "Browser", "Chrome",
                "--metadata", "Test Type", "One-Time Book Purchase",
                "-v"
            ]
        },
        {
            "device": "iPad Pro",
            "description": "iPad Pro One-Time Book Purchase Test",
            "pytest_args": [
                "tests/test_one_time_book_purchase.py::test_book_page_load_and_click",
                "--html", f"{reports_dir}/one_time_book_purchase_ipad_{timestamp}.html",
                "--self-contained-html",
                "--metadata", "Device", "iPad Pro",
                "--metadata", "Browser", "Chrome Mobile",
                "--metadata", "Test Type", "One-Time Book Purchase",
                "-v"
            ]
        }
    ]
    
    results = []
    
    for config in test_configs:
        print(f"\n{'='*60}")
        print(f"Running: {config['description']}")
        print(f"{'='*60}")
        
        try:
            # Run pytest with the specific configuration
            exit_code = pytest.main(config["pytest_args"])
            
            result = {
                "device": config["device"],
                "description": config["description"],
                "exit_code": exit_code,
                "status": "PASSED" if exit_code == 0 else "FAILED",
                "report_file": config["pytest_args"][config["pytest_args"].index("--html") + 1]
            }
            
            results.append(result)
            
            print(f"\n✅ {config['device']} test completed with exit code: {exit_code}")
            print(f"📊 Report saved to: {result['report_file']}")
            
        except Exception as e:
            print(f"\n❌ Error running {config['device']} test: {e}")
            results.append({
                "device": config["device"],
                "description": config["description"],
                "exit_code": -1,
                "status": "ERROR",
                "report_file": "N/A"
            })
    
    # Generate summary report
    generate_summary_report(results, reports_dir, timestamp)
    
    return results

def generate_summary_report(results, reports_dir, timestamp):
    """Generate a summary HTML report"""
    
    summary_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>One-Time Book Purchase Test Summary Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
            .summary {{ margin: 20px 0; }}
            .result {{ margin: 10px 0; padding: 10px; border-radius: 5px; }}
            .passed {{ background-color: #d4edda; border: 1px solid #c3e6cb; }}
            .failed {{ background-color: #f8d7da; border: 1px solid #f5c6cb; }}
            .error {{ background-color: #fff3cd; border: 1px solid #ffeaa7; }}
            .report-link {{ color: #007bff; text-decoration: none; }}
            .report-link:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>One-Time Book Purchase Test Summary Report</h1>
            <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p><strong>Test Run ID:</strong> {timestamp}</p>
        </div>
        
        <div class="summary">
            <h2>Test Results Summary</h2>
            <p><strong>Total Tests:</strong> {len(results)}</p>
            <p><strong>Passed:</strong> {len([r for r in results if r['status'] == 'PASSED'])}</p>
            <p><strong>Failed:</strong> {len([r for r in results if r['status'] == 'FAILED'])}</p>
            <p><strong>Errors:</strong> {len([r for r in results if r['status'] == 'ERROR'])}</p>
        </div>
        
        <div class="results">
            <h2>Detailed Results</h2>
    """
    
    for result in results:
        status_class = result['status'].lower()
        summary_html += f"""
            <div class="result {status_class}">
                <h3>{result['device']} - {result['status']}</h3>
                <p><strong>Description:</strong> {result['description']}</p>
                <p><strong>Exit Code:</strong> {result['exit_code']}</p>
        """
        
        if result['report_file'] != 'N/A':
            summary_html += f"""
                <p><strong>Detailed Report:</strong> 
                    <a href="{os.path.basename(result['report_file'])}" class="report-link">
                        View Full Report
                    </a>
                </p>
            """
        
        summary_html += "</div>"
    
    summary_html += """
        </div>
    </body>
    </html>
    """
    
    summary_file = f"{reports_dir}/summary_report_{timestamp}.html"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_html)
    
    print(f"\n📋 Summary report saved to: {summary_file}")

def main():
    """Main function to run the tests"""
    
    print("🚀 Starting One-Time Book Purchase Tests with HTML Reports...")
    print("📱 Testing on: Desktop and iPad Pro")
    print("📊 HTML reports will be generated for each test run")
    
    try:
        results = run_one_time_book_purchase_tests()
        
        # Print final summary
        print("\n" + "="*80)
        print("FINAL SUMMARY")
        print("="*80)
        
        for result in results:
            status_emoji = "✅" if result['status'] == 'PASSED' else "❌" if result['status'] == 'FAILED' else "⚠️"
            print(f"{status_emoji} {result['device']}: {result['status']}")
        
        # Check if all tests passed
        all_passed = all(result['status'] == 'PASSED' for result in results)
        
        if all_passed:
            print("\n🎉 All tests passed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed. Check the HTML reports for details.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ Test execution interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Git Log Capture System
Captures and stores all Git/GitHub Actions test logs in the test_results database.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from db.db_helper import MySQLHelper


class GitLogCapture:
    def __init__(self):
        self.db_helper = MySQLHelper()
        self.github_actions_log_dir = ".github/workflows"
        self.test_logs_dir = "test_reports"
        
    def capture_github_actions_logs(self):
        """Capture logs from GitHub Actions workflows"""
        print("🔍 Capturing GitHub Actions logs...")
        
        # Check if we're running in GitHub Actions
        if os.getenv('GITHUB_ACTIONS'):
            self._capture_current_workflow_logs()
        else:
            self._capture_local_workflow_logs()
    
    def _capture_current_workflow_logs(self):
        """Capture logs from current GitHub Actions run"""
        try:
            # Get workflow information
            workflow_name = os.getenv('GITHUB_WORKFLOW', 'Unknown Workflow')
            run_id = os.getenv('GITHUB_RUN_ID', 'Unknown')
            job_name = os.getenv('GITHUB_JOB', 'Unknown Job')
            
            print(f"📋 Workflow: {workflow_name}")
            print(f"🆔 Run ID: {run_id}")
            print(f"💼 Job: {job_name}")
            
            # Capture test execution logs
            self._capture_test_execution_logs(workflow_name, run_id, job_name)
            
            # Capture pytest output if available
            self._capture_pytest_logs(workflow_name, run_id, job_name)
            
        except Exception as e:
            print(f"❌ Error capturing current workflow logs: {e}")
    
    def _capture_local_workflow_logs(self):
        """Capture logs from local workflow files"""
        try:
            workflow_files = list(Path(self.github_actions_log_dir).glob("*.yml"))
            
            for workflow_file in workflow_files:
                workflow_name = workflow_file.stem
                print(f"📋 Processing workflow: {workflow_name}")
                
                # Parse workflow file for test information
                self._parse_workflow_file(workflow_file, workflow_name)
                
        except Exception as e:
            print(f"❌ Error capturing local workflow logs: {e}")
    
    def _capture_test_execution_logs(self, workflow_name, run_id, job_name):
        """Capture test execution logs from current run"""
        try:
            # Look for test output files
            test_files = [
                "test_reports/report.html",
                "test_reports/junit.xml",
                "test_reports/coverage.xml"
            ]
            
            for test_file in test_files:
                if os.path.exists(test_file):
                    self._parse_test_file(test_file, workflow_name, run_id, job_name)
            
            # Capture pytest output from environment
            pytest_output = os.getenv('PYTEST_OUTPUT', '')
            if pytest_output:
                self._store_test_log(
                    "pytest_execution",
                    workflow_name,
                    "PASSED" if "passed" in pytest_output.lower() else "FAILED",
                    pytest_output,
                    device_name="github_actions",
                    screen_resolution="ci_environment"
                )
                
        except Exception as e:
            print(f"❌ Error capturing test execution logs: {e}")
    
    def _capture_pytest_logs(self, workflow_name, run_id, job_name):
        """Capture pytest specific logs"""
        try:
            # Look for pytest log files
            pytest_logs = [
                "pytest.log",
                "test.log",
                ".pytest_cache/v/cache/lastfailed"
            ]
            
            for log_file in pytest_logs:
                if os.path.exists(log_file):
                    with open(log_file, 'r', encoding='utf-8') as f:
                        log_content = f.read()
                        
                    # Determine test status from log content
                    test_status = self._determine_test_status_from_log(log_content)
                    
                    self._store_test_log(
                        f"pytest_{Path(log_file).stem}",
                        workflow_name,
                        test_status,
                        log_content,
                        device_name="github_actions",
                        screen_resolution="ci_environment"
                    )
                    
        except Exception as e:
            print(f"❌ Error capturing pytest logs: {e}")
    
    def _parse_workflow_file(self, workflow_file, workflow_name):
        """Parse workflow YAML file for test information"""
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract test steps from workflow
            test_steps = self._extract_test_steps(content)
            
            for step in test_steps:
                self._store_test_log(
                    f"workflow_step_{step['name']}",
                    workflow_name,
                    "PASSED",  # Assume passed for workflow parsing
                    f"Workflow step: {step['name']}\n{step.get('command', '')}",
                    device_name="github_actions",
                    screen_resolution="ci_environment"
                )
                
        except Exception as e:
            print(f"❌ Error parsing workflow file {workflow_file}: {e}")
    
    def _extract_test_steps(self, workflow_content):
        """Extract test steps from workflow content"""
        steps = []
        
        # Look for pytest commands
        pytest_pattern = r'pytest.*?\.py'
        pytest_matches = re.findall(pytest_pattern, workflow_content)
        
        for match in pytest_matches:
            steps.append({
                'name': f'pytest_{len(steps)}',
                'command': match.strip()
            })
        
        # Look for test execution commands
        test_pattern = r'python.*?test.*?\.py'
        test_matches = re.findall(test_pattern, workflow_content)
        
        for match in test_matches:
            steps.append({
                'name': f'test_execution_{len(steps)}',
                'command': match.strip()
            })
        
        return steps
    
    def _parse_test_file(self, test_file, workflow_name, run_id, job_name):
        """Parse test result files"""
        try:
            file_ext = Path(test_file).suffix
            
            if file_ext == '.html':
                self._parse_html_test_file(test_file, workflow_name, run_id, job_name)
            elif file_ext == '.xml':
                self._parse_xml_test_file(test_file, workflow_name, run_id, job_name)
            else:
                self._parse_text_test_file(test_file, workflow_name, run_id, job_name)
                
        except Exception as e:
            print(f"❌ Error parsing test file {test_file}: {e}")
    
    def _parse_html_test_file(self, test_file, workflow_name, run_id, job_name):
        """Parse HTML test report"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract test results from HTML
            passed_tests = len(re.findall(r'passed', content, re.IGNORECASE))
            failed_tests = len(re.findall(r'failed', content, re.IGNORECASE))
            error_tests = len(re.findall(r'error', content, re.IGNORECASE))
            
            total_tests = passed_tests + failed_tests + error_tests
            
            if total_tests > 0:
                test_status = "PASSED" if failed_tests == 0 and error_tests == 0 else "FAILED"
                
                self._store_test_log(
                    f"html_report_{Path(test_file).stem}",
                    workflow_name,
                    test_status,
                    f"HTML Test Report:\nPassed: {passed_tests}\nFailed: {failed_tests}\nErrors: {error_tests}\nTotal: {total_tests}",
                    device_name="github_actions",
                    screen_resolution="ci_environment"
                )
                
        except Exception as e:
            print(f"❌ Error parsing HTML test file: {e}")
    
    def _parse_xml_test_file(self, test_file, workflow_name, run_id, job_name):
        """Parse XML test report (JUnit format)"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract test results from XML
            testsuites = re.findall(r'<testsuite[^>]*>', content)
            testcases = re.findall(r'<testcase[^>]*>', content)
            failures = re.findall(r'<failure[^>]*>', content)
            errors = re.findall(r'<error[^>]*>', content)
            
            total_tests = len(testcases)
            failed_tests = len(failures)
            error_tests = len(errors)
            
            if total_tests > 0:
                test_status = "PASSED" if failed_tests == 0 and error_tests == 0 else "FAILED"
                
                self._store_test_log(
                    f"xml_report_{Path(test_file).stem}",
                    workflow_name,
                    test_status,
                    f"XML Test Report:\nTest Suites: {len(testsuites)}\nTest Cases: {total_tests}\nFailures: {failed_tests}\nErrors: {error_tests}",
                    device_name="github_actions",
                    screen_resolution="ci_environment"
                )
                
        except Exception as e:
            print(f"❌ Error parsing XML test file: {e}")
    
    def _parse_text_test_file(self, test_file, workflow_name, run_id, job_name):
        """Parse text test file"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_status = self._determine_test_status_from_log(content)
            
            self._store_test_log(
                f"text_report_{Path(test_file).stem}",
                workflow_name,
                test_status,
                content[:1000] + "..." if len(content) > 1000 else content,
                device_name="github_actions",
                screen_resolution="ci_environment"
            )
            
        except Exception as e:
            print(f"❌ Error parsing text test file: {e}")
    
    def _determine_test_status_from_log(self, log_content):
        """Determine test status from log content"""
        log_lower = log_content.lower()
        
        if any(word in log_lower for word in ['passed', 'success', 'ok']):
            return "PASSED"
        elif any(word in log_lower for word in ['failed', 'failure', 'error']):
            return "FAILED"
        elif any(word in log_lower for word in ['skipped', 'skip']):
            return "SKIPPED"
        else:
            return "ERROR"
    
    def _store_test_log(self, test_case_name, module_name, test_status, error_message=None, 
                       total_time_duration=None, device_name=None, screen_resolution=None, error_link=None):
        """Store test log in database"""
        try:
            self.db_helper.store_test_result_in_tables(
                test_case_name=test_case_name,
                module_name=module_name,
                test_status=test_status,
                error_message=error_message,
                total_time_duration=total_time_duration,
                device_name=device_name or "github_actions",
                screen_resolution=screen_resolution or "ci_environment",
                error_link=error_link
            )
            print(f"✅ Stored test log: {test_case_name} - {test_status}")
            
        except Exception as e:
            print(f"❌ Error storing test log: {e}")
    
    def capture_git_commit_logs(self):
        """Capture logs from Git commits"""
        print("🔍 Capturing Git commit logs...")
        
        try:
            # Get recent commits
            commits = self._get_recent_commits()
            
            for commit in commits:
                self._store_git_commit_log(commit)
                
        except Exception as e:
            print(f"❌ Error capturing Git commit logs: {e}")
    
    def _get_recent_commits(self, limit=10):
        """Get recent Git commits"""
        try:
            result = subprocess.run(
                ['git', 'log', f'--max-count={limit}', '--pretty=format:%H|%an|%ae|%ad|%s'],
                capture_output=True, text=True, check=True
            )
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 5:
                        commits.append({
                            'hash': parts[0],
                            'author': parts[1],
                            'email': parts[2],
                            'date': parts[3],
                            'message': parts[4]
                        })
            
            return commits
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting Git commits: {e}")
            return []
    
    def _store_git_commit_log(self, commit):
        """Store Git commit log in database"""
        try:
            commit_message = f"Git Commit: {commit['message']}\nAuthor: {commit['author']}\nDate: {commit['date']}"
            
            self._store_test_log(
                f"git_commit_{commit['hash'][:8]}",
                "git_operations",
                "PASSED",  # Git commits are considered successful
                commit_message,
                device_name="git_system",
                screen_resolution="version_control"
            )
            
        except Exception as e:
            print(f"❌ Error storing Git commit log: {e}")
    
    def capture_all_logs(self):
        """Capture all available logs"""
        print("🚀 Starting comprehensive log capture...")
        
        # Capture GitHub Actions logs
        self.capture_github_actions_logs()
        
        # Capture Git commit logs
        self.capture_git_commit_logs()
        
        # Capture any additional log files
        self._capture_additional_logs()
        
        print("✅ Log capture completed!")
    
    def _capture_additional_logs(self):
        """Capture additional log files"""
        try:
            # Look for common log files
            log_patterns = [
                "*.log",
                "test_*.log",
                "pytest_*.log",
                "coverage_*.log"
            ]
            
            for pattern in log_patterns:
                log_files = list(Path(".").glob(pattern))
                
                for log_file in log_files:
                    if log_file.is_file():
                        self._parse_log_file(log_file)
                        
        except Exception as e:
            print(f"❌ Error capturing additional logs: {e}")
    
    def _parse_log_file(self, log_file):
        """Parse individual log file"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_status = self._determine_test_status_from_log(content)
            
            self._store_test_log(
                f"log_file_{log_file.stem}",
                "log_parsing",
                test_status,
                content[:1000] + "..." if len(content) > 1000 else content,
                device_name="file_system",
                screen_resolution="local_environment"
            )
            
        except Exception as e:
            print(f"❌ Error parsing log file {log_file}: {e}")
    
    def close(self):
        """Close database connection"""
        self.db_helper.close()


def main():
    """Main function to capture all logs"""
    try:
        print("🔧 Git Log Capture System")
        print("=" * 50)
        
        # Initialize log capture system
        log_capture = GitLogCapture()
        
        # Capture all logs
        log_capture.capture_all_logs()
        
        # Close connections
        log_capture.close()
        
        print("\n🎉 All logs captured and stored in database!")
        print("📊 Check the test_results table for captured logs.")
        
    except Exception as e:
        print(f"❌ Log capture failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
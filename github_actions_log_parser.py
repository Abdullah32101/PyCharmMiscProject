#!/usr/bin/env python3
"""
GitHub Actions Log Parser
Parses GitHub Actions workflow logs and stores test results in database.
"""

import json
import os
import re
import requests
from datetime import datetime
from pathlib import Path

from db.db_helper import MySQLHelper


class GitHubActionsLogParser:
    def __init__(self, github_token=None):
        self.db_helper = MySQLHelper()
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.repo_owner = os.getenv('GITHUB_REPOSITORY_OWNER', 'Abdullah32101')
        self.repo_name = os.getenv('GITHUB_REPOSITORY', 'PyCharmMiscProject').split('/')[-1]
        
    def parse_current_workflow_logs(self):
        """Parse logs from current GitHub Actions workflow run"""
        print("🔍 Parsing current GitHub Actions workflow logs...")
        
        if not os.getenv('GITHUB_ACTIONS'):
            print("⚠️ Not running in GitHub Actions environment")
            return
        
        try:
            # Get current workflow information
            workflow_name = os.getenv('GITHUB_WORKFLOW', 'Unknown')
            run_id = os.getenv('GITHUB_RUN_ID', 'Unknown')
            job_name = os.getenv('GITHUB_JOB', 'Unknown')
            event_name = os.getenv('GITHUB_EVENT_NAME', 'Unknown')
            
            print(f"📋 Workflow: {workflow_name}")
            print(f"🆔 Run ID: {run_id}")
            print(f"💼 Job: {job_name}")
            print(f"📅 Event: {event_name}")
            
            # Parse workflow logs
            self._parse_workflow_logs(workflow_name, run_id, job_name, event_name)
            
            # Parse test artifacts
            self._parse_test_artifacts(workflow_name, run_id)
            
        except Exception as e:
            print(f"❌ Error parsing current workflow logs: {e}")
    
    def _parse_workflow_logs(self, workflow_name, run_id, job_name, event_name):
        """Parse workflow execution logs"""
        try:
            # Look for test output in environment
            test_output = os.getenv('TEST_OUTPUT', '')
            pytest_output = os.getenv('PYTEST_OUTPUT', '')
            
            # Combine all test outputs
            combined_output = f"{test_output}\n{pytest_output}".strip()
            
            if combined_output:
                test_status = self._determine_test_status(combined_output)
                
                self._store_workflow_result(
                    f"workflow_{workflow_name}_{run_id}",
                    workflow_name,
                    test_status,
                    f"Workflow: {workflow_name}\nRun ID: {run_id}\nJob: {job_name}\nEvent: {event_name}\n\nOutput:\n{combined_output}",
                    device_name="github_actions",
                    screen_resolution="ci_environment"
                )
            
            # Parse step outputs
            self._parse_step_outputs(workflow_name, run_id)
            
        except Exception as e:
            print(f"❌ Error parsing workflow logs: {e}")
    
    def _parse_step_outputs(self, workflow_name, run_id):
        """Parse individual step outputs"""
        try:
            # Look for step output files
            step_files = [
                "step_output.txt",
                "test_results.txt",
                "pytest_results.txt"
            ]
            
            for step_file in step_files:
                if os.path.exists(step_file):
                    with open(step_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    test_status = self._determine_test_status(content)
                    
                    self._store_workflow_result(
                        f"step_{Path(step_file).stem}_{run_id}",
                        workflow_name,
                        test_status,
                        content,
                        device_name="github_actions",
                        screen_resolution="ci_environment"
                    )
                    
        except Exception as e:
            print(f"❌ Error parsing step outputs: {e}")
    
    def _parse_test_artifacts(self, workflow_name, run_id):
        """Parse test artifacts and reports"""
        try:
            # Look for test report files
            test_dirs = ["test_reports", "reports", "coverage"]
            
            for test_dir in test_dirs:
                if os.path.exists(test_dir):
                    self._parse_test_directory(test_dir, workflow_name, run_id)
            
            # Look for specific test files
            test_files = [
                "pytest.xml",
                "junit.xml",
                "coverage.xml",
                "test-results.xml"
            ]
            
            for test_file in test_files:
                if os.path.exists(test_file):
                    self._parse_test_file(test_file, workflow_name, run_id)
                    
        except Exception as e:
            print(f"❌ Error parsing test artifacts: {e}")
    
    def _parse_test_directory(self, test_dir, workflow_name, run_id):
        """Parse test directory for reports"""
        try:
            for file_path in Path(test_dir).rglob("*"):
                if file_path.is_file():
                    if file_path.suffix in ['.html', '.xml', '.json']:
                        self._parse_test_file(str(file_path), workflow_name, run_id)
                        
        except Exception as e:
            print(f"❌ Error parsing test directory {test_dir}: {e}")
    
    def _parse_test_file(self, test_file, workflow_name, run_id):
        """Parse individual test file"""
        try:
            file_ext = Path(test_file).suffix.lower()
            
            if file_ext == '.html':
                self._parse_html_test_file(test_file, workflow_name, run_id)
            elif file_ext == '.xml':
                self._parse_xml_test_file(test_file, workflow_name, run_id)
            elif file_ext == '.json':
                self._parse_json_test_file(test_file, workflow_name, run_id)
            else:
                self._parse_text_test_file(test_file, workflow_name, run_id)
                
        except Exception as e:
            print(f"❌ Error parsing test file {test_file}: {e}")
    
    def _parse_html_test_file(self, test_file, workflow_name, run_id):
        """Parse HTML test report"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract test statistics from HTML
            stats = self._extract_html_test_stats(content)
            
            test_status = "PASSED" if stats['failed'] == 0 and stats['errors'] == 0 else "FAILED"
            
            self._store_workflow_result(
                f"html_report_{Path(test_file).stem}_{run_id}",
                workflow_name,
                test_status,
                f"HTML Test Report:\nPassed: {stats['passed']}\nFailed: {stats['failed']}\nErrors: {stats['errors']}\nTotal: {stats['total']}",
                device_name="github_actions",
                screen_resolution="ci_environment"
            )
            
        except Exception as e:
            print(f"❌ Error parsing HTML test file: {e}")
    
    def _extract_html_test_stats(self, html_content):
        """Extract test statistics from HTML content"""
        stats = {
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'total': 0
        }
        
        try:
            # Look for test result patterns
            passed_patterns = [
                r'(\d+)\s+passed',
                r'passed[^>]*>(\d+)',
                r'success[^>]*>(\d+)'
            ]
            
            failed_patterns = [
                r'(\d+)\s+failed',
                r'failed[^>]*>(\d+)',
                r'failure[^>]*>(\d+)'
            ]
            
            error_patterns = [
                r'(\d+)\s+error',
                r'error[^>]*>(\d+)'
            ]
            
            # Extract counts
            for pattern in passed_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    stats['passed'] = max(stats['passed'], int(matches[0]))
            
            for pattern in failed_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    stats['failed'] = max(stats['failed'], int(matches[0]))
            
            for pattern in error_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                if matches:
                    stats['errors'] = max(stats['errors'], int(matches[0]))
            
            stats['total'] = stats['passed'] + stats['failed'] + stats['errors']
            
        except Exception as e:
            print(f"⚠️ Error extracting HTML stats: {e}")
        
        return stats
    
    def _parse_xml_test_file(self, test_file, workflow_name, run_id):
        """Parse XML test report (JUnit format)"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract test statistics from XML
            stats = self._extract_xml_test_stats(content)
            
            test_status = "PASSED" if stats['failures'] == 0 and stats['errors'] == 0 else "FAILED"
            
            self._store_workflow_result(
                f"xml_report_{Path(test_file).stem}_{run_id}",
                workflow_name,
                test_status,
                f"XML Test Report:\nTests: {stats['tests']}\nFailures: {stats['failures']}\nErrors: {stats['errors']}\nSkipped: {stats['skipped']}",
                device_name="github_actions",
                screen_resolution="ci_environment"
            )
            
        except Exception as e:
            print(f"❌ Error parsing XML test file: {e}")
    
    def _extract_xml_test_stats(self, xml_content):
        """Extract test statistics from XML content"""
        stats = {
            'tests': 0,
            'failures': 0,
            'errors': 0,
            'skipped': 0
        }
        
        try:
            # Look for testsuite attributes
            testsuite_pattern = r'<testsuite[^>]*tests="(\d+)"[^>]*failures="(\d+)"[^>]*errors="(\d+)"[^>]*skipped="(\d+)"'
            matches = re.findall(testsuite_pattern, xml_content)
            
            if matches:
                for match in matches:
                    stats['tests'] += int(match[0])
                    stats['failures'] += int(match[1])
                    stats['errors'] += int(match[2])
                    stats['skipped'] += int(match[3])
            
            # Fallback: count individual elements
            if stats['tests'] == 0:
                stats['tests'] = len(re.findall(r'<testcase[^>]*>', xml_content))
                stats['failures'] = len(re.findall(r'<failure[^>]*>', xml_content))
                stats['errors'] = len(re.findall(r'<error[^>]*>', xml_content))
                stats['skipped'] = len(re.findall(r'<skipped[^>]*>', xml_content))
                
        except Exception as e:
            print(f"⚠️ Error extracting XML stats: {e}")
        
        return stats
    
    def _parse_json_test_file(self, test_file, workflow_name, run_id):
        """Parse JSON test report"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract test information from JSON
            test_info = self._extract_json_test_info(data)
            
            test_status = "PASSED" if test_info['failed'] == 0 and test_info['errors'] == 0 else "FAILED"
            
            self._store_workflow_result(
                f"json_report_{Path(test_file).stem}_{run_id}",
                workflow_name,
                test_status,
                f"JSON Test Report:\n{json.dumps(test_info, indent=2)}",
                device_name="github_actions",
                screen_resolution="ci_environment"
            )
            
        except Exception as e:
            print(f"❌ Error parsing JSON test file: {e}")
    
    def _extract_json_test_info(self, data):
        """Extract test information from JSON data"""
        info = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0
        }
        
        try:
            if isinstance(data, dict):
                # Handle different JSON formats
                if 'summary' in data:
                    summary = data['summary']
                    info['total'] = summary.get('total', 0)
                    info['passed'] = summary.get('passed', 0)
                    info['failed'] = summary.get('failed', 0)
                    info['errors'] = summary.get('errors', 0)
                    info['skipped'] = summary.get('skipped', 0)
                elif 'tests' in data:
                    tests = data['tests']
                    info['total'] = len(tests)
                    for test in tests:
                        status = test.get('status', '').lower()
                        if status == 'passed':
                            info['passed'] += 1
                        elif status == 'failed':
                            info['failed'] += 1
                        elif status == 'error':
                            info['errors'] += 1
                        elif status == 'skipped':
                            info['skipped'] += 1
                            
        except Exception as e:
            print(f"⚠️ Error extracting JSON test info: {e}")
        
        return info
    
    def _parse_text_test_file(self, test_file, workflow_name, run_id):
        """Parse text test file"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_status = self._determine_test_status(content)
            
            self._store_workflow_result(
                f"text_report_{Path(test_file).stem}_{run_id}",
                workflow_name,
                test_status,
                content[:1000] + "..." if len(content) > 1000 else content,
                device_name="github_actions",
                screen_resolution="ci_environment"
            )
            
        except Exception as e:
            print(f"❌ Error parsing text test file: {e}")
    
    def _determine_test_status(self, content):
        """Determine test status from content"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['passed', 'success', 'ok', 'green']):
            return "PASSED"
        elif any(word in content_lower for word in ['failed', 'failure', 'error', 'red']):
            return "FAILED"
        elif any(word in content_lower for word in ['skipped', 'skip']):
            return "SKIPPED"
        else:
            return "ERROR"
    
    def _store_workflow_result(self, test_case_name, module_name, test_status, error_message=None,
                              total_time_duration=None, device_name=None, screen_resolution=None, error_link=None):
        """Store workflow result in database"""
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
            print(f"✅ Stored workflow result: {test_case_name} - {test_status}")
            
        except Exception as e:
            print(f"❌ Error storing workflow result: {e}")
    
    def fetch_workflow_runs(self, workflow_name=None, limit=10):
        """Fetch recent workflow runs from GitHub API"""
        if not self.github_token:
            print("⚠️ GitHub token not available for API access")
            return []
        
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/runs"
            if workflow_name:
                url += f"?workflow={workflow_name}"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            runs = response.json().get('workflow_runs', [])
            return runs[:limit]
            
        except Exception as e:
            print(f"❌ Error fetching workflow runs: {e}")
            return []
    
    def parse_workflow_run(self, run_id):
        """Parse specific workflow run"""
        try:
            print(f"🔍 Parsing workflow run: {run_id}")
            
            # Fetch run details
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/runs/{run_id}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            run_data = response.json()
            
            # Store run information
            self._store_workflow_result(
                f"workflow_run_{run_id}",
                run_data.get('name', 'Unknown Workflow'),
                "PASSED" if run_data.get('conclusion') == 'success' else "FAILED",
                f"Workflow Run Details:\nStatus: {run_data.get('status')}\nConclusion: {run_data.get('conclusion')}\nCreated: {run_data.get('created_at')}",
                device_name="github_actions",
                screen_resolution="ci_environment"
            )
            
        except Exception as e:
            print(f"❌ Error parsing workflow run {run_id}: {e}")
    
    def close(self):
        """Close database connection"""
        self.db_helper.close()


def main():
    """Main function to parse GitHub Actions logs"""
    try:
        print("🔧 GitHub Actions Log Parser")
        print("=" * 50)
        
        # Initialize parser
        parser = GitHubActionsLogParser()
        
        # Parse current workflow logs
        parser.parse_current_workflow_logs()
        
        # Close connections
        parser.close()
        
        print("\n🎉 GitHub Actions logs parsed and stored in database!")
        print("📊 Check the test_results table for parsed logs.")
        
    except Exception as e:
        print(f"❌ Log parsing failed: {e}")


if __name__ == "__main__":
    main() 
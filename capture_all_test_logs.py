#!/usr/bin/env python3
"""
Comprehensive Test Log Capture System
Captures and stores all test logs from Git, GitHub Actions, and local test runs.
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

from db.db_helper import MySQLHelper
from github_actions_log_parser import GitHubActionsLogParser


class ComprehensiveLogCapture:
    def __init__(self):
        self.db_helper = MySQLHelper()
        self.parser = GitHubActionsLogParser()
        
    def capture_all_logs(self):
        """Capture all available test logs"""
        print("🚀 Starting comprehensive test log capture...")
        print("=" * 60)
        
        # Capture GitHub Actions logs
        print("\n📋 1. Capturing GitHub Actions logs...")
        self.capture_github_actions_logs()
        
        # Capture Git commit logs
        print("\n📋 2. Capturing Git commit logs...")
        self.capture_git_commit_logs()
        
        # Capture local test logs
        print("\n📋 3. Capturing local test logs...")
        self.capture_local_test_logs()
        
        # Capture workflow artifacts
        print("\n📋 4. Capturing workflow artifacts...")
        self.capture_workflow_artifacts()
        
        # Capture environment information
        print("\n📋 5. Capturing environment information...")
        self.capture_environment_info()
        
        print("\n✅ Comprehensive log capture completed!")
        self._show_summary()
    
    def capture_github_actions_logs(self):
        """Capture logs from GitHub Actions"""
        try:
            # Parse current workflow logs
            self.parser.parse_current_workflow_logs()
            
            # Store workflow metadata
            self._store_workflow_metadata()
            
        except Exception as e:
            print(f"❌ Error capturing GitHub Actions logs: {e}")
    
    def _store_workflow_metadata(self):
        """Store workflow metadata in database"""
        try:
            workflow_info = {
                'workflow_name': os.getenv('GITHUB_WORKFLOW', 'Unknown'),
                'run_id': os.getenv('GITHUB_RUN_ID', 'Unknown'),
                'job_name': os.getenv('GITHUB_JOB', 'Unknown'),
                'event_name': os.getenv('GITHUB_EVENT_NAME', 'Unknown'),
                'repository': os.getenv('GITHUB_REPOSITORY', 'Unknown'),
                'ref': os.getenv('GITHUB_REF', 'Unknown'),
                'sha': os.getenv('GITHUB_SHA', 'Unknown'),
                'actor': os.getenv('GITHUB_ACTOR', 'Unknown')
            }
            
            metadata_text = "\n".join([f"{k}: {v}" for k, v in workflow_info.items()])
            
            self.db_helper.store_test_result_in_tables(
                test_case_name=f"workflow_metadata_{workflow_info['run_id']}",
                module_name="github_actions_metadata",
                test_status="PASSED",
                error_message=metadata_text,
                device_name="github_actions",
                screen_resolution="ci_environment"
            )
            
        except Exception as e:
            print(f"❌ Error storing workflow metadata: {e}")
    
    def capture_git_commit_logs(self):
        """Capture logs from Git commits"""
        try:
            # Get recent commits
            commits = self._get_recent_commits(limit=20)
            
            for commit in commits:
                self._store_git_commit_log(commit)
                
        except Exception as e:
            print(f"❌ Error capturing Git commit logs: {e}")
    
    def _get_recent_commits(self, limit=20):
        """Get recent Git commits"""
        try:
            result = subprocess.run(
                ['git', 'log', f'--max-count={limit}', '--pretty=format:%H|%an|%ae|%ad|%s|%b'],
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
                            'message': parts[4],
                            'body': parts[5] if len(parts) > 5 else ''
                        })
            
            return commits
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error getting Git commits: {e}")
            return []
    
    def _store_git_commit_log(self, commit):
        """Store Git commit log in database"""
        try:
            commit_message = f"""Git Commit Information:
Hash: {commit['hash']}
Author: {commit['author']} ({commit['email']})
Date: {commit['date']}
Message: {commit['message']}
Body: {commit['body']}"""
            
            self.db_helper.store_test_result_in_tables(
                test_case_name=f"git_commit_{commit['hash'][:8]}",
                module_name="git_operations",
                test_status="PASSED",
                error_message=commit_message,
                device_name="git_system",
                screen_resolution="version_control"
            )
            
        except Exception as e:
            print(f"❌ Error storing Git commit log: {e}")
    
    def capture_local_test_logs(self):
        """Capture logs from local test runs"""
        try:
            # Look for test log files
            log_patterns = [
                "*.log",
                "test_*.log",
                "pytest_*.log",
                "coverage_*.log",
                "test_reports/*.log"
            ]
            
            for pattern in log_patterns:
                log_files = list(Path(".").glob(pattern))
                
                for log_file in log_files:
                    if log_file.is_file():
                        self._parse_local_log_file(log_file)
            
            # Look for test output files
            test_output_files = [
                "test_output.txt",
                "pytest_output.txt",
                "test_results.txt"
            ]
            
            for output_file in test_output_files:
                if os.path.exists(output_file):
                    self._parse_test_output_file(output_file)
                    
        except Exception as e:
            print(f"❌ Error capturing local test logs: {e}")
    
    def _parse_local_log_file(self, log_file):
        """Parse local log file"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_status = self._determine_test_status(content)
            
            self.db_helper.store_test_result_in_tables(
                test_case_name=f"local_log_{log_file.stem}",
                module_name="local_testing",
                test_status=test_status,
                error_message=content[:2000] + "..." if len(content) > 2000 else content,
                device_name="local_environment",
                screen_resolution="local_system"
            )
            
        except Exception as e:
            print(f"❌ Error parsing local log file {log_file}: {e}")
    
    def _parse_test_output_file(self, output_file):
        """Parse test output file"""
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_status = self._determine_test_status(content)
            
            self.db_helper.store_test_result_in_tables(
                test_case_name=f"test_output_{Path(output_file).stem}",
                module_name="test_execution",
                test_status=test_status,
                error_message=content[:2000] + "..." if len(content) > 2000 else content,
                device_name="local_environment",
                screen_resolution="local_system"
            )
            
        except Exception as e:
            print(f"❌ Error parsing test output file {output_file}: {e}")
    
    def capture_workflow_artifacts(self):
        """Capture workflow artifacts"""
        try:
            # Look for test report directories
            artifact_dirs = [
                "test_reports",
                "reports",
                "coverage",
                "screenshots",
                "artifacts"
            ]
            
            for artifact_dir in artifact_dirs:
                if os.path.exists(artifact_dir):
                    self._parse_artifact_directory(artifact_dir)
            
            # Look for specific artifact files
            artifact_files = [
                "pytest.xml",
                "junit.xml",
                "coverage.xml",
                "test-results.xml",
                "report.html"
            ]
            
            for artifact_file in artifact_files:
                if os.path.exists(artifact_file):
                    self._parse_artifact_file(artifact_file)
                    
        except Exception as e:
            print(f"❌ Error capturing workflow artifacts: {e}")
    
    def _parse_artifact_directory(self, artifact_dir):
        """Parse artifact directory"""
        try:
            for file_path in Path(artifact_dir).rglob("*"):
                if file_path.is_file():
                    if file_path.suffix in ['.html', '.xml', '.json', '.log']:
                        self._parse_artifact_file(str(file_path))
                        
        except Exception as e:
            print(f"❌ Error parsing artifact directory {artifact_dir}: {e}")
    
    def _parse_artifact_file(self, artifact_file):
        """Parse artifact file"""
        try:
            file_ext = Path(artifact_file).suffix.lower()
            
            if file_ext == '.html':
                self._parse_html_artifact(artifact_file)
            elif file_ext == '.xml':
                self._parse_xml_artifact(artifact_file)
            elif file_ext == '.json':
                self._parse_json_artifact(artifact_file)
            else:
                self._parse_text_artifact(artifact_file)
                
        except Exception as e:
            print(f"❌ Error parsing artifact file {artifact_file}: {e}")
    
    def _parse_html_artifact(self, artifact_file):
        """Parse HTML artifact"""
        try:
            with open(artifact_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract basic information
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            title = title_match.group(1) if title_match else "Unknown HTML Report"
            
            test_status = self._determine_test_status(content)
            
            self.db_helper.store_test_result_in_tables(
                test_case_name=f"html_artifact_{Path(artifact_file).stem}",
                module_name="html_reports",
                test_status=test_status,
                error_message=f"HTML Report: {title}\nFile: {artifact_file}\nContent length: {len(content)} characters",
                device_name="artifact_processing",
                screen_resolution="report_generation"
            )
            
        except Exception as e:
            print(f"❌ Error parsing HTML artifact: {e}")
    
    def _parse_xml_artifact(self, artifact_file):
        """Parse XML artifact"""
        try:
            with open(artifact_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract basic information
            root_match = re.search(r'<(\w+)', content)
            root_element = root_match.group(1) if root_match else "unknown"
            
            test_status = self._determine_test_status(content)
            
            self.db_helper.store_test_result_in_tables(
                test_case_name=f"xml_artifact_{Path(artifact_file).stem}",
                module_name="xml_reports",
                test_status=test_status,
                error_message=f"XML Report: {root_element}\nFile: {artifact_file}\nContent length: {len(content)} characters",
                device_name="artifact_processing",
                screen_resolution="report_generation"
            )
            
        except Exception as e:
            print(f"❌ Error parsing XML artifact: {e}")
    
    def _parse_json_artifact(self, artifact_file):
        """Parse JSON artifact"""
        try:
            with open(artifact_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to parse JSON
            import json
            data = json.loads(content)
            
            test_status = "PASSED"  # Assume JSON artifacts are successful
            
            self.db_helper.store_test_result_in_tables(
                test_case_name=f"json_artifact_{Path(artifact_file).stem}",
                module_name="json_reports",
                test_status=test_status,
                error_message=f"JSON Report: {type(data).__name__}\nFile: {artifact_file}\nKeys: {list(data.keys()) if isinstance(data, dict) else 'N/A'}",
                device_name="artifact_processing",
                screen_resolution="report_generation"
            )
            
        except Exception as e:
            print(f"❌ Error parsing JSON artifact: {e}")
    
    def _parse_text_artifact(self, artifact_file):
        """Parse text artifact"""
        try:
            with open(artifact_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_status = self._determine_test_status(content)
            
            self.db_helper.store_test_result_in_tables(
                test_case_name=f"text_artifact_{Path(artifact_file).stem}",
                module_name="text_reports",
                test_status=test_status,
                error_message=f"Text Report: {artifact_file}\nContent length: {len(content)} characters\nPreview: {content[:500]}...",
                device_name="artifact_processing",
                screen_resolution="report_generation"
            )
            
        except Exception as e:
            print(f"❌ Error parsing text artifact: {e}")
    
    def capture_environment_info(self):
        """Capture environment information"""
        try:
            env_info = {
                'python_version': sys.version,
                'platform': sys.platform,
                'working_directory': os.getcwd(),
                'environment_variables': dict(os.environ),
                'github_actions': os.getenv('GITHUB_ACTIONS', 'false'),
                'github_workflow': os.getenv('GITHUB_WORKFLOW', 'N/A'),
                'github_run_id': os.getenv('GITHUB_RUN_ID', 'N/A')
            }
            
            env_text = f"""Environment Information:
Python Version: {env_info['python_version']}
Platform: {env_info['platform']}
Working Directory: {env_info['working_directory']}
GitHub Actions: {env_info['github_actions']}
GitHub Workflow: {env_info['github_workflow']}
GitHub Run ID: {env_info['github_run_id']}"""
            
            self.db_helper.store_test_result_in_tables(
                test_case_name="environment_info",
                module_name="system_information",
                test_status="PASSED",
                error_message=env_text,
                device_name="system_environment",
                screen_resolution="environment_capture"
            )
            
        except Exception as e:
            print(f"❌ Error capturing environment info: {e}")
    
    def _determine_test_status(self, content):
        """Determine test status from content"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['passed', 'success', 'ok', 'green', '✓']):
            return "PASSED"
        elif any(word in content_lower for word in ['failed', 'failure', 'error', 'red', '✗', '❌']):
            return "FAILED"
        elif any(word in content_lower for word in ['skipped', 'skip']):
            return "SKIPPED"
        else:
            return "ERROR"
    
    def _show_summary(self):
        """Show capture summary"""
        try:
            # Get recent test results
            results = self.db_helper.get_test_results(limit=10)
            
            print("\n📊 Recent Test Results Summary:")
            print("=" * 40)
            
            for result in results:
                print(f"✅ {result['test_case_name']} - {result['test_status']} ({result['module_name']})")
            
            # Get statistics
            stats = self.db_helper.get_test_statistics()
            
            if stats:
                print(f"\n📈 Overall Statistics:")
                print(f"Total Tests: {stats['total_tests']}")
                print(f"Passed: {stats['passed_tests']}")
                print(f"Failed: {stats['failed_tests']}")
                print(f"Skipped: {stats['skipped_tests']}")
                print(f"Errors: {stats['error_tests']}")
            
        except Exception as e:
            print(f"❌ Error showing summary: {e}")
    
    def close(self):
        """Close all connections"""
        self.db_helper.close()
        self.parser.close()


def main():
    """Main function"""
    try:
        print("🔧 Comprehensive Test Log Capture System")
        print("=" * 60)
        
        # Initialize capture system
        capture = ComprehensiveLogCapture()
        
        # Capture all logs
        capture.capture_all_logs()
        
        # Close connections
        capture.close()
        
        print("\n🎉 All test logs captured and stored in database!")
        print("📊 Check the test_results table for comprehensive log data.")
        
    except Exception as e:
        print(f"❌ Log capture failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
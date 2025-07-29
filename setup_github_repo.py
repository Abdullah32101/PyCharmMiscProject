#!/usr/bin/env python3
"""
GitHub Repository Setup Script
This script helps you set up a GitHub repository and push your code.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return None

def main():
    print("🚀 GitHub Repository Setup Script")
    print("=" * 50)
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("❌ Git is not installed. Please install Git first.")
        return
    
    # Check current git status
    status = run_command("git status", "Checking Git status")
    if not status:
        return
    
    print("\n📋 Current Git Status:")
    print(status)
    
    # Get repository name from user
    print("\n" + "=" * 50)
    print("📝 GitHub Repository Setup")
    print("=" * 50)
    
    repo_name = input("Enter the GitHub repository name (e.g., solutioninn-test-automation): ").strip()
    if not repo_name:
        print("❌ Repository name is required.")
        return
    
    github_username = input("Enter your GitHub username: ").strip()
    if not github_username:
        print("❌ GitHub username is required.")
        return
    
    # Create remote URL
    remote_url = f"https://github.com/{github_username}/{repo_name}.git"
    
    print(f"\n🔗 Remote URL will be: {remote_url}")
    
    # Instructions for creating GitHub repository
    print("\n" + "=" * 50)
    print("📋 Manual Steps Required:")
    print("=" * 50)
    print("1. Go to https://github.com/new")
    print(f"2. Repository name: {repo_name}")
    print("3. Description: SolutionInn Automated Testing System")
    print("4. Make it Public or Private (your choice)")
    print("5. DO NOT initialize with README, .gitignore, or license")
    print("6. Click 'Create repository'")
    print("\nAfter creating the repository, come back here and press Enter to continue...")
    
    input("\nPress Enter when you've created the GitHub repository...")
    
    # Add remote origin
    if not run_command(f'git remote add origin {remote_url}', "Adding remote origin"):
        return
    
    # Push to GitHub
    print("\n" + "=" * 50)
    print("🚀 Pushing Code to GitHub")
    print("=" * 50)
    
    if not run_command("git branch -M main", "Setting main branch"):
        return
    
    if not run_command("git push -u origin main", "Pushing code to GitHub"):
        print("\n⚠️  If you get an authentication error, you may need to:")
        print("1. Use a Personal Access Token instead of password")
        print("2. Or use GitHub CLI: gh auth login")
        print("3. Or configure SSH keys")
        return
    
    print("\n" + "=" * 50)
    print("🎉 SUCCESS! Your code has been pushed to GitHub!")
    print("=" * 50)
    print(f"Repository URL: https://github.com/{github_username}/{repo_name}")
    print(f"Clone URL: {remote_url}")
    
    # Additional setup instructions
    print("\n📋 Next Steps:")
    print("1. Set up GitHub Actions workflows")
    print("2. Configure database secrets in GitHub")
    print("3. Set up email notifications")
    print("4. Configure branch protection rules")
    
    print("\n🔧 GitHub Actions Setup:")
    print("1. Go to your repository Settings > Secrets and variables > Actions")
    print("2. Add the following secrets:")
    print("   - DB_HOST: Your database host")
    print("   - DB_USER: Your database username")
    print("   - DB_PASSWORD: Your database password")
    print("   - DB_NAME: Your database name")
    print("   - EMAIL_PASSWORD: Your email password for notifications")

if __name__ == "__main__":
    main() 
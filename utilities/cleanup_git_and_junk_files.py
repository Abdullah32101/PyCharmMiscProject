#!/usr/bin/env python3
"""
Git History and Junk Files Cleanup Script
This script removes all git history files and junk files from the directory.
"""

import os
import shutil
import glob
from pathlib import Path

def cleanup_git_and_junk_files():
    """Remove all git history files and junk files from the current directory"""
    print("🧹 Starting cleanup of git history and junk files...")
    print("=" * 60)
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"📁 Working directory: {current_dir}")
    
    # Define junk directories and files to remove
    junk_directories = [
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".idea",
        ".vscode",
        ".github",
        "node_modules",  # In case there are any Node.js files
        "venv",          # Virtual environment
        "env",           # Alternative virtual environment
        ".env",          # Environment files
        "dist",          # Distribution files
        "build",         # Build files
        ".mypy_cache",   # MyPy cache
        ".coverage",     # Coverage files
        "htmlcov",       # HTML coverage reports
        ".tox",          # Tox cache
        ".eggs",         # Python eggs
        "*.egg-info",    # Egg info directories
    ]
    
    junk_files = [
        "*.pyc",         # Python compiled files
        "*.pyo",         # Python optimized files
        "*.pyd",         # Python dynamic modules
        "*.so",          # Shared objects
        "*.dll",         # Windows DLLs
        "*.exe",         # Executables
        "*.log",         # Log files
        "*.tmp",         # Temporary files
        "*.temp",        # Temporary files
        "*.bak",         # Backup files
        "*.swp",         # Vim swap files
        "*.swo",         # Vim swap files
        "*~",            # Backup files
        ".DS_Store",     # macOS system files
        "Thumbs.db",     # Windows thumbnail cache
        "desktop.ini",   # Windows desktop configuration
        ".gitignore",    # Git ignore files (if you want to remove them)
        ".gitattributes", # Git attributes
        ".gitmodules",   # Git submodules
        ".gitkeep",      # Git keep files
        ".git-blame*",   # Git blame files
        ".git-rewrite*", # Git rewrite files
        ".git-merge*",   # Git merge files
        ".git-rebase*",  # Git rebase files
        ".git-*",        # Any other git files
    ]
    
    removed_dirs = []
    removed_files = []
    
    print("\n🗂️  Removing junk directories:")
    
    # Remove junk directories
    for pattern in junk_directories:
        if pattern.startswith("*"):
            # Handle glob patterns
            matches = list(current_dir.glob(pattern))
            for match in matches:
                if match.is_dir():
                    try:
                        shutil.rmtree(match)
                        print(f"   🗑️  Removed directory: {match.name}")
                        removed_dirs.append(str(match))
                    except Exception as e:
                        print(f"   ❌ Error removing {match.name}: {e}")
        else:
            # Handle specific directory names
            dir_path = current_dir / pattern
            if dir_path.exists() and dir_path.is_dir():
                try:
                    shutil.rmtree(dir_path)
                    print(f"   🗑️  Removed directory: {pattern}")
                    removed_dirs.append(pattern)
                except Exception as e:
                    print(f"   ❌ Error removing {pattern}: {e}")
    
    print(f"\n📄 Removing junk files:")
    
    # Remove junk files
    for pattern in junk_files:
        matches = list(current_dir.glob(pattern))
        for match in matches:
            if match.is_file():
                try:
                    match.unlink()
                    print(f"   🗑️  Removed file: {match.name}")
                    removed_files.append(str(match))
                except Exception as e:
                    print(f"   ❌ Error removing {match.name}: {e}")
    
    # Also check for common junk files in subdirectories
    print(f"\n🔍 Checking subdirectories for junk files:")
    
    for root, dirs, files in os.walk(current_dir):
        root_path = Path(root)
        
        # Skip directories we're about to remove
        dirs[:] = [d for d in dirs if not any(junk in str(root_path / d) for junk in junk_directories)]
        
        for file in files:
            file_path = root_path / file
            if any(file_path.match(pattern) for pattern in junk_files):
                try:
                    file_path.unlink()
                    print(f"   🗑️  Removed file: {file_path.relative_to(current_dir)}")
                    removed_files.append(str(file_path))
                except Exception as e:
                    print(f"   ❌ Error removing {file_path.relative_to(current_dir)}: {e}")
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"📊 CLEANUP SUMMARY:")
    print(f"   Directories removed: {len(removed_dirs)}")
    print(f"   Files removed: {len(removed_files)}")
    print(f"   Total items removed: {len(removed_dirs) + len(removed_files)}")
    
    if removed_dirs:
        print(f"\n🗂️  Removed directories:")
        for dir_name in removed_dirs:
            print(f"   - {dir_name}")
    
    if removed_files:
        print(f"\n📄 Removed files (showing first 20):")
        for file_name in removed_files[:20]:
            print(f"   - {file_name}")
        if len(removed_files) > 20:
            print(f"   ... and {len(removed_files) - 20} more files")
    
    print(f"\n✅ Git history and junk files cleanup completed!")

def main():
    """Main function"""
    print("🚀 Git History and Junk Files Cleanup Script")
    print("=" * 60)
    
    cleanup_git_and_junk_files()
    
    print("\n" + "=" * 60)
    print("✨ Cleanup process completed!")
    print("💡 Note: This removes all git history. If you need version control,")
    print("   you'll need to reinitialize git with: git init")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Cleanup Old Files Script
This script removes all PNG images and HTML reports from the directory.
"""

import os
import glob
from pathlib import Path

def cleanup_files():
    """Remove all PNG images and HTML reports from the current directory"""
    print("🧹 Starting cleanup of PNG images and HTML reports...")
    print("=" * 60)
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"📁 Working directory: {current_dir}")
    
    # Find all PNG files
    png_files = list(current_dir.glob("*.png"))
    print(f"\n🖼️  Found {len(png_files)} PNG files:")
    
    # Find all HTML files
    html_files = list(current_dir.glob("*.html"))
    print(f"📄 Found {len(html_files)} HTML files:")
    
    # Count total files to remove
    total_files = len(png_files) + len(html_files)
    
    if total_files == 0:
        print("✅ No PNG or HTML files found to remove!")
        return
    
    # Show files that will be removed
    if png_files:
        print("\n🖼️  PNG files to be removed:")
        for png_file in png_files:
            print(f"   - {png_file.name}")
    
    if html_files:
        print("\n📄 HTML files to be removed:")
        for html_file in html_files:
            print(f"   - {html_file.name}")
    
    # Ask for confirmation
    print(f"\n⚠️  About to remove {total_files} files:")
    print(f"   - {len(png_files)} PNG images")
    print(f"   - {len(html_files)} HTML reports")
    
    # Auto-confirm for automation
    confirm = True
    print("✅ Auto-confirming removal...")
    
    if confirm:
        removed_count = 0
        
        # Remove PNG files
        for png_file in png_files:
            try:
                png_file.unlink()
                print(f"🗑️  Removed: {png_file.name}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {png_file.name}: {e}")
        
        # Remove HTML files
        for html_file in html_files:
            try:
                html_file.unlink()
                print(f"🗑️  Removed: {html_file.name}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Error removing {html_file.name}: {e}")
        
        print(f"\n✅ Cleanup completed! Removed {removed_count} files.")
        
        # Calculate space saved
        total_size_saved = 0
        for file_path in png_files + html_files:
            try:
                if file_path.exists():
                    total_size_saved += file_path.stat().st_size
            except:
                pass
        
        if total_size_saved > 0:
            size_mb = total_size_saved / (1024 * 1024)
            print(f"💾 Space saved: {size_mb:.2f} MB")
    else:
        print("❌ Cleanup cancelled.")

def main():
    """Main function"""
    print("🚀 File Cleanup Script")
    print("=" * 60)
    
    cleanup_files()
    
    print("\n" + "=" * 60)
    print("✨ Cleanup process completed!")

if __name__ == "__main__":
    main()

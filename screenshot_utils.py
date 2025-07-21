#!/usr/bin/env python3
"""
Utility module for managing screenshots and generating error links
"""

import os
import time
from datetime import datetime
from pathlib import Path

class ScreenshotManager:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.screenshots_dir = self.base_dir / "screenshots"
        self.screenshots_dir.mkdir(exist_ok=True)
    
    def capture_screenshot(self, driver, test_name, stage="", error=False):
        """
        Capture a screenshot and return the file path and URL
        
        Args:
            driver: Selenium WebDriver instance
            test_name: Name of the test
            stage: Test stage (primary, secondary, etc.)
            error: Whether this is an error screenshot
            
        Returns:
            tuple: (file_path, error_link)
        """
        timestamp = int(time.time())
        
        # Create filename
        if error:
            filename = f"{test_name}_error_{stage}_{timestamp}.png" if stage else f"{test_name}_error_{timestamp}.png"
        else:
            filename = f"{test_name}_final_{stage}_{timestamp}.png" if stage else f"{test_name}_final_{timestamp}.png"
        
        # Ensure filename is safe
        filename = self._sanitize_filename(filename)
        
        # Full file path
        file_path = self.screenshots_dir / filename
        
        try:
            # Capture screenshot
            driver.save_screenshot(str(file_path))
            
            # Generate error link (file:// URL for local access)
            error_link = f"file://{file_path.absolute()}"
            
            print(f"[📸] Screenshot saved: {filename}")
            print(f"[🔗] Error link: {error_link}")
            
            return str(file_path), error_link
            
        except Exception as e:
            print(f"[❌] Failed to capture screenshot: {e}")
            return None, None
    
    def capture_page_source(self, driver, test_name, stage="", error=False):
        """
        Capture page source and return the file path and URL
        
        Args:
            driver: Selenium WebDriver instance
            test_name: Name of the test
            stage: Test stage (primary, secondary, etc.)
            error: Whether this is an error page source
            
        Returns:
            tuple: (file_path, error_link)
        """
        timestamp = int(time.time())
        
        # Create filename
        if error:
            filename = f"{test_name}_error_{stage}_{timestamp}.html" if stage else f"{test_name}_error_{timestamp}.html"
        else:
            filename = f"{test_name}_final_{stage}_{timestamp}.html" if stage else f"{test_name}_final_{timestamp}.html"
        
        # Ensure filename is safe
        filename = self._sanitize_filename(filename)
        
        # Full file path
        file_path = self.screenshots_dir / filename
        
        try:
            # Capture page source
            page_source = driver.page_source
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(page_source)
            
            # Generate error link (file:// URL for local access)
            error_link = f"file://{file_path.absolute()}"
            
            print(f"[📄] Page source saved: {filename}")
            print(f"[🔗] Error link: {error_link}")
            
            return str(file_path), error_link
            
        except Exception as e:
            print(f"[❌] Failed to capture page source: {e}")
            return None, None
    
    def _sanitize_filename(self, filename):
        """Sanitize filename to be safe for file system"""
        # Replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Limit length
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:200-len(ext)] + ext
        
        return filename
    
    def get_screenshot_url(self, file_path):
        """Convert file path to file:// URL"""
        if file_path and os.path.exists(file_path):
            return f"file://{os.path.abspath(file_path)}"
        return None
    
    def cleanup_old_screenshots(self, days=7):
        """Clean up screenshots older than specified days"""
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        for file_path in self.screenshots_dir.glob("*.png"):
            if file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                    print(f"[🗑️] Deleted old screenshot: {file_path.name}")
                except Exception as e:
                    print(f"[⚠️] Failed to delete {file_path.name}: {e}")
        
        for file_path in self.screenshots_dir.glob("*.html"):
            if file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                    print(f"[🗑️] Deleted old page source: {file_path.name}")
                except Exception as e:
                    print(f"[⚠️] Failed to delete {file_path.name}: {e}")

# Global instance
screenshot_manager = ScreenshotManager() 
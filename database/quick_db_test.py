#!/usr/bin/env python3
"""
Quick Database Connection Test
Fast connectivity test with 5-second timeout
"""

import mysql.connector
import sys
from db.db_config import DB_CONFIG

def quick_connection_test():
    """Test database connection with 5-second timeout"""
    try:
        print("🧪 Quick connectivity test...")
        conn = mysql.connector.connect(**DB_CONFIG, connection_timeout=5)
        print("✅ Quick connection successful!")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Quick connection failed: {e}")
        return False

if __name__ == "__main__":
    if quick_connection_test():
        sys.exit(0)
    else:
        sys.exit(1) 
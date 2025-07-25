#!/usr/bin/env python3
"""
Test script to verify GitHub Actions database configuration
"""

import os
import sys
from db.db_config import get_database_config, is_github_actions

def test_github_actions_config():
    """Test GitHub Actions database configuration"""
    print("🧪 Testing GitHub Actions Database Configuration")
    print("=" * 60)
    
    # Test environment detection
    print(f"🔍 Environment Detection:")
    print(f"   GitHub Actions: {is_github_actions()}")
    print(f"   GITHUB_ACTIONS env var: {os.getenv('GITHUB_ACTIONS')}")
    
    # Get database configuration
    config = get_database_config()
    
    print(f"\n📋 Database Configuration:")
    print(f"   Host: {config['host']}")
    print(f"   Port: {config['port']}")
    print(f"   Database: {config['database']}")
    print(f"   User: {config['user']}")
    print(f"   Password: {'*' * len(config['password']) if config['password'] else 'None'}")
    
    # Test connection
    try:
        import mysql.connector
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            print(f"\n✅ Database connection successful!")
            print(f"   Test query result: {result}")
            return True
        else:
            print(f"\n❌ Database connection failed!")
            return False
            
    except Exception as e:
        print(f"\n❌ Database connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_github_actions_config()
    sys.exit(0 if success else 1) 
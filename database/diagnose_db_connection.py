#!/usr/bin/env python3
"""
Database Connection Diagnostic Script
Comprehensive analysis of why database connection is failing
"""

import socket
import subprocess
import sys
import time
from datetime import datetime

def test_dns_resolution():
    """Test if the hostname can be resolved"""
    print("🔍 Testing DNS Resolution...")
    try:
        ip_address = socket.gethostbyname("solutionsole.com")
        print(f"✅ DNS Resolution successful: solutionsole.com -> {ip_address}")
        return ip_address
    except socket.gaierror as e:
        print(f"❌ DNS Resolution failed: {e}")
        return None

def test_port_connectivity(host, port=3306):
    """Test if the port is reachable"""
    print(f"🔍 Testing Port Connectivity: {host}:{port}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} is reachable on {host}")
            return True
        else:
            print(f"❌ Port {port} is NOT reachable on {host}")
            print(f"   Error code: {result}")
            return False
    except Exception as e:
        print(f"❌ Port connectivity test failed: {e}")
        return False

def test_mysql_connection():
    """Test MySQL connection with detailed error reporting"""
    print("🔍 Testing MySQL Connection...")
    try:
        import mysql.connector
        from db.db_config import DB_CONFIG
        
        print(f"   Host: {DB_CONFIG['host']}")
        print(f"   User: {DB_CONFIG['user']}")
        print(f"   Database: {DB_CONFIG['database']}")
        print(f"   Port: 3306 (default)")
        
        # Try connection with different timeouts
        for timeout in [5, 10, 30]:
            print(f"   Trying with {timeout}s timeout...")
            try:
                conn = mysql.connector.connect(
                    **DB_CONFIG, 
                    connection_timeout=timeout,
                    autocommit=True
                )
                print(f"✅ MySQL connection successful with {timeout}s timeout!")
                conn.close()
                return True
            except mysql.connector.Error as e:
                print(f"   ❌ Failed with {timeout}s timeout: {e}")
                if e.errno:
                    print(f"   Error code: {e.errno}")
                    print(f"   Error message: {e.msg}")
                
                # Provide specific troubleshooting based on error code
                if e.errno == 2003:  # Can't connect to MySQL server
                    print("   🔧 This usually means:")
                    print("      - MySQL server is not running")
                    print("      - Firewall is blocking the connection")
                    print("      - MySQL is not configured for remote access")
                elif e.errno == 1045:  # Access denied
                    print("   🔧 This usually means:")
                    print("      - Wrong username/password")
                    print("      - User doesn't have remote access permissions")
                elif e.errno == 1049:  # Unknown database
                    print("   🔧 This usually means:")
                    print("      - Database 'test' doesn't exist")
                    print("      - Wrong database name")
                
                if timeout < 30:  # Don't wait for the last attempt
                    time.sleep(1)
                    
        return False
        
    except ImportError:
        print("❌ mysql-connector-python not installed")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_github_actions_connectivity():
    """Test connectivity from GitHub Actions perspective"""
    print("🔍 Testing GitHub Actions Connectivity...")
    
    # GitHub Actions IP ranges (partial list)
    github_ips = [
        "140.82.112.0/20",
        "143.55.64.0/20", 
        "185.199.108.0/22",
        "192.30.252.0/22"
    ]
    
    print("📋 GitHub Actions IP ranges that need firewall access:")
    for ip_range in github_ips:
        print(f"   - {ip_range}")
    
    print("\n🔧 To fix GitHub Actions connectivity:")
    print("   1. Add these IP ranges to your firewall")
    print("   2. Allow port 3306 for these ranges")
    print("   3. Configure MySQL to accept remote connections")

def main():
    """Main diagnostic function"""
    print("=" * 60)
    print("🔧 DATABASE CONNECTION DIAGNOSTIC")
    print("=" * 60)
    print(f"📅 Time: {datetime.now()}")
    print(f"🎯 Target: solutionsole.com:3306")
    print("=" * 60)
    
    # Test DNS resolution
    ip_address = test_dns_resolution()
    print()
    
    if ip_address:
        # Test port connectivity
        port_ok = test_port_connectivity(ip_address, 3306)
        print()
        
        if port_ok:
            # Test MySQL connection
            mysql_ok = test_mysql_connection()
            print()
        else:
            print("⚠️ Skipping MySQL test since port is not reachable")
            mysql_ok = False
    else:
        print("⚠️ Skipping port and MySQL tests since DNS failed")
        port_ok = False
        mysql_ok = False
    
    # GitHub Actions specific info
    test_github_actions_connectivity()
    print()
    
    # Summary
    print("📊 DIAGNOSTIC SUMMARY:")
    print("-" * 30)
    print(f"DNS Resolution: {'✅' if ip_address else '❌'}")
    print(f"Port Connectivity: {'✅' if port_ok else '❌'}")
    print(f"MySQL Connection: {'✅' if mysql_ok else '❌'}")
    print()
    
    if not ip_address:
        print("🚨 ISSUE: DNS resolution failed")
        print("   - Check if solutionsole.com is correct")
        print("   - Verify domain is active")
    elif not port_ok:
        print("🚨 ISSUE: Port 3306 is not reachable")
        print("   - MySQL server may not be running")
        print("   - Firewall may be blocking port 3306")
        print("   - Server may not be accepting external connections")
    elif not mysql_ok:
        print("🚨 ISSUE: MySQL connection failed")
        print("   - Check MySQL configuration")
        print("   - Verify user permissions")
        print("   - Check MySQL bind-address setting")
    else:
        print("✅ All tests passed! Database should be accessible.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 
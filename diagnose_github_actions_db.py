#!/usr/bin/env python3
"""
GitHub Actions Database Connection Diagnostic
Comprehensive troubleshooting for database connection timeouts in CI/CD
"""

import os
import sys
import socket
import subprocess
import time
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("=" * 60)
    print(f"🔧 {title}")
    print("=" * 60)

def print_status(message):
    """Print a status message"""
    print(f"📋 {message}")

def print_success(message):
    """Print a success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print an error message"""
    print(f"❌ {message}")

def print_warning(message):
    """Print a warning message"""
    print(f"⚠️ {message}")

def test_dns_resolution(host):
    """Test DNS resolution for the host"""
    print_status(f"Testing DNS resolution for {host}...")
    try:
        ip_address = socket.gethostbyname(host)
        print_success(f"DNS resolution successful: {host} -> {ip_address}")
        return ip_address
    except socket.gaierror as e:
        print_error(f"DNS resolution failed: {e}")
        return None

def test_port_connectivity(host, port, timeout=5):
    """Test if a port is reachable"""
    print_status(f"Testing port connectivity to {host}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print_success(f"Port {port} is reachable on {host}")
            return True
        else:
            print_error(f"Port {port} is not reachable on {host}")
            return False
    except Exception as e:
        print_error(f"Port connectivity test failed: {e}")
        return False

def test_mysql_connection():
    """Test MySQL connection with detailed error reporting"""
    print_status("Testing MySQL Connection...")
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
                print_success(f"MySQL connection successful with {timeout}s timeout!")
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
                    print("      - Database 'solutioninn_testing' doesn't exist")
                    print("      - Wrong database name")
                
                if timeout < 30:  # Don't wait for the last attempt
                    time.sleep(1)
                    
        return False
        
    except ImportError:
        print_error("mysql-connector-python not installed")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def test_github_actions_connectivity():
    """Test connectivity from GitHub Actions perspective"""
    print_status("Testing GitHub Actions Connectivity...")
    
    # Check if we're in GitHub Actions
    if os.getenv('GITHUB_ACTIONS'):
        print("   Running in GitHub Actions environment")
        print(f"   Runner OS: {os.getenv('RUNNER_OS', 'Unknown')}")
        print(f"   Runner Architecture: {os.getenv('RUNNER_ARCH', 'Unknown')}")
        
        # Test basic network connectivity
        try:
            import requests
            response = requests.get('https://httpbin.org/ip', timeout=10)
            external_ip = response.json().get('origin', 'Unknown')
            print(f"   External IP: {external_ip}")
        except Exception as e:
            print(f"   Could not determine external IP: {e}")
    else:
        print("   Running in local environment")
        
        # Test if we can reach common GitHub Actions IP ranges
        github_ips = [
            '140.82.112.0/20',
            '143.55.64.0/20',
            '185.199.108.0/22',
            '192.30.252.0/22'
        ]
        print("   Note: GitHub Actions uses various IP ranges that may change")

def get_troubleshooting_steps():
    """Provide specific troubleshooting steps"""
    print_header("TROUBLESHOOTING STEPS")
    
    print_status("Based on the diagnostic results, here are the recommended steps:")
    print()
    
    print("🔧 SERVER-SIDE FIXES:")
    print("1. SSH into your database server (18.235.51.183)")
    print("2. Check MySQL bind-address configuration:")
    print("   grep bind-address /etc/mysql/mysql.conf.d/mysqld.cnf")
    print("   # Should show: bind-address = 0.0.0.0")
    print()
    print("3. If bind-address is not 0.0.0.0, update it:")
    print("   sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf")
    print("   # Change: bind-address = 0.0.0.0")
    print("   sudo systemctl restart mysql")
    print()
    print("4. Check user permissions:")
    print("   mysql -u root -p")
    print("   SELECT user, host FROM mysql.user WHERE user = 'sqa_user';")
    print("   # Should show: sqa_user | %")
    print()
    print("5. If user doesn't have '%' host, grant permissions:")
    print("   GRANT ALL PRIVILEGES ON solutioninn_testing.* TO 'sqa_user'@'%';")
    print("   FLUSH PRIVILEGES;")
    print()
    print("6. Check firewall settings:")
    print("   sudo ufw status")
    print("   sudo ufw allow 3306")
    print()
    
    print("🌐 NETWORK FIXES:")
    print("1. Allow GitHub Actions IP ranges in firewall:")
    print("   sudo ufw allow from 140.82.112.0/20 to any port 3306")
    print("   sudo ufw allow from 143.55.64.0/20 to any port 3306")
    print("   sudo ufw allow from 185.199.108.0/22 to any port 3306")
    print("   sudo ufw allow from 192.30.252.0/22 to any port 3306")
    print()
    print("2. Or temporarily allow all external connections (for testing):")
    print("   sudo ufw allow 3306")
    print()
    
    print("🧪 TESTING:")
    print("1. Test local connection on server:")
    print("   mysql -u sqa_user -p'Hassan123!@#' -h localhost solutioninn_testing")
    print()
    print("2. Test external connection:")
    print("   mysql -u sqa_user -p'Hassan123!@#' -h 18.235.51.183 solutioninn_testing")
    print()
    print("3. Check if port is listening:")
    print("   sudo netstat -tlnp | grep :3306")
    print()

def main():
    """Main diagnostic function"""
    print_header("GITHUB ACTIONS DATABASE CONNECTION DIAGNOSTIC")
    print(f"📅 Time: {datetime.now()}")
    print(f"🎯 Target: 18.235.51.183:3306")
    print()
    
    # Test DNS resolution
    ip_address = test_dns_resolution("18.235.51.183")
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
    print_header("DIAGNOSTIC SUMMARY")
    print(f"DNS Resolution: {'✅' if ip_address else '❌'}")
    print(f"Port Connectivity: {'✅' if port_ok else '❌'}")
    print(f"MySQL Connection: {'✅' if mysql_ok else '❌'}")
    print()
    
    if not mysql_ok:
        get_troubleshooting_steps()
    else:
        print_success("Database connection is working! The issue might be intermittent.")
        print_status("If GitHub Actions still fails, check the server logs for connection attempts.")

if __name__ == "__main__":
    main() 
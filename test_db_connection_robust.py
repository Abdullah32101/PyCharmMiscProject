#!/usr/bin/env python3
"""
Robust Database Connection Test
Enhanced connection test with better error handling and timeout management
"""

import os
import sys
import time
import threading
from datetime import datetime

def timeout_handler(timeout_seconds):
    """Handle timeout using threading instead of signals (works on Windows)"""
    def timeout_function():
        time.sleep(timeout_seconds)
        print("❌ Database connection timed out!")
        print("🔍 This usually means:")
        print("   - Server firewall is blocking GitHub Actions IP ranges")
        print("   - MySQL bind-address is not set to 0.0.0.0")
        print("   - User permissions don't allow external connections")
        os._exit(124)
    
    timer = threading.Timer(timeout_seconds, timeout_function)
    timer.daemon = True
    timer.start()
    return timer

def test_robust_connection():
    """Test database connection with comprehensive error handling"""
    
    # Set timeout for the entire operation (30 seconds)
    timer = timeout_handler(30)
    
    try:
        import mysql.connector
        from db.db_config import DB_CONFIG
        
        print("🔧 Testing database connection...")
        print(f"📅 Time: {datetime.now()}")
        print(f"🖥️ Environment: {'GitHub Actions' if os.getenv('GITHUB_ACTIONS') else 'Local'}")
        print(f"🗄️ Database Host: {DB_CONFIG['host']}")
        print(f"📊 Database Name: {DB_CONFIG['database']}")
        print(f"👤 Database User: {DB_CONFIG['user']}")
        print("")
        
        # Try connection with progressive timeouts
        timeouts = [5, 10, 15]
        
        for timeout in timeouts:
            print(f"⏱️ Attempting connection with {timeout}s timeout...")
            try:
                conn = mysql.connector.connect(
                    **DB_CONFIG,
                    connection_timeout=timeout,
                    autocommit=True
                )
                
                # Cancel the timer since connection succeeded
                timer.cancel()
                
                print(f"✅ Database connection successful with {timeout}s timeout!")
                
                # Test basic functionality
                cursor = conn.cursor(dictionary=True)
                
                # Test simple query
                cursor.execute("SELECT COUNT(*) as count FROM test_results")
                result = cursor.fetchone()
                test_count = result['count'] if result else 0
                
                print(f"📊 Current test records: {test_count}")
                
                # Test table structure
                cursor.execute("DESCRIBE test_results")
                columns = cursor.fetchall()
                print(f"📋 test_results table has {len(columns)} columns")
                
                cursor.close()
                conn.close()
                
                print("")
                print("🎉 Database connection test completed successfully!")
                return True
                
            except mysql.connector.Error as e:
                print(f"❌ Connection failed with {timeout}s timeout: {e}")
                
                # Provide specific troubleshooting based on error code
                if hasattr(e, 'errno'):
                    if e.errno == 2003:  # Can't connect to MySQL server
                        print("🔧 Error 2003 - Connection refused:")
                        print("   - Check if MySQL is running")
                        print("   - Verify firewall allows port 3306")
                        print("   - Check MySQL bind-address configuration")
                    elif e.errno == 1045:  # Access denied
                        print("🔧 Error 1045 - Access denied:")
                        print("   - Verify username and password")
                        print("   - Check user permissions for external connections")
                        print("   - Ensure user has '%' host permission")
                    elif e.errno == 1049:  # Unknown database
                        print("🔧 Error 1049 - Unknown database:")
                        print("   - Verify database name is correct")
                        print("   - Check if database exists")
                    elif e.errno == 2013:  # Lost connection
                        print("🔧 Error 2013 - Lost connection:")
                        print("   - Network connectivity issues")
                        print("   - Server overload or timeout")
                
                if timeout < 15:  # Don't wait for the last attempt
                    print("⏳ Waiting 2 seconds before next attempt...")
                    time.sleep(2)
        
        # If we get here, all attempts failed
        timer.cancel()
        print("")
        print("❌ All connection attempts failed!")
        print("🔧 Recommended fixes:")
        print("1. SSH into your database server (18.235.51.183)")
        print("2. Run: sudo ufw allow 3306")
        print("3. Check: grep bind-address /etc/mysql/mysql.conf.d/mysqld.cnf")
        print("4. Ensure: bind-address = 0.0.0.0")
        print("5. Restart MySQL: sudo systemctl restart mysql")
        print("6. Grant permissions: GRANT ALL PRIVILEGES ON solutioninn_testing.* TO 'sqa_user'@'%';")
        
        return False
        
    except ImportError:
        timer.cancel()
        print("❌ mysql-connector-python not installed")
        print("🔧 Install with: pip install mysql-connector-python")
        return False
        
    except Exception as e:
        timer.cancel()
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("🔧 ROBUST DATABASE CONNECTION TEST")
    print("=" * 60)
    
    success = test_robust_connection()
    
    print("=" * 60)
    if success:
        print("✅ CONNECTION TEST PASSED")
        sys.exit(0)
    else:
        print("❌ CONNECTION TEST FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main() 
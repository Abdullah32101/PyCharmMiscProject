#!/usr/bin/env python3
"""
Simple Database Test
Tests database connectivity and basic operations.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import mysql.connector
    from datetime import datetime
    
    # Database configuration
    DB_CONFIG = {
        'host': 'solutionsole.com',
        'user': 'root',
        'password': 'SolutionInn321',
        'database': 'test'
    }
    
    def test_database_connection():
        """Test basic database connection"""
        try:
            print("🔧 Testing database connection...")
            
            # Connect to database
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            print("✅ Database connection successful!")
            
            # Test creating test_results table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS test_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                test_case_name VARCHAR(255) NOT NULL,
                module_name VARCHAR(255) NOT NULL,
                test_status ENUM('PASSED', 'FAILED', 'SKIPPED', 'ERROR') NOT NULL,
                test_datetime DATETIME NOT NULL,
                error_message TEXT,
                error_summary VARCHAR(255),
                total_time_duration DECIMAL(10,3) NULL COMMENT 'Test execution time in seconds',
                device_name VARCHAR(50) NULL COMMENT 'Device type (mobile/desktop/tablet)',
                screen_resolution VARCHAR(50) NULL COMMENT 'Screen resolution (e.g., 1920x1080, 375x812)',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_table_query)
            conn.commit()
            print("✅ Test results table created/verified successfully")
            
            # Test inserting a sample test result
            insert_query = """
            INSERT INTO test_results (test_case_name, module_name, test_status, test_datetime, error_message, error_summary, total_time_duration, device_name, screen_resolution)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                'test_database_connection',
                'test_db_simple',
                'PASSED',
                datetime.now(),
                None,
                None,
                1.5,  # Sample duration
                'desktop',  # Sample device
                '1920x1080'  # Sample resolution
            ))
            conn.commit()
            print("✅ Sample test result inserted successfully")
            
            # Test retrieving test results
            cursor.execute("SELECT COUNT(*) as count FROM test_results")
            result = cursor.fetchone()
            count = result['count'] if result else 0
            print(f"✅ Retrieved test results count: {count}")
            
            # Show recent test results
            cursor.execute("SELECT * FROM test_results ORDER BY test_datetime DESC LIMIT 5")
            results = cursor.fetchall()
            
            print("\n📊 Recent Test Results:")
            print("-" * 80)
            print(f"{'ID':<4} {'Test Case':<25} {'Module':<15} {'Status':<10} {'DateTime':<20}")
            print("-" * 80)
            
            for result in results:
                test_datetime = result['test_datetime'].strftime('%Y-%m-%d %H:%M:%S') if result['test_datetime'] else 'N/A'
                print(f"{result['id']:<4} {result['test_case_name'][:24]:<25} {result['module_name'][:14]:<15} {result['test_status']:<10} {test_datetime:<20}")
            
            cursor.close()
            conn.close()
            
            print("\n🎉 All database tests passed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
            return False
    
    def main():
        """Main function"""
        print("🧪 Simple Database Test")
        print("=" * 50)
        
        success = test_database_connection()
        
        if success:
            print("\n✅ Database integration is working correctly!")
            print("You can now run your tests and they will be stored in the database.")
        else:
            print("\n❌ Database integration failed.")
            print("Please check your database configuration and connection.")
        
        return success
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install mysql-connector-python")
except Exception as e:
    print(f"❌ Unexpected error: {e}") 
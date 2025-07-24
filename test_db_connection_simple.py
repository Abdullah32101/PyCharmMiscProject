#!/usr/bin/env python3
"""
Simple Database Connection Test
"""

import mysql.connector
from db.db_config import DB_CONFIG

def test_connection():
    """Test basic database connection"""
    try:
        print("🔌 Testing database connection...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Test basic query
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        print("✅ Database connection successful")
        
        # Test table creation
        print("\n📋 Creating test_results table...")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS test_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            test_case_name VARCHAR(255) NOT NULL,
            module_name VARCHAR(255) NOT NULL,
            test_status ENUM('PASSED', 'FAILED', 'SKIPPED', 'ERROR') NOT NULL,
            test_datetime DATETIME NOT NULL,
            error_message TEXT,
            error_summary VARCHAR(255),
            total_time_duration DECIMAL(10,3) NULL,
            device_name VARCHAR(50) NULL,
            screen_resolution VARCHAR(50) NULL,
            error_link VARCHAR(500) NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("✅ test_results table created/verified")
        
        # Check existing tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n📋 Database tables ({len(tables)}):")
        for table in tables:
            table_name = list(table.values())[0]
            print(f"   - {table_name}")
        
        # Close connections properly
        cursor.close()
        conn.close()
        print("\n✅ Database test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection() 
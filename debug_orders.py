#!/usr/bin/env python3
"""
Debug Orders Table
Check what's actually stored in the orders table
"""

import sys
sys.path.append('.')

from db.db_helper import MySQLHelper

def debug_orders():
    """Debug what's in the orders table"""
    print("🔍 Debugging Orders Table")
    print("=" * 60)
    
    db = MySQLHelper()
    
    try:
        # Check all orders
        print("\n📋 All Orders in Database:")
        db.cursor.execute("""
            SELECT order_number, order_type, amount, order_date, order_status
            FROM orders 
            ORDER BY order_date DESC
        """)
        all_orders = db.cursor.fetchall()
        
        if all_orders:
            for order in all_orders:
                print(f"   - {order['order_number']}: {order['order_type']} - ${order['amount']} - {order['order_status']} - {order['order_date']}")
        else:
            print("   - No orders found")
        
        # Check orders with TEST prefix
        print("\n📋 Orders with TEST prefix:")
        db.cursor.execute("""
            SELECT order_number, order_type, amount, order_date, order_status
            FROM orders 
            WHERE order_number LIKE 'TEST-%'
            ORDER BY order_date DESC
        """)
        test_orders = db.cursor.fetchall()
        
        if test_orders:
            for order in test_orders:
                print(f"   - {order['order_number']}: {order['order_type']} - ${order['amount']} - {order['order_status']} - {order['order_date']}")
        else:
            print("   - No TEST orders found")
        
        # Check recent orders (last hour)
        print("\n📋 Recent Orders (Last Hour):")
        db.cursor.execute("""
            SELECT order_number, order_type, amount, order_date, order_status
            FROM orders 
            WHERE order_date >= NOW() - INTERVAL 1 HOUR
            ORDER BY order_date DESC
        """)
        recent_orders = db.cursor.fetchall()
        
        if recent_orders:
            for order in recent_orders:
                print(f"   - {order['order_number']}: {order['order_type']} - ${order['amount']} - {order['order_status']} - {order['order_date']}")
        else:
            print("   - No recent orders found")
        
        # Check book purchases specifically
        print("\n📚 Book Purchases:")
        db.cursor.execute("""
            SELECT order_number, order_type, amount, order_date, order_status
            FROM orders 
            WHERE order_type = 'book_purchase'
            ORDER BY order_date DESC
        """)
        book_orders = db.cursor.fetchall()
        
        if book_orders:
            for order in book_orders:
                print(f"   - {order['order_number']}: {order['order_type']} - ${order['amount']} - {order['order_status']} - {order['order_date']}")
        else:
            print("   - No book purchases found")
        
        # Check order types distribution
        print("\n📊 Order Types Distribution:")
        db.cursor.execute("""
            SELECT order_type, COUNT(*) as count 
            FROM orders 
            GROUP BY order_type 
            ORDER BY count DESC
        """)
        order_types = db.cursor.fetchall()
        
        if order_types:
            for order_type in order_types:
                print(f"   - {order_type['order_type']}: {order_type['count']} orders")
        else:
            print("   - No orders found")
        
    except Exception as e:
        print(f"❌ Error debugging orders: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_orders() 
# db_helper.py
import uuid
from datetime import datetime

import mysql.connector

from .db_config import DB_CONFIG


class MySQLHelper:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def create_test_results_table(self):
        """Create the test_results table if it doesn't exist"""
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
            error_link VARCHAR(500) NULL COMMENT 'URL link to screenshot showing affected screen',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("✅ Test results table created successfully")
        except Exception as e:
            print(f"❌ Error creating test results table: {e}")
            self.conn.rollback()

    def _create_error_summary(self, error_message):
        """Create a short error summary from the full error message"""
        if not error_message:
            return None

        import re

        # Common error patterns to extract short messages
        error_patterns = [
            r"ElementClickInterceptedException: (.+?)(?:\n|$)",
            r"NoSuchElementException: (.+?)(?:\n|$)",
            r"TimeoutException: (.+?)(?:\n|$)",
            r"AssertionError: (.+?)(?:\n|$)",
            r"WebDriverException: (.+?)(?:\n|$)",
            r"Exception: (.+?)(?:\n|$)",
            r"Message: (.+?)(?:\n|$)",  # Selenium/WebDriver error
        ]

        for pattern in error_patterns:
            match = re.search(pattern, str(error_message))
            if match:
                summary = match.group(1).strip()
                return summary[:250] if len(summary) > 250 else summary

        # If no pattern matches, take the first line and limit to 250 characters
        first_line = str(error_message).split("\n")[0].strip()
        return first_line[:250] if len(first_line) > 250 else first_line

    def insert_test_result(
        self,
        test_case_name,
        module_name,
        test_status,
        error_message=None,
        total_time_duration=None,
        device_name=None,
        screen_resolution=None,
        error_link=None,
    ):
        """Insert a test result into the database"""
        # Clean module name - remove common test prefixes
        for prefix in ("tests.test_", "tests.", "test."):
            if module_name.startswith(prefix):
                module_name = module_name[len(prefix) :]
                break

        # Create error summary
        error_summary = self._create_error_summary(error_message)

        insert_query = """
        INSERT INTO test_results (test_case_name, module_name, test_status, test_datetime, error_message, error_summary, total_time_duration, device_name, screen_resolution, error_link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(
                insert_query,
                (
                    test_case_name,
                    module_name,
                    test_status,
                    datetime.now(),
                    error_message,
                    error_summary,
                    total_time_duration,
                    device_name,
                    screen_resolution,
                    error_link,
                ),
            )
            self.conn.commit()
            print(f"✅ Test result inserted: {test_case_name} - {test_status}")
        except Exception as e:
            print(f"❌ Error inserting test result: {e}")
            self.conn.rollback()

    def store_test_result_in_tables(
        self,
        test_case_name,
        module_name,
        test_status,
        error_message=None,
        test_data=None,
        total_time_duration=None,
        device_name=None,
        screen_resolution=None,
        error_link=None,
    ):
        """Store test results in appropriate tables based on test type"""
        try:
            # Always store in test_results table
            self.insert_test_result(
                test_case_name,
                module_name,
                test_status,
                error_message,
                total_time_duration,
                device_name,
                screen_resolution,
                error_link,
            )

            # Store in specific tables based on test type
            if "book" in test_case_name.lower() or "book" in module_name.lower():
                self._store_book_test_result(
                    test_case_name, module_name, test_status, test_data
                )

            elif (
                "monthly" in test_case_name.lower() or "monthly" in module_name.lower()
            ):
                self._store_subscription_test_result(
                    test_case_name, module_name, test_status, "monthly", test_data
                )

            elif (
                "six_month" in test_case_name.lower()
                or "six_month" in module_name.lower()
            ):
                self._store_subscription_test_result(
                    test_case_name, module_name, test_status, "six_month", test_data
                )

            elif (
                "onetime" in test_case_name.lower() or "onetime" in module_name.lower()
            ):
                self._store_onetime_test_result(
                    test_case_name, module_name, test_status, test_data
                )

            elif "user" in test_case_name.lower() or "user" in module_name.lower():
                self._store_user_test_result(
                    test_case_name, module_name, test_status, test_data
                )

            else:
                # Default: store as general order
                self._store_general_order_test_result(
                    test_case_name, module_name, test_status, test_data
                )

        except Exception as e:
            print(f"❌ Error storing test result in tables: {e}")

    def _store_book_test_result(
        self, test_case_name, module_name, test_status, test_data=None
    ):
        """Store book-related test results"""
        try:
            # Create or get test user
            user_id = self._get_or_create_test_user()

            # Create or get test book
            book_id = self._get_or_create_test_book()

            # Create order record
            order_number = f"TEST-{uuid.uuid4().hex[:8].upper()}"
            order_type = "book_purchase"
            amount = 49.99 if test_status == "PASSED" else 0.00
            payment_status = "completed" if test_status == "PASSED" else "failed"
            order_status = "completed" if test_status == "PASSED" else "cancelled"

            self.cursor.execute(
                """
                INSERT INTO orders (order_number, user_id, book_id, order_type, amount, 
                                  payment_method, payment_status, order_status, order_date, completed_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    order_number,
                    user_id,
                    book_id,
                    order_type,
                    amount,
                    "credit_card",
                    payment_status,
                    order_status,
                    datetime.now(),
                    datetime.now() if test_status == "PASSED" else None,
                ),
            )

            self.conn.commit()
            print(f"✅ Book test result stored in orders table: {order_number}")

        except Exception as e:
            print(f"❌ Error storing book test result: {e}")
            self.conn.rollback()

    def _store_subscription_test_result(
        self,
        test_case_name,
        module_name,
        test_status,
        subscription_type,
        test_data=None,
    ):
        """Store subscription-related test results"""
        try:
            # Create or get test user
            user_id = self._get_or_create_test_user()

            # Create subscription record
            start_date = datetime.now().date()
            if subscription_type == "monthly":
                end_date = datetime.now().replace(month=datetime.now().month + 1).date()
                amount = 29.99
            elif subscription_type == "six_month":
                end_date = datetime.now().replace(month=datetime.now().month + 6).date()
                amount = 149.99
            else:
                end_date = datetime.now().replace(year=datetime.now().year + 1).date()
                amount = 299.99

            status = "active" if test_status == "PASSED" else "cancelled"

            self.cursor.execute(
                """
                INSERT INTO subscriptions (user_id, subscription_type, status, start_date, end_date, 
                                         amount, auto_renew, payment_method)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    user_id,
                    subscription_type,
                    status,
                    start_date,
                    end_date,
                    amount,
                    True,
                    "credit_card",
                ),
            )

            # Create corresponding order record
            order_number = f"TEST-{uuid.uuid4().hex[:8].upper()}"
            order_type = f"{subscription_type}_plan"

            self.cursor.execute(
                """
                INSERT INTO orders (order_number, user_id, order_type, amount, 
                                  payment_method, payment_status, order_status, order_date, completed_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    order_number,
                    user_id,
                    order_type,
                    amount,
                    "credit_card",
                    "completed" if test_status == "PASSED" else "failed",
                    "completed" if test_status == "PASSED" else "cancelled",
                    datetime.now(),
                    datetime.now() if test_status == "PASSED" else None,
                ),
            )

            self.conn.commit()
            print(f"✅ Subscription test result stored: {subscription_type} - {status}")

        except Exception as e:
            print(f"❌ Error storing subscription test result: {e}")
            self.conn.rollback()

    def _store_onetime_test_result(
        self, test_case_name, module_name, test_status, test_data=None
    ):
        """Store onetime plan test results"""
        try:
            # Create or get test user
            user_id = self._get_or_create_test_user()

            # Create order record for onetime plan
            order_number = f"TEST-{uuid.uuid4().hex[:8].upper()}"
            order_type = "onetime_plan"
            amount = 99.99 if test_status == "PASSED" else 0.00

            self.cursor.execute(
                """
                INSERT INTO orders (order_number, user_id, order_type, amount, 
                                  payment_method, payment_status, order_status, order_date, completed_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    order_number,
                    user_id,
                    order_type,
                    amount,
                    "credit_card",
                    "completed" if test_status == "PASSED" else "failed",
                    "completed" if test_status == "PASSED" else "cancelled",
                    datetime.now(),
                    datetime.now() if test_status == "PASSED" else None,
                ),
            )

            self.conn.commit()
            print(f"✅ Onetime plan test result stored: {order_number}")

        except Exception as e:
            print(f"❌ Error storing onetime test result: {e}")
            self.conn.rollback()

    def _store_user_test_result(
        self, test_case_name, module_name, test_status, test_data=None
    ):
        """Store user-related test results"""
        try:
            # Create test user record
            username = f"test_user_{uuid.uuid4().hex[:8]}"
            email = f"{username}@test.com"
            password_hash = "test_password_hash"

            self.cursor.execute(
                """
                INSERT INTO users (username, email, password_hash, first_name, last_name, 
                                 university, user_type, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    username,
                    email,
                    password_hash,
                    "Test",
                    "User",
                    "Test University",
                    "student",
                    test_status == "PASSED",
                ),
            )

            self.conn.commit()
            print(f"✅ User test result stored: {username}")

        except Exception as e:
            print(f"❌ Error storing user test result: {e}")
            self.conn.rollback()

    def _store_general_order_test_result(
        self, test_case_name, module_name, test_status, test_data=None
    ):
        """Store general test results as orders"""
        try:
            # Create or get test user
            user_id = self._get_or_create_test_user()

            # Create general order record
            order_number = f"TEST-{uuid.uuid4().hex[:8].upper()}"
            order_type = "book_purchase"  # Default type
            amount = 49.99 if test_status == "PASSED" else 0.00

            self.cursor.execute(
                """
                INSERT INTO orders (order_number, user_id, order_type, amount, 
                                  payment_method, payment_status, order_status, order_date, completed_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    order_number,
                    user_id,
                    order_type,
                    amount,
                    "credit_card",
                    "completed" if test_status == "PASSED" else "failed",
                    "completed" if test_status == "PASSED" else "cancelled",
                    datetime.now(),
                    datetime.now() if test_status == "PASSED" else None,
                ),
            )

            self.conn.commit()
            print(f"✅ General test result stored as order: {order_number}")

        except Exception as e:
            print(f"❌ Error storing general test result: {e}")
            self.conn.rollback()

    def _get_or_create_test_user(self):
        """Get or create a test user for test results"""
        try:
            # Try to get existing test user
            self.cursor.execute(
                "SELECT id FROM users WHERE username = 'test_user' LIMIT 1"
            )
            result = self.cursor.fetchone()

            if result:
                return result["id"]

            # Create new test user
            self.cursor.execute(
                """
                INSERT INTO users (username, email, password_hash, first_name, last_name, 
                                 university, user_type, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    "test_user",
                    "test@example.com",
                    "test_hash",
                    "Test",
                    "User",
                    "Test University",
                    "student",
                    True,
                ),
            )

            self.conn.commit()
            return self.cursor.lastrowid

        except Exception as e:
            print(f"❌ Error getting/creating test user: {e}")
            return 1  # Fallback to first user

    def _get_or_create_test_book(self):
        """Get or create a test book for test results"""
        try:
            # Try to get existing test book
            self.cursor.execute(
                "SELECT id FROM books WHERE title LIKE '%Test Book%' LIMIT 1"
            )
            result = self.cursor.fetchone()

            if result:
                return result["id"]

            # Create new test book
            self.cursor.execute(
                """
                INSERT INTO books (title, author, isbn, publisher, publication_year, 
                                 price, description, category, is_available)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    "Test Book for Automation",
                    "Test Author",
                    "978-TEST-1234",
                    "Test Publisher",
                    2024,
                    49.99,
                    "Test book for automation testing",
                    "Test Category",
                    True,
                ),
            )

            self.conn.commit()
            return self.cursor.lastrowid

        except Exception as e:
            print(f"❌ Error getting/creating test book: {e}")
            return 1  # Fallback to first book

    def get_test_results(self, limit=100):
        """Get recent test results"""
        select_query = """
        SELECT * FROM test_results 
        ORDER BY test_datetime DESC 
        LIMIT %s
        """
        try:
            self.cursor.execute(select_query, (limit,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ Error fetching test results: {e}")
            return []

    def get_test_statistics(self):
        """Get test statistics"""
        stats_query = """
        SELECT 
            COUNT(*) as total_tests,
            SUM(CASE WHEN test_status = 'PASSED' THEN 1 ELSE 0 END) as passed_tests,
            SUM(CASE WHEN test_status = 'FAILED' THEN 1 ELSE 0 END) as failed_tests,
            SUM(CASE WHEN test_status = 'SKIPPED' THEN 1 ELSE 0 END) as skipped_tests,
            SUM(CASE WHEN test_status = 'ERROR' THEN 1 ELSE 0 END) as error_tests
        FROM test_results
        """
        try:
            self.cursor.execute(stats_query)
            return self.cursor.fetchone()
        except Exception as e:
            print(f"❌ Error fetching test statistics: {e}")
            return None

    def close(self):
        self.cursor.close()
        self.conn.close()

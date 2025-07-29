-- Database Schema for Test Project
-- This file contains all table creation scripts

-- Test Results Table (already created by the system)
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
);

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    university VARCHAR(255),
    user_type ENUM('student', 'instructor', 'admin') DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. Books Table
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    author VARCHAR(255),
    isbn VARCHAR(20) UNIQUE,
    publisher VARCHAR(255),
    publication_year INT,
    price DECIMAL(10,2),
    description TEXT,
    cover_image_url VARCHAR(500),
    category VARCHAR(100),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    book_id INT,
    order_type ENUM('book_purchase', 'monthly_plan', 'three_month_plan', 'six_month_plan', 'popular_plan', 'onetime_plan') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('credit_card', 'paypal', 'free') DEFAULT 'credit_card',
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    order_status ENUM('pending', 'processing', 'completed', 'cancelled') DEFAULT 'pending',
    billing_address TEXT,
    shipping_address TEXT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_date TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE SET NULL
);

-- 4. Subscriptions Table
CREATE TABLE IF NOT EXISTS subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subscription_type ENUM('monthly', 'three_month', 'six_month', 'popular', 'onetime', 'annual') NOT NULL,
    status ENUM('active', 'cancelled', 'expired', 'pending') DEFAULT 'pending',
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    auto_renew BOOLEAN DEFAULT FALSE,
    payment_method ENUM('credit_card', 'paypal') DEFAULT 'credit_card',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Sample Data Insertion (Optional)

-- Insert sample users
INSERT INTO users (username, email, password_hash, first_name, last_name, university, user_type) VALUES
('john_doe', 'john@example.com', 'hashed_password_123', 'John', 'Doe', 'Harvard University', 'student'),
('jane_smith', 'jane@example.com', 'hashed_password_456', 'Jane', 'Smith', 'MIT', 'instructor'),
('admin_user', 'admin@example.com', 'hashed_password_789', 'Admin', 'User', 'System', 'admin');

-- Insert sample books
INSERT INTO books (title, author, isbn, publisher, publication_year, price, description, category) VALUES
('Introduction to Computer Science', 'John Smith', '978-0123456789', 'Tech Books Inc', 2023, 49.99, 'A comprehensive guide to computer science fundamentals', 'Computer Science'),
('Advanced Mathematics', 'Dr. Sarah Johnson', '978-0987654321', 'Math Publishers', 2022, 79.99, 'Advanced mathematical concepts and applications', 'Mathematics'),
('Business Management', 'Michael Brown', '978-1122334455', 'Business Press', 2023, 59.99, 'Modern business management strategies', 'Business');

-- Insert sample orders
INSERT INTO orders (order_number, user_id, book_id, order_type, amount, payment_method, payment_status, order_status) VALUES
('ORD-001', 1, 1, 'book_purchase', 49.99, 'credit_card', 'completed', 'completed'),
('ORD-002', 2, 2, 'monthly_plan', 29.99, 'credit_card', 'completed', 'completed'),
('ORD-003', 1, NULL, 'six_month_plan', 149.99, 'paypal', 'pending', 'pending');

-- Insert sample subscriptions
INSERT INTO subscriptions (user_id, subscription_type, status, start_date, end_date, amount, auto_renew) VALUES
(1, 'monthly', 'active', '2024-01-01', '2024-02-01', 29.99, TRUE),
(2, 'six_month', 'active', '2024-01-01', '2024-07-01', 149.99, FALSE);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_books_isbn ON books(isbn);
CREATE INDEX idx_books_category ON books(category);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_order_number ON orders(order_number);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_test_results_datetime ON test_results(test_datetime);
CREATE INDEX idx_test_results_status ON test_results(test_status); 
# Database Tables Documentation

This document describes the 4 additional tables created in your test database, along with the existing `test_results` table.

## Table Overview

| Table | Purpose | Key Features |
|-------|---------|--------------|
| `test_results` | Store test execution results | Automatic capture, status tracking |
| `users` | User management | Authentication, profiles, roles |
| `books` | Book catalog | Inventory, pricing, categories |
| `orders` | Order management | Purchases, subscriptions, payments |
| `subscriptions` | Subscription tracking | Plans, billing, renewals |

## 1. test_results Table

**Purpose**: Automatically stores all test execution results

```sql
CREATE TABLE test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_case_name VARCHAR(255) NOT NULL,
    module_name VARCHAR(255) NOT NULL,
    test_status ENUM('PASSED', 'FAILED', 'SKIPPED', 'ERROR') NOT NULL,
    test_datetime DATETIME NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields**:
- `id`: Unique identifier
- `test_case_name`: Name of the test function
- `module_name`: Name of the test file/module
- `test_status`: Test execution status
- `test_datetime`: When the test was executed
- `error_message`: Error details for failed tests
- `created_at`: Record creation timestamp

## 2. users Table

**Purpose**: Store user information and authentication data

```sql
CREATE TABLE users (
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
```

**Fields**:
- `id`: Unique user identifier
- `username`: Unique username for login
- `email`: Unique email address
- `password_hash`: Hashed password for security
- `first_name`, `last_name`: User's full name
- `university`: User's educational institution
- `user_type`: Role-based access control
- `is_active`: Account status
- `created_at`, `updated_at`: Timestamps

## 3. books Table

**Purpose**: Manage book catalog and inventory

```sql
CREATE TABLE books (
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
```

**Fields**:
- `id`: Unique book identifier
- `title`: Book title
- `author`: Book author
- `isbn`: International Standard Book Number
- `publisher`: Publishing company
- `publication_year`: Year of publication
- `price`: Book price
- `description`: Book description
- `cover_image_url`: Book cover image URL
- `category`: Book category/genre
- `is_available`: Inventory status
- `created_at`, `updated_at`: Timestamps

## 4. orders Table

**Purpose**: Track all orders and transactions

```sql
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    book_id INT,
    order_type ENUM('book_purchase', 'monthly_plan', 'six_month_plan', 'onetime_plan') NOT NULL,
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
```

**Fields**:
- `id`: Unique order identifier
- `order_number`: Human-readable order number
- `user_id`: Reference to user who placed order
- `book_id`: Reference to book (if applicable)
- `order_type`: Type of order/purchase
- `amount`: Order total amount
- `payment_method`: Payment method used
- `payment_status`: Payment processing status
- `order_status`: Order fulfillment status
- `billing_address`, `shipping_address`: Address information
- `order_date`, `completed_date`: Order timestamps

## 5. subscriptions Table

**Purpose**: Manage user subscriptions and recurring billing

```sql
CREATE TABLE subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    subscription_type ENUM('monthly', 'six_month', 'annual') NOT NULL,
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
```

**Fields**:
- `id`: Unique subscription identifier
- `user_id`: Reference to subscribed user
- `subscription_type`: Subscription plan type
- `status`: Current subscription status
- `start_date`, `end_date`: Subscription period
- `amount`: Subscription cost
- `auto_renew`: Automatic renewal setting
- `payment_method`: Payment method for billing
- `created_at`, `updated_at`: Timestamps

## Relationships

```
users (1) ←→ (many) orders
users (1) ←→ (many) subscriptions
books (1) ←→ (many) orders
```

## Indexes

Performance indexes have been created on:
- `users`: email, username
- `books`: isbn, category
- `orders`: user_id, order_number, order_date
- `subscriptions`: user_id, status
- `test_results`: test_datetime, test_status

## Usage Examples

### Create Tables
```bash
python create_tables.py
```

### View Database Summary
```bash
python manage_database.py summary
```

### View Table Data
```bash
python manage_database.py view users 10
python manage_database.py view books 5
```

### Search Data
```bash
python manage_database.py search books "computer"
python manage_database.py search users "john" email
```

### Insert Sample Data
```bash
python manage_database.py sample
```

## Sample Data

The system includes sample data for testing:

**Users**:
- john_doe (student)
- jane_smith (instructor)
- admin_user (admin)

**Books**:
- Introduction to Computer Science
- Advanced Mathematics
- Business Management

**Orders & Subscriptions**:
- Sample orders with different types
- Active subscriptions with various plans

## Database Management

### View All Tables
```bash
python manage_database.py tables
```

### Get Table Counts
```bash
python manage_database.py summary
```

### Search Functionality
```bash
# Search in all text columns
python manage_database.py search books "science"

# Search in specific column
python manage_database.py search users "john@example.com" email
```

## Security Considerations

1. **Password Hashing**: Passwords are stored as hashes, not plain text
2. **Foreign Keys**: Proper referential integrity with CASCADE/SET NULL
3. **Unique Constraints**: Username and email uniqueness enforced
4. **Enum Types**: Restricted values for status fields
5. **Timestamps**: Audit trail with created/updated timestamps

## Performance Optimizations

1. **Indexes**: Strategic indexes on frequently queried columns
2. **Data Types**: Appropriate data types for each field
3. **Constraints**: Database-level constraints for data integrity
4. **Foreign Keys**: Proper relationships for data consistency

## Backup and Maintenance

### Backup Database
```sql
mysqldump -h solutionsole.com -u root -p test > backup.sql
```

### Restore Database
```sql
mysql -h solutionsole.com -u root -p test < backup.sql
```

### Clean Old Data
```sql
-- Clean old test results (older than 30 days)
DELETE FROM test_results WHERE test_datetime < DATE_SUB(NOW(), INTERVAL 30 DAY);

-- Clean cancelled subscriptions
DELETE FROM subscriptions WHERE status = 'cancelled' AND end_date < CURDATE();
``` 
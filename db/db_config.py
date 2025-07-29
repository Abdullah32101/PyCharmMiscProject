import os
import socket
from typing import Dict, Any

def is_github_actions() -> bool:
    """Check if running in GitHub Actions environment"""
    return os.getenv('GITHUB_ACTIONS') == 'true'

def is_local_environment() -> bool:
    """Check if running in local development environment"""
    return not is_github_actions()

def can_connect_to_host(host: str, port: int, timeout: int = 10) -> bool:
    """Test if we can connect to a host:port with longer timeout"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def get_database_config() -> Dict[str, Any]:
    """Get database configuration based on environment"""
    
    # Check if we're in GitHub Actions
    if is_github_actions():
        print("Detected GitHub Actions environment")
        
        # For GitHub Actions, try multiple database options
        database_options = [
            # Option 1: Remote database (primary)
            {
                "name": "Remote Database (18.235.51.183)",
                "config": {
                    "host": "18.235.51.183",
                    "user": "sqa_user",
                    "password": "Hassan123!@#",
                    "database": "solutioninn_testing",
                    "port": 3306,
                    "autocommit": True,
                    "charset": "utf8mb4"
                }
            },
            # Option 2: Alternative remote database
            {
                "name": "Alternative Remote Database (solutionsole.com)",
                "config": {
                    "host": "solutionsole.com",
                    "user": "root",
                    "password": "SolutionInn321",
                    "database": "test",
                    "port": 3306,
                    "autocommit": True,
                    "charset": "utf8mb4"
                }
            },
            # Option 3: Local test database (fallback)
            {
                "name": "Local Test Database",
                "config": {
                    "host": os.getenv("TEST_DB_HOST", "127.0.0.1"),
                    "user": os.getenv("TEST_DB_USER", "root"),
                    "password": os.getenv("TEST_DB_PASSWORD", "root"),
                    "database": os.getenv("TEST_DB_NAME", "test_results"),
                    "port": int(os.getenv("TEST_DB_PORT", "3306")),
                    "autocommit": True,
                    "charset": "utf8mb4"
                }
            }
        ]
        
        # Try each database option
        for option in database_options:
            print(f"Testing connection to: {option['name']}")
            host = option['config']['host']
            port = option['config']['port']
            
            if can_connect_to_host(host, port):
                print(f"SUCCESS: {option['name']} is accessible")
                return option['config']
            else:
                print(f"FAILED: {option['name']} is not accessible")
        
        # If none work, use the local test database as final fallback
        print("WARNING: No remote databases accessible, using local test database")
        return {
            "host": "127.0.0.1",
            "user": "root",
            "password": "root",
            "database": "test_results",
            "port": 3306,
            "autocommit": True,
            "charset": "utf8mb4"
        }
    
    # Local development environment
    else:
        print("Detected local development environment")
        
        # Try remote database first
        if can_connect_to_host("18.235.51.183", 3306):
            print("SUCCESS: Using remote database for local development")
            return {
                "host": "18.235.51.183",
                "user": "sqa_user",
                "password": "Hassan123!@#",
                "database": "solutioninn_testing",
                "port": 3306,
                "autocommit": True,
                "charset": "utf8mb4"
            }
        else:
            print("WARNING: Remote database not accessible locally")
            print("Using local database configuration")
            
            # Fallback to local database
            return {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "test_results",
                "port": 3306,
                "autocommit": True,
                "charset": "utf8mb4"
            }

# Legacy support - keep the old DB_CONFIG for backward compatibility
DB_CONFIG = get_database_config()

# Export the function for use in other modules
__all__ = ['DB_CONFIG', 'get_database_config', 'is_github_actions', 'is_local_environment']

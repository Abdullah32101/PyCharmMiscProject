import os
import socket
from typing import Dict, Any

def is_github_actions() -> bool:
    """Check if running in GitHub Actions environment"""
    return os.getenv('GITHUB_ACTIONS') == 'true'

def is_local_environment() -> bool:
    """Check if running in local development environment"""
    return not is_github_actions()

def can_connect_to_host(host: str, port: int, timeout: int = 5) -> bool:
    """Test if we can connect to a host:port"""
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
        print("🔧 Detected GitHub Actions environment")
        
        # Try to connect to the remote database first
        if can_connect_to_host("18.235.51.183", 3306):
            print("✅ Remote database is accessible from GitHub Actions")
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
            print("⚠️ Remote database not accessible from GitHub Actions")
            print("🔧 Using local test configuration")
            
            # Use environment variables for local test database
            return {
                "host": os.getenv("TEST_DB_HOST", "localhost"),
                "user": os.getenv("TEST_DB_USER", "root"),
                "password": os.getenv("TEST_DB_PASSWORD", ""),
                "database": os.getenv("TEST_DB_NAME", "test_results"),
                "port": int(os.getenv("TEST_DB_PORT", "3306")),
                "autocommit": True,
                "charset": "utf8mb4"
            }
    
    # Local development environment
    else:
        print("🔧 Detected local development environment")
        
        # Try remote database first
        if can_connect_to_host("18.235.51.183", 3306):
            print("✅ Using remote database for local development")
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
            print("⚠️ Remote database not accessible locally")
            print("🔧 Using local database configuration")
            
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

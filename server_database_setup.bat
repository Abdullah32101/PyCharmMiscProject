@echo off
REM Server Database Setup Instructions for Windows
REM This file contains instructions to set up your solutionsole.com server database

echo.
echo ========================================
echo   Server Database Setup Instructions
echo ========================================
echo Target Server: solutionsole.com
echo Date: %date% %time%
echo.

echo [INFO] This script provides instructions to set up your server database
echo [INFO] You need to SSH into your solutionsole.com server and run the commands
echo.

echo ========================================
echo   STEP 1: SSH into your server
echo ========================================
echo Command: ssh your-username@solutionsole.com
echo.

echo ========================================
echo   STEP 2: Download and run setup script
echo ========================================
echo 1. Copy the server_database_setup.sh file to your server
echo 2. Make it executable: chmod +x server_database_setup.sh
echo 3. Run it: ./server_database_setup.sh
echo.

echo ========================================
echo   STEP 3: Manual commands (if needed)
echo ========================================
echo If the script fails, run these commands manually:
echo.
echo 1. Check MySQL status:
echo    sudo systemctl status mysql
echo.
echo 2. Edit MySQL configuration:
echo    sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
echo    Change: bind-address = 0.0.0.0
echo.
echo 3. Restart MySQL:
echo    sudo systemctl restart mysql
echo.
echo 4. Connect to MySQL and update permissions:
echo    mysql -u root -p
echo    GRANT ALL PRIVILEGES ON test.* TO 'root'@'%%' IDENTIFIED BY 'SolutionInn321';
echo    FLUSH PRIVILEGES;
echo    EXIT;
echo.
echo 5. Check firewall:
echo    sudo ufw status
echo    sudo ufw allow 3306
echo.

echo ========================================
echo   STEP 4: Test the connection
echo ========================================
echo Test local connection:
echo mysql -u root -p -h localhost test
echo.
echo Test external connection:
echo mysql -u root -p'SolutionInn321' -h localhost test
echo.

echo ========================================
echo   STEP 5: Verify GitHub Actions access
echo ========================================
echo After completing the server setup:
echo 1. Go to your GitHub repository
echo 2. Run the scheduled test workflow manually
echo 3. Check if database connection succeeds
echo.

echo [SUCCESS] Instructions completed!
echo [INFO] Please follow these steps on your solutionsole.com server
echo.
pause 
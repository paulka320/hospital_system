@echo off
REM Hospital Management System - Setup Script for Windows

echo ================================
echo Hospital Management System Setup
echo ================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel > nul 2>&1
echo pip upgraded
echo.

REM Install requirements
echo Installing Python packages...
pip install -r requirements.txt > nul 2>&1
echo Python packages installed
echo.

REM Create .env file
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created (please update with your settings)
) else (
    echo .env file already exists
)
echo.

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo Migrations completed
echo.

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput > nul 2>&1
echo Static files collected
echo.

REM Create superuser
setlocal enabledelayedexpansion
set /p create_superuser="Create superuser? (y/n): "
if /i "!create_superuser!"=="y" (
    python manage.py createsuperuser
)
echo.

REM Load sample data
set /p load_data="Load sample data? (y/n): "
if /i "!load_data!"=="y" (
    python manage.py loaddata fixtures\sample_data.json
)
echo.

echo ================================
echo Setup completed successfully!
echo ================================
echo.
echo Next steps:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Update .env file with your configuration
echo 3. Run development server: python manage.py runserver
echo 4. Visit http://localhost:8000 in your browser
echo 5. Admin panel: http://localhost:8000/admin
echo.
pause

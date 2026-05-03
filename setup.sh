#!/bin/bash

# Hospital Management System - Setup Script
# This script automates the setup process

set -e

echo "================================"
echo "Hospital Management System Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1)
echo "Found: $python_version"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Python packages installed"
echo ""

# Create .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created (please update with your settings)"
else
    echo "✓ .env file already exists"
fi
echo ""

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo "✓ Migrations completed"
echo ""

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1
echo "✓ Static files collected"
echo ""

# Create superuser
read -p "Create superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi
echo ""

# Load sample data
read -p "Load sample data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py loaddata fixtures/sample_data.json 2>/dev/null && echo "✓ Sample data loaded" || echo "✗ Sample data not found"
fi
echo ""

echo "================================"
echo "Setup completed successfully!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Update .env file with your configuration"
echo "3. Run development server: python manage.py runserver"
echo "4. Visit http://localhost:8000 in your browser"
echo "5. Admin panel: http://localhost:8000/admin"
echo ""

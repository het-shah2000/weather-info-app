#!/bin/bash

# Weather Backend Service Setup Script
# This script sets up the development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Setup virtual environment
setup_venv() {
    print_status "Setting up Python virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_status "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    print_status "Dependencies installed"
}

# Create .env file from example
setup_env() {
    print_status "Setting up environment file..."
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        print_warning "Created .env file from .env.example"
        print_warning "Please update .env with your actual values"
    else
        print_status ".env file already exists"
    fi
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    source venv/bin/activate
    python -m pytest tests/ -v
    
    print_status "Tests completed"
}

# Main setup function
main() {
    print_status "Setting up Weather Backend Service development environment..."
    
    setup_venv
    setup_env
    run_tests
    
    print_status "Setup completed successfully! 🎉"
    print_status "To activate the virtual environment, run: source venv/bin/activate"
    print_status "To start the application, run: python app.py"
}

main "$@"

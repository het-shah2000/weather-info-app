#!/usr/bin/env python3
"""
Entry point for Weather Backend Service
This file is kept for backward compatibility and easy deployment
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import after path setup
from src.app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

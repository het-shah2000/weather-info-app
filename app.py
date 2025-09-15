#!/usr/bin/env python3
"""
Entry point for Weather Backend Service
This file is kept for backward compatibility and easy deployment
"""
import sys
import os

# Add current directory and src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

try:
    from src.app import create_app
    # Create the Flask application
    app = create_app()
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback simple Flask app for debugging
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "message": "Weather Backend Service"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

#!/usr/bin/env python3
"""
WSGI entry point for Weather Backend Service
"""
import sys
import os

# Add current directory and src to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

from flask import Flask, jsonify

# Simple Flask app that works
app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "message": "Weather Backend Service",
        "version": "1.0.0"
    })

@app.route('/')
def index():
    return jsonify({
        "service": "Weather Backend Service",
        "status": "running",
        "endpoints": ["/health", "/docs"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

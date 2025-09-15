#!/usr/bin/env python3
"""
Test script for the Weather Backend Service API
"""

import requests
import json
import time
import sys
import os

# Add src directory to Python path for local testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configuration
BASE_URL = "http://localhost:8080"  # Change this to your deployed URL when testing production

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_store_weather_data():
    """Test storing weather data"""
    print("\nTesting store weather data...")
    
    test_data = {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "start_date": "2023-01-01",
        "end_date": "2023-01-07"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/store-weather-data",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            return response.json().get('filename')
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_list_weather_files():
    """Test listing weather files"""
    print("\nTesting list weather files...")
    try:
        response = requests.get(f"{BASE_URL}/list-weather-files")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Files count: {result.get('count', 0)}")
        
        if result.get('files'):
            print("Files:")
            for file_info in result['files'][:3]:  # Show first 3 files
                print(f"  - {file_info['filename']} ({file_info['size']} bytes)")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_weather_file_content(filename):
    """Test getting weather file content"""
    if not filename:
        print("\nSkipping file content test - no filename provided")
        return False
        
    print(f"\nTesting get weather file content for: {filename}")
    try:
        response = requests.get(f"{BASE_URL}/weather-file-content/{filename}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Latitude: {data.get('latitude')}")
            print(f"Longitude: {data.get('longitude')}")
            print(f"Timezone: {data.get('timezone')}")
            
            if 'daily' in data and 'time' in data['daily']:
                print(f"Date range: {data['daily']['time'][0]} to {data['daily']['time'][-1]}")
                print(f"Data points: {len(data['daily']['time'])}")
            
            return True
        else:
            print(f"Response: {response.json()}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_error_cases():
    """Test various error cases"""
    print("\nTesting error cases...")
    
    # Test invalid latitude
    print("Testing invalid latitude...")
    response = requests.post(
        f"{BASE_URL}/store-weather-data",
        json={
            "latitude": 91,  # Invalid
            "longitude": -74.0060,
            "start_date": "2023-01-01",
            "end_date": "2023-01-07"
        }
    )
    print(f"Invalid latitude - Status: {response.status_code}, Response: {response.json()}")
    
    # Test missing fields
    print("Testing missing fields...")
    response = requests.post(
        f"{BASE_URL}/store-weather-data",
        json={"latitude": 40.7128}  # Missing other fields
    )
    print(f"Missing fields - Status: {response.status_code}, Response: {response.json()}")
    
    # Test invalid date format
    print("Testing invalid date format...")
    response = requests.post(
        f"{BASE_URL}/store-weather-data",
        json={
            "latitude": 40.7128,
            "longitude": -74.0060,
            "start_date": "2023-13-01",  # Invalid month
            "end_date": "2023-01-07"
        }
    )
    print(f"Invalid date - Status: {response.status_code}, Response: {response.json()}")
    
    # Test non-existent file
    print("Testing non-existent file...")
    response = requests.get(f"{BASE_URL}/weather-file-content/non-existent-file.json")
    print(f"Non-existent file - Status: {response.status_code}, Response: {response.json()}")

def main():
    """Run all tests"""
    print("=" * 50)
    print("Weather Backend Service API Tests")
    print("=" * 50)
    
    # Test health check first
    if not test_health_check():
        print("Health check failed. Make sure the service is running.")
        return
    
    # Test storing weather data
    filename = test_store_weather_data()
    
    # Wait a moment for the file to be processed
    if filename:
        print("Waiting 2 seconds for file processing...")
        time.sleep(2)
    
    # Test listing files
    test_list_weather_files()
    
    # Test getting file content
    test_get_weather_file_content(filename)
    
    # Test error cases
    test_error_cases()
    
    print("\n" + "=" * 50)
    print("Tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()

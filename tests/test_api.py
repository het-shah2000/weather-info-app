"""
Integration tests for Weather Backend Service API
"""
import unittest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.app import create_app


class TestWeatherAPI(unittest.TestCase):
    """Test cases for Weather API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
    
    @patch('src.api.routes.get_weather_service')
    @patch('src.api.routes.get_storage_service')
    def test_store_weather_data_success(self, mock_get_storage, mock_get_weather):
        """Test successful weather data storage"""
        # Mock services
        mock_weather_service = MagicMock()
        mock_storage_service = MagicMock()
        mock_get_weather.return_value = mock_weather_service
        mock_get_storage.return_value = mock_storage_service
        
        # Mock responses
        mock_weather_service.fetch_weather_data.return_value = {'test': 'data'}
        mock_storage_service.store_weather_data.return_value = 'test_file.json'
        mock_storage_service.bucket_name = 'test-bucket'
        
        data = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "start_date": "2023-01-01",
            "end_date": "2023-01-31"
        }
        
        response = self.client.post('/store-weather-data',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('message', response_data)
        self.assertIn('filename', response_data)
    
    def test_store_weather_data_invalid_latitude(self):
        """Test weather data storage with invalid latitude"""
        data = {
            "latitude": 91.0,  # Invalid
            "longitude": -74.0060,
            "start_date": "2023-01-01",
            "end_date": "2023-01-31"
        }
        
        response = self.client.post('/store-weather-data',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
    
    def test_store_weather_data_missing_field(self):
        """Test weather data storage with missing field"""
        data = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "start_date": "2023-01-01"
            # Missing end_date
        }
        
        response = self.client.post('/store-weather-data',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
    
    @patch('src.api.routes.get_storage_service')
    def test_list_weather_files(self, mock_get_storage):
        """Test listing weather files"""
        mock_storage_service = MagicMock()
        mock_get_storage.return_value = mock_storage_service
        mock_storage_service.list_weather_files.return_value = [
            {
                'filename': 'test_file.json',
                'size': 1024,
                'created': '2023-01-01T00:00:00Z',
                'updated': '2023-01-01T00:00:00Z'
            }
        ]
        
        response = self.client.get('/list-weather-files')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('files', data)
        self.assertIn('count', data)
        self.assertEqual(data['count'], 1)
    
    @patch('src.api.routes.get_storage_service')
    def test_get_weather_file_content_success(self, mock_get_storage):
        """Test successful file content retrieval"""
        mock_storage_service = MagicMock()
        mock_get_storage.return_value = mock_storage_service
        mock_storage_service.get_weather_file_content.return_value = {'test': 'weather_data'}
        
        response = self.client.get('/weather-file-content/test_file.json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['test'], 'weather_data')
    
    @patch('src.api.routes.get_storage_service')
    def test_get_weather_file_content_not_found(self, mock_get_storage):
        """Test file content retrieval for non-existent file"""
        mock_storage_service = MagicMock()
        mock_get_storage.return_value = mock_storage_service
        mock_storage_service.get_weather_file_content.side_effect = Exception("File 'test_file.json' not found")
        
        response = self.client.get('/weather-file-content/test_file.json')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()

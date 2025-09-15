"""
Unit tests for validation utilities
"""
import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.utils.validators import (
    validate_coordinates,
    validate_date_format,
    validate_date_range,
    validate_weather_request
)


class TestValidators(unittest.TestCase):
    """Test cases for validation functions"""
    
    def test_validate_coordinates_valid(self):
        """Test valid coordinates"""
        is_valid, error = validate_coordinates(40.7128, -74.0060)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_coordinates_invalid_latitude(self):
        """Test invalid latitude"""
        is_valid, error = validate_coordinates(91.0, -74.0060)
        self.assertFalse(is_valid)
        self.assertIn("Latitude must be between", error)
    
    def test_validate_coordinates_invalid_longitude(self):
        """Test invalid longitude"""
        is_valid, error = validate_coordinates(40.7128, 181.0)
        self.assertFalse(is_valid)
        self.assertIn("Longitude must be between", error)
    
    def test_validate_coordinates_invalid_type(self):
        """Test invalid coordinate types"""
        is_valid, error = validate_coordinates("invalid", -74.0060)
        self.assertFalse(is_valid)
        self.assertIn("must be valid numbers", error)
    
    def test_validate_date_format_valid(self):
        """Test valid date format"""
        result = validate_date_format("2023-01-01")
        self.assertEqual(result, "2023-01-01")
    
    def test_validate_date_format_invalid(self):
        """Test invalid date format"""
        result = validate_date_format("2023-13-01")
        self.assertIsNone(result)
    
    def test_validate_date_range_valid(self):
        """Test valid date range"""
        is_valid, error = validate_date_range("2023-01-01", "2023-01-31")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    def test_validate_date_range_invalid_order(self):
        """Test invalid date range order"""
        is_valid, error = validate_date_range("2023-01-31", "2023-01-01")
        self.assertFalse(is_valid)
        self.assertIn("Start date must be before", error)
    
    def test_validate_weather_request_valid(self):
        """Test valid weather request"""
        data = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "start_date": "2023-01-01",
            "end_date": "2023-01-31"
        }
        is_valid, error, normalized = validate_weather_request(data)
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        self.assertIsNotNone(normalized)
    
    def test_validate_weather_request_missing_field(self):
        """Test weather request with missing field"""
        data = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "start_date": "2023-01-01"
            # Missing end_date
        }
        is_valid, error, normalized = validate_weather_request(data)
        self.assertFalse(is_valid)
        self.assertIn("Missing required field", error)
        self.assertIsNone(normalized)


if __name__ == '__main__':
    unittest.main()

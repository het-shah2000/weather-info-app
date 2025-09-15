"""
Input validation utilities for Weather Backend Service
"""
from typing import Optional, Tuple
from dateutil.parser import parse as parse_date
from src.config import Config


def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, Optional[str]]:
    """
    Validate latitude and longitude coordinates
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        lat = float(latitude)
        lon = float(longitude)
        
        if not (Config.MIN_LATITUDE <= lat <= Config.MAX_LATITUDE):
            return False, f"Latitude must be between {Config.MIN_LATITUDE} and {Config.MAX_LATITUDE}"
        
        if not (Config.MIN_LONGITUDE <= lon <= Config.MAX_LONGITUDE):
            return False, f"Longitude must be between {Config.MIN_LONGITUDE} and {Config.MAX_LONGITUDE}"
        
        return True, None
        
    except (ValueError, TypeError):
        return False, "Latitude and longitude must be valid numbers"


def validate_date_format(date_string: str) -> Optional[str]:
    """
    Validate and normalize date format to YYYY-MM-DD
    
    Args:
        date_string: Date string to validate
        
    Returns:
        Normalized date string or None if invalid
    """
    try:
        parsed_date = parse_date(date_string)
        return parsed_date.strftime('%Y-%m-%d')
    except:
        return None


def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, Optional[str]]:
    """
    Validate date range
    
    Args:
        start_date: Start date string
        end_date: End date string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    start_normalized = validate_date_format(start_date)
    end_normalized = validate_date_format(end_date)
    
    if not start_normalized:
        return False, "Start date must be in YYYY-MM-DD format"
    
    if not end_normalized:
        return False, "End date must be in YYYY-MM-DD format"
    
    if start_normalized > end_normalized:
        return False, "Start date must be before or equal to end date"
    
    return True, None


def validate_weather_request(data: dict) -> Tuple[bool, Optional[str], Optional[dict]]:
    """
    Validate complete weather data request
    
    Args:
        data: Request data dictionary
        
    Returns:
        Tuple of (is_valid, error_message, normalized_data)
    """
    if not data:
        return False, "No JSON data provided", None
    
    required_fields = ['latitude', 'longitude', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}", None
    
    # Validate coordinates
    is_valid, error = validate_coordinates(data['latitude'], data['longitude'])
    if not is_valid:
        return False, error, None
    
    # Validate date range
    is_valid, error = validate_date_range(data['start_date'], data['end_date'])
    if not is_valid:
        return False, error, None
    
    # Normalize data
    normalized_data = {
        'latitude': float(data['latitude']),
        'longitude': float(data['longitude']),
        'start_date': validate_date_format(data['start_date']),
        'end_date': validate_date_format(data['end_date'])
    }
    
    return True, None, normalized_data

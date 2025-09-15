"""
Configuration management for Weather Backend Service
"""
import os
from typing import Optional


class Config:
    """Base configuration class"""
    
    # Google Cloud Storage
    GCS_BUCKET_NAME: str = os.environ.get('GCS_BUCKET_NAME', 'weather-data-bucket')
    GOOGLE_CLOUD_PROJECT: Optional[str] = os.environ.get('GOOGLE_CLOUD_PROJECT')
    
    # Flask settings
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG: bool = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Server settings
    HOST: str = os.environ.get('HOST', '0.0.0.0')
    PORT: int = int(os.environ.get('PORT', 8080))
    
    # API settings
    OPEN_METEO_BASE_URL: str = "https://archive-api.open-meteo.com/v1/archive"
    REQUEST_TIMEOUT: int = int(os.environ.get('REQUEST_TIMEOUT', 30))
    
    # Weather data variables
    WEATHER_VARIABLES = [
        'temperature_2m_max',
        'temperature_2m_min', 
        'temperature_2m_mean',
        'apparent_temperature_max',
        'apparent_temperature_min',
        'apparent_temperature_mean'
    ]
    
    # File naming
    FILENAME_TEMPLATE = "weather_data_lat{latitude}_lon{longitude}_{start_date}_to_{end_date}_{timestamp}.json"
    
    # Validation limits
    MIN_LATITUDE = -90.0
    MAX_LATITUDE = 90.0
    MIN_LONGITUDE = -180.0
    MAX_LONGITUDE = 180.0


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    USE_MOCK_STORAGE = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    GCS_BUCKET_NAME = 'test-weather-data-bucket'


# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

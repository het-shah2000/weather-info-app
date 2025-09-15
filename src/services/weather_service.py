"""
Weather data service for fetching data from Open-Meteo API
"""
import requests
from typing import Dict, Any
from src.config import Config
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class WeatherService:
    """Service for interacting with Open-Meteo API"""
    
    def __init__(self):
        self.base_url = Config.OPEN_METEO_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        self.weather_variables = Config.WEATHER_VARIABLES
    
    def fetch_weather_data(self, latitude: float, longitude: float, 
                          start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Fetch weather data from Open-Meteo API
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Weather data dictionary
            
        Raises:
            Exception: If API request fails
        """
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date,
            'end_date': end_date,
            'daily': self.weather_variables,
            'timezone': 'UTC'
        }
        
        logger.info(f"Fetching weather data for coordinates ({latitude}, {longitude}) "
                   f"from {start_date} to {end_date}")
        
        try:
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully fetched weather data with {len(data.get('daily', {}).get('time', []))} data points")
            
            return data
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout after {self.timeout} seconds")
            raise Exception("Request timeout - the weather service is taking too long to respond")
        
        except requests.exceptions.ConnectionError:
            logger.error("Connection error to Open-Meteo API")
            raise Exception("Unable to connect to weather service")
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error from Open-Meteo API: {e}")
            if response.status_code == 400:
                raise Exception("Invalid request parameters for weather data")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded for weather service")
            else:
                raise Exception(f"Weather service error: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {e}")
            raise Exception(f"Failed to fetch weather data: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception(f"Unexpected error while fetching weather data: {str(e)}")

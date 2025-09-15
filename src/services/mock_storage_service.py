"""
Mock storage service for local development and testing
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from src.config import Config
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class MockStorageService:
    """Mock storage service that uses local filesystem instead of GCS"""
    
    def __init__(self):
        self.bucket_name = Config.GCS_BUCKET_NAME
        self.filename_template = Config.FILENAME_TEMPLATE
        self.local_storage_dir = "local_weather_data"
        
        # Create local storage directory
        if not os.path.exists(self.local_storage_dir):
            os.makedirs(self.local_storage_dir)
            logger.info(f"Created local storage directory: {self.local_storage_dir}")
    
    def generate_filename(self, latitude: float, longitude: float, 
                         start_date: str, end_date: str) -> str:
        """Generate a unique filename for weather data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.filename_template.format(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            timestamp=timestamp
        )
        logger.debug(f"Generated filename: {filename}")
        return filename
    
    def store_weather_data(self, weather_data: Dict[str, Any], 
                          latitude: float, longitude: float,
                          start_date: str, end_date: str) -> str:
        """Store weather data as JSON file locally"""
        filename = self.generate_filename(latitude, longitude, start_date, end_date)
        
        try:
            file_path = os.path.join(self.local_storage_dir, filename)
            
            # Convert to JSON string with proper formatting
            json_data = json.dumps(weather_data, indent=2, ensure_ascii=False)
            
            # Write to local file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_data)
            
            logger.info(f"Successfully stored weather data in local file: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error storing file locally: {e}")
            raise Exception(f"Failed to store weather data locally: {str(e)}")
    
    def list_weather_files(self) -> List[Dict[str, Any]]:
        """List all weather data files in the local directory"""
        try:
            files = []
            
            if not os.path.exists(self.local_storage_dir):
                return files
            
            for filename in os.listdir(self.local_storage_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.local_storage_dir, filename)
                    stat = os.stat(file_path)
                    
                    file_info = {
                        'filename': filename,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        'updated': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'content_type': 'application/json'
                    }
                    files.append(file_info)
            
            logger.info(f"Listed {len(files)} files from local storage")
            return files
            
        except Exception as e:
            logger.error(f"Error listing local files: {e}")
            raise Exception(f"Failed to list weather files: {str(e)}")
    
    def get_weather_file_content(self, filename: str) -> Dict[str, Any]:
        """Get content of a specific weather data file"""
        try:
            file_path = os.path.join(self.local_storage_dir, filename)
            
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {filename}")
                raise Exception(f"File '{filename}' not found")
            
            # Read and parse JSON content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            weather_data = json.loads(content)
            
            logger.info(f"Successfully retrieved content for local file: {filename}")
            return weather_data
            
        except FileNotFoundError:
            logger.warning(f"File not found: {filename}")
            raise Exception(f"File '{filename}' not found")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {filename}: {e}")
            raise Exception(f"File '{filename}' contains invalid JSON data")
        except Exception as e:
            logger.error(f"Error retrieving local file: {e}")
            raise Exception(f"Failed to retrieve weather file: {str(e)}")
    
    def file_exists(self, filename: str) -> bool:
        """Check if a file exists in local storage"""
        try:
            file_path = os.path.join(self.local_storage_dir, filename)
            return os.path.exists(file_path)
        except Exception as e:
            logger.error(f"Error checking file existence: {e}")
            return False

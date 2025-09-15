"""
Google Cloud Storage service for managing weather data files
"""
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from google.cloud import storage
from google.cloud.exceptions import NotFound, GoogleCloudError
from src.config import Config
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


class StorageService:
    """Service for interacting with Google Cloud Storage"""
    
    def __init__(self, client=None):
        try:
            self.client = client or storage.Client()
        except Exception as e:
            logger.warning(f"Failed to initialize GCS client: {e}")
            self.client = None
        self.bucket_name = Config.GCS_BUCKET_NAME
        self.filename_template = Config.FILENAME_TEMPLATE
        self._bucket = None
    
    def get_bucket(self) -> storage.Bucket:
        """
        Get or create the GCS bucket
        
        Returns:
            GCS bucket instance
            
        Raises:
            Exception: If bucket operations fail
        """
        if self._bucket is None:
            try:
                self._bucket = self.client.bucket(self.bucket_name)
                
                # Check if bucket exists, create if it doesn't
                if not self._bucket.exists():
                    logger.info(f"Creating bucket: {self.bucket_name}")
                    self._bucket = self.client.create_bucket(self.bucket_name)
                    logger.info(f"Successfully created bucket: {self.bucket_name}")
                else:
                    logger.debug(f"Using existing bucket: {self.bucket_name}")
                    
            except GoogleCloudError as e:
                logger.error(f"Google Cloud error accessing bucket: {e}")
                raise Exception(f"Failed to access Google Cloud Storage bucket: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error accessing bucket: {e}")
                raise Exception(f"Failed to access storage bucket: {str(e)}")
        
        return self._bucket
    
    def generate_filename(self, latitude: float, longitude: float, 
                         start_date: str, end_date: str) -> str:
        """
        Generate a unique filename for weather data
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            start_date: Start date
            end_date: End date
            
        Returns:
            Generated filename
        """
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
        """
        Store weather data as JSON file in GCS
        
        Args:
            weather_data: Weather data dictionary
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            start_date: Start date
            end_date: End date
            
        Returns:
            Filename of stored file
            
        Raises:
            Exception: If storage operation fails
        """
        filename = self.generate_filename(latitude, longitude, start_date, end_date)
        
        try:
            bucket = self.get_bucket()
            blob = bucket.blob(filename)
            
            # Convert to JSON string with proper formatting
            json_data = json.dumps(weather_data, indent=2, ensure_ascii=False)
            
            # Upload to GCS
            blob.upload_from_string(
                json_data,
                content_type='application/json'
            )
            
            logger.info(f"Successfully stored weather data in file: {filename}")
            return filename
            
        except GoogleCloudError as e:
            logger.error(f"Google Cloud error storing file: {e}")
            raise Exception(f"Failed to store weather data in cloud storage: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error storing file: {e}")
            raise Exception(f"Failed to store weather data: {str(e)}")
    
    def list_weather_files(self) -> List[Dict[str, Any]]:
        """
        List all weather data files in the bucket
        
        Returns:
            List of file information dictionaries
            
        Raises:
            Exception: If listing operation fails
        """
        try:
            bucket = self.get_bucket()
            blobs = bucket.list_blobs()
            
            files = []
            for blob in blobs:
                file_info = {
                    'filename': blob.name,
                    'size': blob.size,
                    'created': blob.time_created.isoformat() if blob.time_created else None,
                    'updated': blob.updated.isoformat() if blob.updated else None,
                    'content_type': blob.content_type
                }
                files.append(file_info)
            
            logger.info(f"Listed {len(files)} files from bucket")
            return files
            
        except GoogleCloudError as e:
            logger.error(f"Google Cloud error listing files: {e}")
            raise Exception(f"Failed to list files from cloud storage: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error listing files: {e}")
            raise Exception(f"Failed to list weather files: {str(e)}")
    
    def get_weather_file_content(self, filename: str) -> Dict[str, Any]:
        """
        Get content of a specific weather data file
        
        Args:
            filename: Name of the file to retrieve
            
        Returns:
            Weather data dictionary
            
        Raises:
            Exception: If file not found or retrieval fails
        """
        try:
            bucket = self.get_bucket()
            blob = bucket.blob(filename)
            
            if not blob.exists():
                logger.warning(f"File not found: {filename}")
                raise Exception(f"File '{filename}' not found")
            
            # Download and parse JSON content
            content = blob.download_as_text()
            weather_data = json.loads(content)
            
            logger.info(f"Successfully retrieved content for file: {filename}")
            return weather_data
            
        except NotFound:
            logger.warning(f"File not found: {filename}")
            raise Exception(f"File '{filename}' not found")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {filename}: {e}")
            raise Exception(f"File '{filename}' contains invalid JSON data")
        except GoogleCloudError as e:
            logger.error(f"Google Cloud error retrieving file: {e}")
            raise Exception(f"Failed to retrieve file from cloud storage: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error retrieving file: {e}")
            raise Exception(f"Failed to retrieve weather file: {str(e)}")
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if a file exists in the bucket
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            bucket = self.get_bucket()
            blob = bucket.blob(filename)
            return blob.exists()
        except Exception as e:
            logger.error(f"Error checking file existence: {e}")
            return False

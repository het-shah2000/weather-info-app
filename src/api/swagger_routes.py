"""
API routes with Swagger documentation using Flask-RESTX
"""
from flask import request
from flask_restx import Api, Resource, fields, Namespace
from src.services.weather_service import WeatherService
from src.services.storage_service import StorageService
from src.services.mock_storage_service import MockStorageService
from src.utils.validators import validate_weather_request
from src.utils.logging_config import get_logger
from src.config import config
import os

logger = get_logger(__name__)

# Create API instance
api = Api(
    version='1.0',
    title='Weather Backend Service API',
    description='A Flask-based backend service that fetches historical weather data from Open-Meteo API and stores it in Google Cloud Storage',
    doc='/docs/',
    prefix='/api/v1'
)

# Create namespace
weather_ns = Namespace('weather', description='Weather data operations')
api.add_namespace(weather_ns)

# Initialize services
weather_service = None
storage_service = None

def get_weather_service():
    global weather_service
    if weather_service is None:
        weather_service = WeatherService()
    return weather_service

def get_storage_service():
    global storage_service
    if storage_service is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
        app_config = config[config_name]
        
        if hasattr(app_config, 'USE_MOCK_STORAGE') and app_config.USE_MOCK_STORAGE:
            logger.info("Using mock storage service for local development")
            storage_service = MockStorageService()
        else:
            logger.info("Using Google Cloud Storage service")
            storage_service = StorageService()
    return storage_service

# Request/Response models
weather_request_model = api.model('WeatherRequest', {
    'latitude': fields.Float(required=True, description='Latitude coordinate (-90 to 90)', example=40.7128),
    'longitude': fields.Float(required=True, description='Longitude coordinate (-180 to 180)', example=-74.0060),
    'start_date': fields.String(required=True, description='Start date in YYYY-MM-DD format', example='2023-01-01'),
    'end_date': fields.String(required=True, description='End date in YYYY-MM-DD format', example='2023-01-31')
})

weather_response_model = api.model('WeatherResponse', {
    'message': fields.String(description='Success message'),
    'filename': fields.String(description='Generated filename for stored data'),
    'location': fields.String(description='GCS location of stored file')
})

file_info_model = api.model('FileInfo', {
    'filename': fields.String(description='Name of the file'),
    'size': fields.Integer(description='File size in bytes'),
    'created': fields.String(description='Creation timestamp'),
    'updated': fields.String(description='Last update timestamp'),
    'content_type': fields.String(description='MIME type of the file')
})

files_list_model = api.model('FilesList', {
    'files': fields.List(fields.Nested(file_info_model), description='List of weather data files'),
    'count': fields.Integer(description='Total number of files')
})

error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})

health_model = api.model('Health', {
    'status': fields.String(description='Service status'),
    'timestamp': fields.String(description='Current timestamp'),
    'service': fields.String(description='Service name'),
    'version': fields.String(description='Service version')
})

@weather_ns.route('/store-weather-data')
class StoreWeatherData(Resource):
    @weather_ns.expect(weather_request_model)
    @weather_ns.marshal_with(weather_response_model, code=201)
    @weather_ns.response(400, 'Bad Request', error_model)
    @weather_ns.response(500, 'Internal Server Error', error_model)
    @weather_ns.doc('store_weather_data')
    def post(self):
        """
        Store weather data
        
        Fetches historical weather data from Open-Meteo API for the specified coordinates and date range,
        then stores the results as a JSON file in Google Cloud Storage.
        
        Weather Variables Fetched:
        - Maximum Temperature (2m)
        - Minimum Temperature (2m) 
        - Mean Temperature (2m)
        - Maximum Apparent Temperature (2m)
        - Minimum Apparent Temperature (2m)
        - Mean Apparent Temperature (2m)
        """
        try:
            data = request.get_json()
            is_valid, error_message, normalized_data = validate_weather_request(data)
            
            if not is_valid:
                logger.warning(f"Invalid request: {error_message}")
                return {'error': error_message}, 400
            
            # Fetch weather data
            weather_data = get_weather_service().fetch_weather_data(
                normalized_data['latitude'],
                normalized_data['longitude'],
                normalized_data['start_date'],
                normalized_data['end_date']
            )
            
            # Store in storage
            filename = get_storage_service().store_weather_data(
                weather_data,
                normalized_data['latitude'],
                normalized_data['longitude'],
                normalized_data['start_date'],
                normalized_data['end_date']
            )
            
            response_data = {
                'message': 'Weather data stored successfully',
                'filename': filename,
                'location': f'gs://{get_storage_service().bucket_name}/{filename}'
            }
            
            logger.info(f"Successfully processed weather data request for {filename}")
            return response_data, 201
            
        except Exception as e:
            logger.error(f"Error in store_weather_data: {e}")
            return {'error': str(e)}, 500

@weather_ns.route('/list-weather-files')
class ListWeatherFiles(Resource):
    @weather_ns.marshal_with(files_list_model)
    @weather_ns.response(500, 'Internal Server Error', error_model)
    @weather_ns.doc('list_weather_files')
    def get(self):
        """
        List all weather data files
        
        Returns a list of all weather data files stored in the storage bucket
        with their metadata including size, creation time, and update time.
        """
        try:
            files = get_storage_service().list_weather_files()
            
            response_data = {
                'files': files,
                'count': len(files)
            }
            
            logger.info(f"Listed {len(files)} weather files")
            return response_data, 200
            
        except Exception as e:
            logger.error(f"Error in list_weather_files: {e}")
            return {'error': str(e)}, 500

@weather_ns.route('/weather-file-content/<string:filename>')
class GetWeatherFileContent(Resource):
    @weather_ns.response(200, 'Success - Returns weather data JSON')
    @weather_ns.response(404, 'File not found', error_model)
    @weather_ns.response(500, 'Internal Server Error', error_model)
    @weather_ns.doc('get_weather_file_content')
    def get(self, filename):
        """
        Get weather file content
        
        Retrieves and returns the content of a specific weather data file.
        The response contains the complete weather data in JSON format including
        coordinates, timezone, and daily weather measurements.
        """
        try:
            weather_data = get_storage_service().get_weather_file_content(filename)
            
            logger.info(f"Retrieved content for file: {filename}")
            return weather_data, 200
            
        except Exception as e:
            error_message = str(e)
            status_code = 404 if 'not found' in error_message.lower() else 500
            
            logger.error(f"Error in get_weather_file_content: {e}")
            return {'error': error_message}, status_code

@weather_ns.route('/health')
class HealthCheck(Resource):
    @weather_ns.marshal_with(health_model)
    @weather_ns.doc('health_check')
    def get(self):
        """
        Health check endpoint
        
        Returns the current health status of the service including
        timestamp and version information.
        """
        from datetime import datetime
        
        try:
            response_data = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'service': 'weather-backend-service',
                'version': '1.0.0'
            }
            
            logger.debug("Health check requested")
            return response_data, 200
            
        except Exception as e:
            logger.error(f"Error in health_check: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }, 500

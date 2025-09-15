"""
API routes for Weather Backend Service
"""
from flask import Blueprint, request, jsonify
from src.services.weather_service import WeatherService
from src.services.storage_service import StorageService
from src.services.mock_storage_service import MockStorageService
from src.utils.validators import validate_weather_request
from src.utils.logging_config import get_logger
from src.config import config
import os

logger = get_logger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__)

# Initialize services (will be created per request to handle testing)
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
        # Use mock storage for development/local testing
        config_name = os.environ.get('FLASK_ENV', 'default')
        app_config = config[config_name]
        
        if hasattr(app_config, 'USE_MOCK_STORAGE') and app_config.USE_MOCK_STORAGE:
            logger.info("Using mock storage service for local development")
            storage_service = MockStorageService()
        else:
            logger.info("Using Google Cloud Storage service")
            storage_service = StorageService()
    return storage_service


@api_bp.route('/store-weather-data', methods=['POST'])
def store_weather_data():
    """Store weather data endpoint"""
    try:
        # Validate request data
        data = request.get_json()
        is_valid, error_message, normalized_data = validate_weather_request(data)
        
        if not is_valid:
            logger.warning(f"Invalid request: {error_message}")
            return jsonify({'error': error_message}), 400
        
        # Fetch weather data
        weather_data = get_weather_service().fetch_weather_data(
            normalized_data['latitude'],
            normalized_data['longitude'],
            normalized_data['start_date'],
            normalized_data['end_date']
        )
        
        # Store in GCS
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
        return jsonify(response_data), 201
        
    except Exception as e:
        logger.error(f"Error in store_weather_data: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/list-weather-files', methods=['GET'])
def list_weather_files():
    """List all weather data files in GCS bucket"""
    try:
        files = get_storage_service().list_weather_files()
        
        response_data = {
            'files': files,
            'count': len(files)
        }
        
        logger.info(f"Listed {len(files)} weather files")
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in list_weather_files: {e}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/weather-file-content/<filename>', methods=['GET'])
def get_weather_file_content(filename):
    """Get content of a specific weather data file"""
    try:
        weather_data = get_storage_service().get_weather_file_content(filename)
        
        logger.info(f"Retrieved content for file: {filename}")
        return jsonify(weather_data), 200
        
    except Exception as e:
        error_message = str(e)
        status_code = 404 if 'not found' in error_message.lower() else 500
        
        logger.error(f"Error in get_weather_file_content: {e}")
        return jsonify({'error': error_message}), status_code


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    from datetime import datetime
    
    try:
        # Basic health check - could be extended to check dependencies
        response_data = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'weather-backend-service',
            'version': '1.0.0'
        }
        
        logger.debug("Health check requested")
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error in health_check: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


# Error handlers
@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    logger.warning(f"404 error: {request.url}")
    return jsonify({'error': 'Endpoint not found'}), 404


@api_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    logger.warning(f"405 error: {request.method} {request.url}")
    return jsonify({'error': 'Method not allowed'}), 405


@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

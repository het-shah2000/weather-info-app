"""
Main Flask application for Weather Backend Service
"""
import os
from flask import Flask
from src.config import config
from src.api.routes import api_bp
from src.api.swagger_routes import api as swagger_api
from src.utils.logging_config import setup_logging, get_logger


def create_app(config_name: str = None) -> Flask:
    """
    Application factory pattern
    
    Args:
        config_name: Configuration name to use
        
    Returns:
        Flask application instance
    """
    # Determine configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # Setup logging
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_format = os.environ.get('LOG_FORMAT', 'json')
    setup_logging(level=log_level, format_type=log_format)
    
    logger = get_logger(__name__)
    logger.info(f"Starting Weather Backend Service with config: {config_name}")
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/weather')
    
    # Initialize Swagger API
    swagger_api.init_app(app)
    
    # Add CORS headers if needed
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    logger.info("Weather Backend Service initialized successfully")
    return app


def main():
    """Main entry point"""
    app = create_app()
    
    # Get configuration
    config_name = os.environ.get('FLASK_ENV', 'default')
    app_config = config[config_name]
    
    # Run the application
    app.run(
        host=app_config.HOST,
        port=app_config.PORT,
        debug=app_config.DEBUG
    )


if __name__ == '__main__':
    main()

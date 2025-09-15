# Weather Analytics Platform

A full-stack weather analytics platform featuring a robust Flask backend service and an interactive React dashboard for visualizing historical weather data from the Open-Meteo API.

## 🌟 Features

### Backend Service
- 🌤️ **Weather Data Fetching**: Integrates with Open-Meteo API for historical weather data
- ☁️ **Dual Storage**: Supports both Google Cloud Storage and local mock storage
- 📋 **RESTful API**: Clean REST endpoints with comprehensive validation
- 📊 **Interactive Documentation**: Built-in Swagger UI for API exploration
- 🧪 **Production Ready**: Containerized with comprehensive testing

### Frontend Dashboard
- 📱 **Interactive Visualization**: Beautiful charts using Chart.js
- 🎨 **Responsive Design**: Mobile-first design with Tailwind CSS
- ⚡ **Real-time Data**: Live weather data fetching and visualization
- 📤 **Data Export**: CSV export functionality for analysis
- 📄 **Smart Pagination**: Efficient data table with customizable page sizes

## 🚀 Live Demo

- **Frontend Dashboard**: [Deploy to Vercel/Netlify]
- **Backend API**: [Deploy to Railway/Render]
- **API Documentation**: [Your-API-URL]/docs/

## 🏗️ Architecture

This is a **monorepo** containing both frontend and backend services:

```
weather-analytics-platform/
├── frontend/          # React dashboard with Tailwind CSS
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── utils/         # API utilities and validation
│   │   └── styles/        # Tailwind CSS styles
│   ├── package.json
│   └── vite.config.js
├── src/               # Flask backend service
│   ├── api/           # API routes and Swagger docs
│   ├── services/      # Weather and storage services
│   └── utils/         # Validation and logging
├── tests/             # Backend test suite
└── requirements.txt   # Python dependencies
```

## Project Structure

```
weather-backend-service/
├── src/                          # Source code
│   ├── api/                      # API routes and blueprints
│   │   ├── __init__.py
│   │   └── routes.py            # Flask routes
│   ├── services/                # Business logic services
│   │   ├── __init__.py
│   │   ├── weather_service.py   # Open-Meteo API integration
│   │   └── storage_service.py   # Google Cloud Storage operations
│   ├── utils/                   # Utility modules
│   │   ├── __init__.py
│   │   ├── validators.py        # Input validation
│   │   └── logging_config.py    # Logging configuration
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   └── app.py                  # Flask application factory
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_api.py            # API endpoint tests
│   └── test_validators.py     # Validation tests
├── scripts/                   # Deployment and setup scripts
│   ├── deploy.sh             # GCP deployment script
│   └── setup.sh              # Development setup script
├── app.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
├── docker-compose.yml       # Local development with Docker
├── Makefile                # Development commands
├── pytest.ini             # Test configuration
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore patterns
└── README.md            # This file
```

## API Endpoints

### 1. Store Weather Data
**POST** `/store-weather-data`

Fetches historical weather data and stores it in GCS.

**Request Body:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "start_date": "2023-01-01",
  "end_date": "2023-01-31"
}
```

**Response:**
```json
{
  "message": "Weather data stored successfully",
  "filename": "weather_data_lat40.7128_lon-74.006_2023-01-01_to_2023-01-31_20240101_120000.json",
  "location": "gs://weather-data-bucket/weather_data_lat40.7128_lon-74.006_2023-01-01_to_2023-01-31_20240101_120000.json"
}
```

**Weather Variables Fetched:**
- Maximum Temperature (2m)
- Minimum Temperature (2m)
- Mean Temperature (2m)
- Maximum Apparent Temperature (2m)
- Minimum Apparent Temperature (2m)
- Mean Apparent Temperature (2m)

### 2. List Weather Files
**GET** `/list-weather-files`

Returns a list of all weather data files stored in GCS.

**Response:**
```json
{
  "files": [
    {
      "filename": "weather_data_lat40.7128_lon-74.006_2023-01-01_to_2023-01-31_20240101_120000.json",
      "size": 15420,
      "created": "2024-01-01T12:00:00.000Z",
      "updated": "2024-01-01T12:00:00.000Z"
    }
  ],
  "count": 1
}
```

### 3. Get Weather File Content
**GET** `/weather-file-content/<filename>`

Retrieves the content of a specific weather data file.

**Response:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.006,
  "generationtime_ms": 0.123,
  "utc_offset_seconds": 0,
  "timezone": "UTC",
  "daily_units": {
    "time": "iso8601",
    "temperature_2m_max": "°C",
    "temperature_2m_min": "°C",
    "temperature_2m_mean": "°C",
    "apparent_temperature_max": "°C",
    "apparent_temperature_min": "°C",
    "apparent_temperature_mean": "°C"
  },
  "daily": {
    "time": ["2023-01-01", "2023-01-02", "..."],
    "temperature_2m_max": [5.2, 7.1, "..."],
    "temperature_2m_min": [-2.1, 0.3, "..."],
    "temperature_2m_mean": [1.5, 3.7, "..."],
    "apparent_temperature_max": [3.8, 5.9, "..."],
    "apparent_temperature_min": [-4.2, -1.8, "..."],
    "apparent_temperature_mean": [-0.2, 2.1, "..."]
  }
}
```

### 4. Health Check
**GET** `/health`

Returns the health status of the service.

## Prerequisites

1. **Google Cloud Platform Account**
2. **Google Cloud SDK** installed and configured
3. **Docker** installed (for containerization)
4. **Python 3.11+** (for local development)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd weather-backend-service
```

### 2. Google Cloud Setup

#### Create a GCP Project
```bash
gcloud projects create your-project-id
gcloud config set project your-project-id
```

#### Enable Required APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com
```

#### Create a Service Account
```bash
gcloud iam service-accounts create weather-service-account \
    --display-name="Weather Service Account"

gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:weather-service-account@your-project-id.iam.gserviceaccount.com" \
    --role="roles/storage.admin"
```

#### Create a GCS Bucket
```bash
gsutil mb gs://your-weather-data-bucket
```

### 3. Local Development Setup

#### Quick Setup (Recommended)
```bash
# Run the setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

#### Manual Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your actual values

# Run tests
make test

# Start the application
make run
```

#### Set Environment Variables
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
export GCS_BUCKET_NAME="your-weather-data-bucket"
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

#### Run Locally
```bash
python app.py
# OR
make run
```

The service will be available at `http://localhost:8080`

## Development Commands

The project includes a Makefile with common development tasks:

```bash
make help          # Show available commands
make install       # Install dependencies
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run linting (requires dev dependencies)
make format        # Format code (requires dev dependencies)
make clean         # Clean up generated files
make run           # Run the application
make run-dev       # Run in development mode
make docker-build  # Build Docker image
make docker-run    # Run Docker container
```

## Deployment to Google Cloud Run

### Method 1: Using Deployment Script (Recommended)

#### 1. Quick Deploy
```bash
# Set required environment variables
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GCS_BUCKET_NAME="your-weather-data-bucket"

# Run the deployment script
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Method 2: Manual Cloud Build Deploy

#### 1. Build and Deploy
```bash
gcloud run deploy weather-backend-service \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GCS_BUCKET_NAME=your-weather-data-bucket \
    --project your-project-id
```

### Method 2: Using Docker

#### 1. Build Docker Image
```bash
docker build -t gcr.io/your-project-id/weather-backend-service .
```

#### 2. Push to Container Registry
```bash
docker push gcr.io/your-project-id/weather-backend-service
```

#### 3. Deploy to Cloud Run
```bash
gcloud run deploy weather-backend-service \
    --image gcr.io/your-project-id/weather-backend-service \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars GCS_BUCKET_NAME=your-weather-data-bucket \
    --service-account weather-service-account@your-project-id.iam.gserviceaccount.com
```

## Testing the API

### Using curl

#### Store Weather Data
```bash
curl -X POST https://your-service-url/store-weather-data \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 40.7128,
    "longitude": -74.0060,
    "start_date": "2023-01-01",
    "end_date": "2023-01-31"
  }'
```

#### List Files
```bash
curl https://your-service-url/list-weather-files
```

#### Get File Content
```bash
curl https://your-service-url/weather-file-content/filename.json
```

### Using Python requests
```python
import requests

# Store weather data
response = requests.post('https://your-service-url/store-weather-data', json={
    'latitude': 40.7128,
    'longitude': -74.0060,
    'start_date': '2023-01-01',
    'end_date': '2023-01-31'
})
print(response.json())

# List files
response = requests.get('https://your-service-url/list-weather-files')
print(response.json())
```

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:

- **400 Bad Request**: Invalid input data, missing fields, or validation errors
- **404 Not Found**: File not found or invalid endpoint
- **405 Method Not Allowed**: Invalid HTTP method
- **500 Internal Server Error**: Server-side errors

Example error response:
```json
{
  "error": "Latitude must be between -90 and 90"
}
```

## File Naming Convention

Weather data files are stored with the following naming pattern:
```
weather_data_lat{latitude}_lon{longitude}_{start_date}_to_{end_date}_{timestamp}.json
```

Example: `weather_data_lat40.7128_lon-74.006_2023-01-01_to_2023-01-31_20240101_120000.json`

## Environment Variables

- `GCS_BUCKET_NAME`: Name of the Google Cloud Storage bucket (required)
- `PORT`: Port number for the application (default: 8080)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to service account key file (for local development)

## Performance Considerations

- API requests to Open-Meteo are cached by the service
- GCS operations are optimized for batch processing
- Gunicorn is configured with 4 workers for production deployment
- Request timeout is set to 120 seconds for large date ranges

## Security

- Service account follows principle of least privilege
- Input validation prevents injection attacks
- CORS headers can be configured as needed
- All API responses include appropriate HTTP status codes

## Monitoring and Logging

Google Cloud Run provides built-in monitoring and logging. You can view:
- Request logs in Google Cloud Console
- Performance metrics
- Error rates and response times

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure service account has proper GCS permissions
2. **Bucket Not Found**: Verify bucket name and existence
3. **API Rate Limits**: Open-Meteo has rate limits; implement retry logic if needed
4. **Large Date Ranges**: Very large date ranges may timeout; consider chunking requests

### Debug Mode

For local development, enable debug mode:
```python
app.run(host='0.0.0.0', port=port, debug=True)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

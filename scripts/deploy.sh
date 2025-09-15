#!/bin/bash

# Weather Backend Service Deployment Script
# This script helps deploy the service to Google Cloud Run

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required environment variables are set
check_env_vars() {
    print_status "Checking environment variables..."
    
    if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
        print_error "GOOGLE_CLOUD_PROJECT environment variable is not set"
        exit 1
    fi
    
    if [ -z "$GCS_BUCKET_NAME" ]; then
        print_error "GCS_BUCKET_NAME environment variable is not set"
        exit 1
    fi
    
    print_status "Environment variables are set"
}

# Check if gcloud is installed and authenticated
check_gcloud() {
    print_status "Checking Google Cloud SDK..."
    
    if ! command -v gcloud &> /dev/null; then
        print_error "gcloud CLI is not installed. Please install Google Cloud SDK."
        exit 1
    fi
    
    # Check if authenticated
    if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
        print_error "Not authenticated with Google Cloud. Run: gcloud auth login"
        exit 1
    fi
    
    print_status "Google Cloud SDK is ready"
}

# Enable required APIs
enable_apis() {
    print_status "Enabling required Google Cloud APIs..."
    
    gcloud services enable cloudbuild.googleapis.com --project=$GOOGLE_CLOUD_PROJECT
    gcloud services enable run.googleapis.com --project=$GOOGLE_CLOUD_PROJECT
    gcloud services enable storage.googleapis.com --project=$GOOGLE_CLOUD_PROJECT
    
    print_status "APIs enabled successfully"
}

# Create GCS bucket if it doesn't exist
create_bucket() {
    print_status "Checking if GCS bucket exists..."
    
    if gsutil ls -b gs://$GCS_BUCKET_NAME &> /dev/null; then
        print_status "Bucket gs://$GCS_BUCKET_NAME already exists"
    else
        print_status "Creating GCS bucket: $GCS_BUCKET_NAME"
        gsutil mb gs://$GCS_BUCKET_NAME
        print_status "Bucket created successfully"
    fi
}

# Deploy to Cloud Run
deploy_service() {
    print_status "Deploying to Google Cloud Run..."
    
    gcloud run deploy weather-backend-service \
        --source . \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated \
        --set-env-vars GCS_BUCKET_NAME=$GCS_BUCKET_NAME \
        --project=$GOOGLE_CLOUD_PROJECT \
        --max-instances=10 \
        --memory=512Mi \
        --cpu=1 \
        --timeout=300
    
    print_status "Deployment completed successfully!"
}

# Get service URL
get_service_url() {
    print_status "Getting service URL..."
    
    SERVICE_URL=$(gcloud run services describe weather-backend-service \
        --platform managed \
        --region us-central1 \
        --project=$GOOGLE_CLOUD_PROJECT \
        --format="value(status.url)")
    
    print_status "Service deployed at: $SERVICE_URL"
    print_status "Health check: $SERVICE_URL/health"
    print_status "API endpoints:"
    print_status "  POST $SERVICE_URL/store-weather-data"
    print_status "  GET  $SERVICE_URL/list-weather-files"
    print_status "  GET  $SERVICE_URL/weather-file-content/<filename>"
}

# Main deployment function
main() {
    print_status "Starting Weather Backend Service deployment..."
    
    check_env_vars
    check_gcloud
    enable_apis
    create_bucket
    deploy_service
    get_service_url
    
    print_status "Deployment completed successfully! 🎉"
}

# Run main function
main "$@"

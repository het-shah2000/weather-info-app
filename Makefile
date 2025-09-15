.PHONY: help install test lint format clean run docker-build docker-run deploy

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
SRC_DIR := src
TEST_DIR := tests

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	$(PIP) install -r requirements.txt

install-dev: ## Install development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install black flake8 mypy

test: ## Run tests
	$(PYTHON) -m pytest $(TEST_DIR) -v

test-cov: ## Run tests with coverage
	$(PYTHON) -m pytest $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term

lint: ## Run linting
	flake8 $(SRC_DIR) $(TEST_DIR)
	mypy $(SRC_DIR)

format: ## Format code
	black $(SRC_DIR) $(TEST_DIR)

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/

run: ## Run the application locally
	$(PYTHON) app.py

run-dev: ## Run the application in development mode
	FLASK_ENV=development $(PYTHON) app.py

docker-build: ## Build Docker image
	docker build -t weather-backend-service .

docker-run: ## Run Docker container
	docker run -p 8080:8080 --env-file .env weather-backend-service

deploy-gcp: ## Deploy to Google Cloud Run
	gcloud run deploy weather-backend-service \
		--source . \
		--platform managed \
		--region us-central1 \
		--allow-unauthenticated \
		--set-env-vars GCS_BUCKET_NAME=$(GCS_BUCKET_NAME)

setup-venv: ## Set up virtual environment
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

activate-venv: ## Show command to activate virtual environment
	@echo "Run: source $(VENV)/bin/activate"

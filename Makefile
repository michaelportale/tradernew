.PHONY: help setup dev backend-dev frontend-dev test backend-test frontend-test lint format migrations db-upgrade

help:
	@echo "ML Trading System"
	@echo "---------------"
	@echo "make setup       # Set up the development environment"
	@echo "make dev         # Run the full development environment"
	@echo "make backend-dev # Run the backend server only"
	@echo "make frontend-dev # Run the frontend server only"
	@echo "make test        # Run all tests"
	@echo "make backend-test # Run backend tests"
	@echo "make frontend-test # Run frontend tests"
	@echo "make lint        # Run linters"
	@echo "make format      # Format code"
	@echo "make migrations  # Generate database migrations"
	@echo "make db-upgrade  # Apply database migrations"

setup:
	@echo "Setting up development environment..."
	cd backend && poetry install
	cd frontend && npm install

dev:
	@echo "Starting development environment..."
	docker-compose -f docker-compose.dev.yml up

backend-dev:
	@echo "Starting backend server..."
	cd backend && poetry run uvicorn app.main:app --reload

frontend-dev:
	@echo "Starting frontend server..."
	cd frontend && npm run dev

test:
	@echo "Running all tests..."
	make backend-test
	make frontend-test

backend-test:
	@echo "Running backend tests..."
	cd backend && poetry run pytest

frontend-test:
	@echo "Running frontend tests..."
	cd frontend && npm test

lint:
	@echo "Running linters..."
	cd backend && poetry run flake8
	cd backend && poetry run mypy app
	cd frontend && npm run lint

format:
	@echo "Formatting code..."
	cd backend && poetry run black .
	cd backend && poetry run isort .
	cd frontend && npm run format

migrations:
	@echo "Generating database migrations..."
	cd backend && poetry run alembic revision --autogenerate -m "$(message)"

db-upgrade:
	@echo "Applying database migrations..."
	cd backend && poetry run alembic upgrade head

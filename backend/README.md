# ML Trading System Backend

The backend service for the ML Trading System, built with FastAPI, SQLAlchemy, Celery and Redis.

## Features

- Fast and efficient API with FastAPI
- Asynchronous database operations with SQLAlchemy and Asyncpg
- Background task processing with Celery and Redis
- ML model training and backtesting
- Market data processing and technical indicator calculation
- Scheduled data fetching tasks with Celery Beat

## Background Tasks with Celery

This system uses Celery with Redis for handling background tasks:

- Model training and evaluation tasks
- Market data processing tasks
- Technical indicator calculation tasks
- Market data fetching tasks

### Task Queues

The system has two main task queues:

1. `model_tasks`: For machine learning model training and evaluation
2. `data_tasks`: For market data processing, indicator calculation, and data fetching

### Scheduled Tasks with Celery Beat

The system uses Celery Beat to run scheduled tasks:

- Daily market data fetching for popular stocks (AAPL, MSFT, GOOGL, etc.) at 18:00 UTC on weekdays

## Running the application

### Using Docker Compose

The easiest way to run the application is using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis server
- FastAPI backend
- Celery workers for model tasks and data tasks
- Celery Beat for scheduled tasks
- Flower for monitoring Celery tasks
- Frontend application

### Running Celery Workers Manually

To run the Celery workers manually, use the provided `celery_worker.py` script:

```bash
# Run a worker for model tasks
python celery_worker.py --queue model_tasks

# Run a worker for data tasks  
python celery_worker.py --queue data_tasks

# Run a worker with both queues
python celery_worker.py

# Run with a specific concurrency
python celery_worker.py --concurrency 4
```

### Running Celery Beat Manually

To run the Celery Beat scheduler manually:

```bash
celery -A app.tasks.worker beat --loglevel=info
```

### Monitoring with Flower

Celery Flower provides a web interface to monitor Celery tasks. It is available at:

```
http://localhost:5555
```

## API Endpoints

### Model Training

- `POST /api/v1/models/train`: Create and train a new model
- `POST /api/v1/models/{model_id}/retrain`: Retrain an existing model

### Data Processing

- `POST /api/v1/data/tasks/process`: Process market data for a symbol
- `POST /api/v1/data/tasks/indicators`: Calculate technical indicators for a symbol
- `POST /api/v1/data/tasks/fetch`: Fetch market data for a symbol for the last X days

### Task Management

- `GET /api/v1/tasks/{task_id}`: Get the status of a task
- `POST /api/v1/tasks/{task_id}/revoke`: Revoke a running or pending task
- `GET /api/v1/tasks/`: Get a list of active tasks

## Example API Usage

### Train a new model

```bash
curl -X POST "http://localhost:8000/api/v1/models/train" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SPY Trend Predictor",
    "description": "Predicts trend direction for SPY",
    "model_type": "random_forest",
    "features": ["sma_20", "rsi_14", "macd", "volume"],
    "target": "trend_direction",
    "parameters": {
      "n_estimators": 100,
      "max_depth": 10,
      "random_state": 42
    }
  }'
```

### Process market data

```bash
curl -X POST "http://localhost:8000/api/v1/data/tasks/process?symbol=AAPL&start_date=2023-01-01&end_date=2023-12-31"
```

### Calculate technical indicators

```bash
curl -X POST "http://localhost:8000/api/v1/data/tasks/indicators" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "indicators": ["sma", "ema", "rsi", "macd"]
  }'
```

### Fetch market data

```bash
curl -X POST "http://localhost:8000/api/v1/data/tasks/fetch?symbol=AAPL&days=30"
```

### Check task status

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/{task_id}"
``` 
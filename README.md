# ML Trading System

A comprehensive machine learning trading system that demonstrates advanced software engineering, data science, and financial domain expertise.

## Project Vision

To create an impressive, production-ready machine learning trading system that enables users to fetch real financial data, train ML models for predicting market movements, backtest trading strategies, and visualize performance metrics through a modern, intuitive interface.

## Core Features

- Data fetching from various financial sources
- Feature engineering and technical indicator calculation
- ML model training and evaluation
- Strategy backtesting with realistic market simulation
- Performance visualization and analysis
- Modern, responsive web interface

## Tech Stack

### Backend
- FastAPI for API development
- PostgreSQL with TimescaleDB for time-series data
- SQLAlchemy for ORM
- Pandas/NumPy for data manipulation
- scikit-learn for ML models
- Celery for background tasks

### Frontend
- React with TypeScript
- Tailwind CSS for styling
- TradingView for financial charts
- React Query for data fetching

### DevOps
- Docker and Docker Compose
- GitHub Actions for CI/CD

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.10+
- Node.js 18+
- Poetry (Python dependency management)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ml-trading-system.git
   cd ml-trading-system
   ```

2. Create an `.env` file from the example:
   ```
   cp .env.example .env
   ```

3. Start the development environment:
   ```
   make dev
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development

- Run backend only: `make backend-dev`
- Run frontend only: `make frontend-dev`
- Run tests: `make test`
- Format code: `make format`

## License

MIT

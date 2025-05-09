# Setup Instructions

This document provides detailed instructions for setting up the ML Trading System development environment.

## Prerequisites

Before you begin, ensure you have the following installed:

- Docker and Docker Compose
- Python 3.10 or higher
- Node.js 18 or higher
- Poetry (Python dependency management)
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ml-trading-system.git
cd ml-trading-system
```

### 2. Environment Setup

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit the `.env` file to update the configuration as needed:

```
# Backend
POSTGRES_SERVER=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=ml_trading
REDIS_HOST=redis
REDIS_PORT=6379
SECRET_KEY=your-super-secret-key-here-at-least-32-characters

# External APIs (get these from the respective services)
YAHOO_FINANCE_API_KEY=your_yahoo_finance_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
FRED_API_KEY=your_fred_api_key

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Backend Setup

Install backend dependencies using Poetry:

```bash
cd backend
poetry install
```

### 4. Frontend Setup

Install frontend dependencies:

```bash
cd frontend
npm install
```

### 5. Start Development Environment

Start the entire development stack with Docker Compose:

```bash
make dev
```

Or start individual components:

```bash
# Backend only
make backend-dev

# Frontend only
make frontend-dev
```

### 6. Access the Application

Once the application is running, you can access:

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Workflow

### Database Migrations

Create a new migration:

```bash
make migrations message="Your migration description"
```

Apply migrations:

```bash
make db-upgrade
```

### Code Formatting

Format all code:

```bash
make format
```

### Running Tests

Run all tests:

```bash
make test
```

Or specific tests:

```bash
make backend-test
make frontend-test
```

## Troubleshooting

### Database Connection Issues

If you encounter database connection issues:

1. Ensure PostgreSQL is running:
   ```bash
   docker-compose ps
   ```

2. Check the logs:
   ```bash
   docker-compose logs postgres
   ```

3. Verify your database credentials in the `.env` file.

### Port Conflicts

If you encounter port conflicts, edit the `docker-compose.yml` file to change the exposed ports.

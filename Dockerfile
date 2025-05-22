# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock* alembic.ini ./
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the FastAPI app code
COPY backend/app ./app
COPY backend/alembic ./backend/alembic

# Copy .env if you want it in the container (optional, since you use env_file in compose)
# COPY backend/.env .env

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
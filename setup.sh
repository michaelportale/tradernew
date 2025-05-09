#!/bin/bash
# Script to generate the initial ML Trading System project structure

# Check if the directory already exists
if [ -d "ml-trading-system" ]; then
  echo "Error: The directory 'ml-trading-system' already exists."
  echo "Please either remove it or run this script in a different location."
  exit 1
fi

# Create root directory
mkdir -p ml-trading-system
cd ml-trading-system

echo "Creating project structure..."

# GitHub workflows
mkdir -p .github/workflows
cat > .github/workflows/ci.yml << 'EOT'
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
      - name: Install dependencies
        run: |
          cd backend
          poetry install
      - name: Run tests
        run: |
          cd backend
          poetry run pytest
EOT

# Backend structure
mkdir -p backend/app/api/v1/endpoints
mkdir -p backend/app/core
mkdir -p backend/app/db
mkdir -p backend/app/models
mkdir -p backend/app/schemas
mkdir -p backend/app/services
mkdir -p backend/app/tasks
mkdir -p backend/alembic/versions
mkdir -p backend/ml/data/providers
mkdir -p backend/ml/data/processors
mkdir -p backend/ml/data/features
mkdir -p backend/ml/models
mkdir -p backend/ml/evaluation
mkdir -p backend/backtest
mkdir -p backend/tests/api

# Create __init__.py files
touch backend/app/__init__.py
touch backend/app/api/__init__.py
touch backend/app/api/v1/__init__.py
touch backend/app/api/v1/endpoints/__init__.py
touch backend/app/core/__init__.py
touch backend/app/db/__init__.py
touch backend/app/models/__init__.py
touch backend/app/schemas/__init__.py
touch backend/app/services/__init__.py
touch backend/app/tasks/__init__.py
touch backend/ml/__init__.py
touch backend/ml/data/__init__.py
touch backend/ml/data/providers/__init__.py
touch backend/ml/data/processors/__init__.py
touch backend/ml/data/features/__init__.py
touch backend/ml/models/__init__.py
touch backend/ml/evaluation/__init__.py
touch backend/backtest/__init__.py
touch backend/tests/__init__.py
touch backend/tests/api/__init__.py

echo "Creating backend files..."

# Create initial backend files
cat > backend/pyproject.toml << 'EOT'
[tool.poetry]
name = "ml-trading-system"
version = "0.1.0"
description = "Machine Learning Trading System"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.104.0"
uvicorn = "^0.23.2"
sqlalchemy = "^2.0.22"
alembic = "^1.12.0"
pydantic = "^2.4.2"
python-dotenv = "^1.0.0"
psycopg2-binary = "^2.9.9"
celery = "^5.3.4"
redis = "^5.0.1"
pandas = "^2.1.1"
numpy = "^1.26.0"
scikit-learn = "^1.3.1"
yfinance = "^0.2.31"
pandas-ta = "^0.3.14b0"
loguru = "^0.7.2"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.2"
pytest-asyncio = "^0.21.1"
pytest-cov = "^4.1.0"
black = "^23.10.0"
isort = "^5.12.0"
mypy = "^1.6.1"
flake8 = "^6.1.0"
pre-commit = "^3.5.0"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ["py310"]

[tool.isort]
profile = "black"

[tool.mypy]
python_version = "3.10"
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
strict_optional = true
warn_redundant_casts = true
warn_return_any = true
warn_unused_ignores = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
EOT

cat > backend/app/core/config.py << 'EOT'
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings
from typing import Any, Dict, List, Optional, Union


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ML Trading System"
    
    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # External APIs
    YAHOO_FINANCE_RATE_LIMIT: int = 2000  # Requests per hour

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
EOT

cat > backend/app/main.py << 'EOT'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "Welcome to ML Trading System API"}
EOT

cat > backend/app/api/v1/endpoints/health.py << 'EOT'
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok"}
EOT

cat > backend/app/api/v1/router.py << 'EOT'
from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])

# Add more routers as you implement them
# api_router.include_router(data.router, prefix="/data", tags=["data"])
# api_router.include_router(models.router, prefix="/models", tags=["models"])
# api_router.include_router(backtest.router, prefix="/backtest", tags=["backtest"])
EOT

cat > backend/app/db/base.py << 'EOT'
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
EOT

cat > backend/app/db/session.py << 'EOT'
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOT

cat > backend/Dockerfile << 'EOT'
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy project
COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOT

echo "Creating frontend files..."

# Frontend structure
mkdir -p frontend/public
mkdir -p frontend/src/assets
mkdir -p frontend/src/components/common
mkdir -p frontend/src/components/charts
mkdir -p frontend/src/components/layout
mkdir -p frontend/src/hooks
mkdir -p frontend/src/pages
mkdir -p frontend/src/services
mkdir -p frontend/src/types
mkdir -p frontend/src/utils

# Create initial frontend files
cat > frontend/package.json << 'EOT'
{
  "name": "ml-trading-system-frontend",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "format": "prettier --write 'src/**/*.{js,jsx,ts,tsx,css,md,json}'"
  },
  "dependencies": {
    "axios": "^1.5.1",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-query": "^3.39.3",
    "react-router-dom": "^6.16.0",
    "recharts": "^2.8.0",
    "lightweight-charts": "^4.1.0",
    "zustand": "^4.4.3"
  },
  "devDependencies": {
    "@types/node": "^20.8.6",
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@typescript-eslint/eslint-plugin": "^6.7.5",
    "@typescript-eslint/parser": "^6.7.5",
    "@vitejs/plugin-react": "^4.1.0",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.51.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.3",
    "postcss": "^8.4.31",
    "prettier": "3.0.3",
    "tailwindcss": "^3.3.3",
    "typescript": "^5.2.2",
    "vite": "^4.4.11"
  }
}
EOT

cat > frontend/tsconfig.json << 'EOT'
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    
    /* Path aliases */
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
EOT

cat > frontend/tsconfig.node.json << 'EOT'
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
EOT

cat > frontend/vite.config.ts << 'EOT'
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
EOT

cat > frontend/tailwind.config.js << 'EOT'
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
EOT

cat > frontend/postcss.config.js << 'EOT'
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
EOT

cat > frontend/index.html << 'EOT'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ML Trading System</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
EOT

cat > frontend/src/main.tsx << 'EOT'
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
EOT

cat > frontend/src/App.tsx << 'EOT'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import Dashboard from './pages/Dashboard';
import DataExplorer from './pages/DataExplorer';
import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="flex h-screen bg-gray-100">
          <Sidebar />
          <div className="flex flex-col flex-1 overflow-hidden">
            <Header />
            <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 p-6">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/data" element={<DataExplorer />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
EOT

cat > frontend/src/index.css << 'EOT'
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
    Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  line-height: 1.5;
  font-weight: 400;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  min-height: 100vh;
}
EOT

echo "Creating component files..."

mkdir -p frontend/src/pages
cat > frontend/src/pages/Dashboard.tsx << 'EOT'
import React from 'react';

const Dashboard: React.FC = () => {
  return (
    <div className="grid gap-6 mb-8 md:grid-cols-2 xl:grid-cols-4">
      <div className="min-w-0 rounded-lg shadow-xs overflow-hidden bg-white">
        <div className="p-4 flex items-center">
          <div className="p-3 rounded-full text-orange-500 bg-orange-100 mr-4">
            <svg fill="currentColor" viewBox="0 0 20 20" className="w-5 h-5">
              <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"></path>
            </svg>
          </div>
          <div>
            <p className="mb-2 text-sm font-medium text-gray-600">
              Models
            </p>
            <p className="text-lg font-semibold text-gray-700">
              8
            </p>
          </div>
        </div>
      </div>
      
      <div className="min-w-0 rounded-lg shadow-xs overflow-hidden bg-white">
        <div className="p-4 flex items-center">
          <div className="p-3 rounded-full text-green-500 bg-green-100 mr-4">
            <svg fill="currentColor" viewBox="0 0 20 20" className="w-5 h-5">
              <path fillRule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"></path>
            </svg>
          </div>
          <div>
            <p className="mb-2 text-sm font-medium text-gray-600">
              Dataset Size
            </p>
            <p className="text-lg font-semibold text-gray-700">
              1,235 records
            </p>
          </div>
        </div>
      </div>
      
      <div className="min-w-0 rounded-lg shadow-xs overflow-hidden bg-white">
        <div className="p-4 flex items-center">
          <div className="p-3 rounded-full text-blue-500 bg-blue-100 mr-4">
            <svg fill="currentColor" viewBox="0 0 20 20" className="w-5 h-5">
              <path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"></path>
            </svg>
          </div>
          <div>
            <p className="mb-2 text-sm font-medium text-gray-600">
              Backtests
            </p>
            <p className="text-lg font-semibold text-gray-700">
              12
            </p>
          </div>
        </div>
      </div>
      
      <div className="min-w-0 rounded-lg shadow-xs overflow-hidden bg-white">
        <div className="p-4 flex items-center">
          <div className="p-3 rounded-full text-teal-500 bg-teal-100 mr-4">
            <svg fill="currentColor" viewBox="0 0 20 20" className="w-5 h-5">
              <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2zM7 8H5v2h2V8zm2 0h2v2H9V8zm6 0h-2v2h2V8z" clipRule="evenodd"></path>
            </svg>
          </div>
          <div>
            <p className="mb-2 text-sm font-medium text-gray-600">
              Active Strategies
            </p>
            <p className="text-lg font-semibold text-gray-700">
              3
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
EOT

cat > frontend/src/pages/DataExplorer.tsx << 'EOT'
import React from 'react';

const DataExplorer: React.FC = () => {
  return (
    <div className="container mx-auto">
      <h2 className="text-2xl font-semibold text-gray-700 mb-6">Data Explorer</h2>
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Symbol
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
              placeholder="AAPL"
              defaultValue="AAPL"
            />
            <button
              type="button"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Fetch Data
            </button>
          </div>
        </div>
        
        <div className="bg-gray-100 p-4 rounded-md mb-4">
          <p className="text-gray-500 text-sm italic">
            No data loaded. Please select a symbol and fetch data.
          </p>
        </div>
      </div>
    </div>
  );
};

export default DataExplorer;
EOT

mkdir -p frontend/src/components/layout
cat > frontend/src/components/layout/Header.tsx << 'EOT'
import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm z-10">
      <div className="flex items-center justify-between h-16 px-6">
        <h1 className="text-xl font-semibold text-gray-800">ML Trading System</h1>
        <div className="flex items-center space-x-4">
          {/* User profile, notifications, etc. */}
          <button className="p-1 rounded-full text-gray-600 hover:text-gray-900 focus:outline-none">
            <span className="sr-only">View notifications</span>
            <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 00-6-6H9a6 6 0 00-6 6v3.159c0 .538-.214 1.055-.595 1.436L1 17h5m0 0h6m-6 0v3m6-3v3" />
            </svg>
          </button>
          <div className="relative">
            <button className="flex items-center text-sm font-medium text-gray-700 rounded-full hover:text-gray-900 focus:outline-none">
              <span className="sr-only">Open user menu</span>
              <div className="h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center text-gray-700">
                U
              </div>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
EOT

cat > frontend/src/components/layout/Sidebar.tsx << 'EOT'
import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar: React.FC = () => {
  return (
    <aside className="bg-gray-800 text-white w-64 space-y-6 py-7 px-2 absolute inset-y-0 left-0 transform -translate-x-full md:relative md:translate-x-0 transition duration-200 ease-in-out">
      <div className="flex flex-col h-full">
        <div className="space-y-3">
          <div className="flex items-center justify-center">
            <h2 className="text-xl font-bold">ML Trading</h2>
          </div>
          <div className="flex-1">
            <ul className="pt-2 pb-4 space-y-1 text-sm">
              <li className="rounded-sm">
                <NavLink 
                  to="/" 
                  className={({ isActive }) => 
                    `flex items-center p-2 space-x-3 rounded-md ${isActive ? 'bg-gray-700' : 'hover:bg-gray-700'}`
                  }
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                  </svg>
                  <span>Dashboard</span>
                </NavLink>
              </li>
              <li className="rounded-sm">
                <NavLink 
                  to="/data" 
                  className={({ isActive }) => 
                    `flex items-center p-2 space-x-3 rounded-md ${isActive ? 'bg-gray-700' : 'hover:bg-gray-700'}`
                  }
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                  </svg>
                  <span>Data Explorer</span>
                </NavLink>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
EOT

echo "Creating additional frontend components..."

mkdir -p frontend/src/hooks
cat > frontend/src/hooks/useApi.ts << 'EOT'
import { useState, useCallback } from 'react';
import axios, { AxiosRequestConfig } from 'axios';

// Base API URL from environment variables
const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

interface ApiResponse<T> {
  data: T | null;
  error: Error | null;
  loading: boolean;
}

export function useApi<T>() {
  const [state, setState] = useState<ApiResponse<T>>({
    data: null,
    error: null,
    loading: false,
  });

  const request = useCallback(
    async (endpoint: string, options: AxiosRequestConfig = {}) => {
      try {
        setState({ data: null, error: null, loading: true });
        
        const url = endpoint.startsWith('http') ? endpoint : `${API_URL}${endpoint}`;
        const response = await axios({ ...options, url });
        
        setState({ data: response.data, error: null, loading: false });
        return response.data;
      } catch (error) {
        const errorObject = error instanceof Error ? error : new Error('An unknown error occurred');
        setState({ data: null, error: errorObject, loading: false });
        throw errorObject;
      }
    },
    []
  );

  return { ...state, request };
}

export default useApi;
EOT

mkdir -p frontend/src/services
cat > frontend/src/services/api.ts << 'EOT'
import axios from 'axios';

// Base API URL from environment variables
const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = localStorage.getItem('token');
    
    // If token exists, add to headers
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle 401 Unauthorized
    if (error.response && error.response.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

export default api;
EOT

mkdir -p frontend/src/components/common
cat > frontend/src/components/common/Button.tsx << 'EOT'
import React, { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'warning' | 'info';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  fullWidth?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  fullWidth = false,
  className = '',
  disabled,
  ...props
}) => {
  // Base classes
  const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  // Variant classes
  const variantClasses = {
    primary: 'bg-indigo-600 hover:bg-indigo-700 text-white focus:ring-indigo-500',
    secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800 focus:ring-gray-500',
    success: 'bg-green-600 hover:bg-green-700 text-white focus:ring-green-500',
    danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500',
    warning: 'bg-yellow-500 hover:bg-yellow-600 text-white focus:ring-yellow-500',
    info: 'bg-blue-500 hover:bg-blue-600 text-white focus:ring-blue-500',
  };
  
  // Size classes
  const sizeClasses = {
    sm: 'px-2.5 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base',
  };
  
  // Width class
  const widthClass = fullWidth ? 'w-full' : '';
  
  // Disabled class
  const disabledClass = disabled || isLoading ? 'opacity-60 cursor-not-allowed' : '';
  
  // Combine all classes
  const buttonClasses = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${widthClass} ${disabledClass} ${className}`;
  
  return (
    <button className={buttonClasses} disabled={disabled || isLoading} {...props}>
      {isLoading ? (
        <>
          <svg className="animate-spin -ml-1 mr-3 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading...
        </>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;
EOT

cat > frontend/src/components/common/Card.tsx << 'EOT'
import React, { ReactNode } from 'react';

interface CardProps {
  title?: string;
  children: ReactNode;
  className?: string;
  footer?: ReactNode;
}

const Card: React.FC<CardProps> = ({ title, children, className = '', footer }) => {
  return (
    <div className={`bg-white overflow-hidden shadow rounded-lg ${className}`}>
      {title && (
        <div className="border-b border-gray-200 px-4 py-5 sm:px-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">{title}</h3>
        </div>
      )}
      <div className="px-4 py-5 sm:p-6">{children}</div>
      {footer && (
        <div className="border-t border-gray-200 px-4 py-4 sm:px-6">{footer}</div>
      )}
    </div>
  );
};

export default Card;
EOT

mkdir -p frontend/src/components/charts
cat > frontend/src/components/charts/PriceChart.tsx << 'EOT'
import React, { useEffect, useRef } from 'react';
import { createChart, ColorType } from 'lightweight-charts';

interface PriceChartProps {
  data: {
    time: string;
    open: number;
    high: number;
    low: number;
    close: number;
  }[];
  height?: number;
}

const PriceChart: React.FC<PriceChartProps> = ({ data, height = 300 }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (!chartContainerRef.current || !data.length) return;
    
    const chartContainer = chartContainerRef.current;
    
    // Clear any existing chart
    chartContainer.innerHTML = '';
    
    // Create the chart
    const chart = createChart(chartContainer, {
      height,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
      timeScale: {
        borderColor: '#d1d5db',
      },
    });
    
    // Add the candlestick series
    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#4CAF50',
      downColor: '#FF5252',
      borderVisible: false,
      wickUpColor: '#4CAF50',
      wickDownColor: '#FF5252',
    });
    
    // Set the data
    candlestickSeries.setData(data);
    
    // Fit content to container
    chart.timeScale().fitContent();
    
    // Handle resizing
    const handleResize = () => {
      chart.applyOptions({ width: chartContainer.clientWidth });
    };
    
    window.addEventListener('resize', handleResize);
    
    // Cleanup on unmount
    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, height]);
  
  return <div ref={chartContainerRef} className="w-full"></div>;
};

export default PriceChart;
EOT

cat > frontend/Dockerfile << 'EOT'
FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
EOT

echo "Creating Docker configuration files..."

# Docker related files
mkdir -p docker/postgres
mkdir -p docker/nginx

cat > docker/postgres/init.sql << 'EOT'
-- Create TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create hypertable function for easier table creation
CREATE OR REPLACE FUNCTION create_market_data_hypertable(
  schema_name TEXT, 
  table_name TEXT
) 
RETURNS VOID AS $
BEGIN
  EXECUTE format('SELECT create_hypertable(%L, %L, chunk_time_interval => interval %L)',
            schema_name || '.' || table_name, 'timestamp', '1 day');
END;
$ LANGUAGE plpgsql;
EOT

cat > docker/nginx/default.conf << 'EOT'
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOT

# Root level files
cat > docker-compose.yml << 'EOT'
version: '3.8'

services:
  postgres:
    image: timescale/timescaledb:latest-pg15
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data/
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    env_file:
      - .env
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_DB=${POSTGRES_DB}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.tasks.worker worker --loglevel=info
    volumes:
      - ./backend:/app
    env_file:
      - .env
    depends_on:
      - backend
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    env_file:
      - .env
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
EOT

cat > docker-compose.dev.yml << 'EOT'
version: '3.8'

services:
  postgres:
    image: timescale/timescaledb:latest-pg15
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data/
      - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    env_file:
      - .env
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_DB=${POSTGRES_DB}

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - postgres
      - redis

  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.tasks.worker worker --loglevel=info
    volumes:
      - ./backend:/app
    env_file:
      - .env
    depends_on:
      - backend
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    env_file:
      - .env
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
EOT

cat > .env.example << 'EOT'
# Backend
POSTGRES_SERVER=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ml_trading
REDIS_HOST=redis
REDIS_PORT=6379
SECRET_KEY=your-super-secret-key-here-at-least-32-characters

# External APIs
YAHOO_FINANCE_API_KEY=
ALPHA_VANTAGE_API_KEY=
FRED_API_KEY=

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
EOT

cat > .gitignore << 'EOT'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
venv/
ENV/

# Node
node_modules/
npm-debug.log
yarn-error.log
yarn-debug.log
.pnpm-debug.log
.DS_Store
coverage/
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# Docker
.docker/

# Database
*.sqlite3

# Logs
logs/
*.log

# Distribution / packaging
dist/
build/
*.egg-info/
EOT

cat > Makefile << 'EOT'
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
EOT

cat > README.md << 'EOT'
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
EOT

mkdir -p docs/architecture
mkdir -p docs/api

cat > docs/setup.md << 'EOT'
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
EOT

# Create ML infrastructure models
mkdir -p backend/app/models

# Create directories for ML modules
mkdir -p backend/ml/models

echo "Creating script completion handler..."

# Finish script with success message
echo
echo "============================================="
echo "ML Trading System structure created successfully!"
echo "============================================="
echo 
echo "To start development:"
echo "1. Copy .env.example to .env and update the values"
echo "   cp .env.example .env"
echo
echo "2. Install dependencies"
echo "   make setup"
echo
echo "3. Start the development environment"
echo "   make dev"
echo
echo "Access the application at:"
echo "- API: http://localhost:8000"
echo "- Frontend: http://localhost:3000"
echo "- API Documentation: http://localhost:8000/docs"
echo
echo "Happy coding!"
echo "============================================="

cd ..
echo "Setup complete in directory: ml-trading-system"
import os

# Project base
BASE_DIR = "mvp_trader"

# Directory structure
DIRS = [
    "backend/app/api",
    "backend/app/core",
    "backend/app/db",
    "backend/app/services",
    "backend/app/tasks",
    "backend/app/models",
    "backend/app/utils",
    "ml_pipeline/data",
    "ml_pipeline/features",
    "ml_pipeline/models",
    "ml_pipeline/evaluation",
    "ml_pipeline/inference",
    "ml_pipeline/utils",
    "frontend/public",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/services",
    "frontend/src/hooks",
    "frontend/src/store",
    "tests/unit/backend",
    "tests/unit/ml_pipeline",
    "tests/integration",
    "tests/e2e",
    "docs/architecture",
    "docs/api",
    "docs/user_guides",
    "docs/development",
    "infrastructure/terraform",
    "infrastructure/k8s",
    "monitoring/dashboards",
    "monitoring/alerts",
    "monitoring/logging",
    "schemas",
    "deployment/traefik",
    "deployment/nginx",
    "scripts",
]

# Basic files with optional content
FILES = {
    ".env": "",
    ".env.example": "",
    "README.md": "# MVP Trader\n",
    "Makefile": "setup:\n\tpoetry install\n\nrun-backend:\n\tuvicorn backend.app.main:app --reload\n",
    "pyproject.toml": "[tool.poetry]\nname = \"mvp-trader\"\nversion = \"0.1.0\"\ndescription = \"MVP ML Trading System\"\nauthors = [\"You <you@example.com>\"]\n\n[tool.poetry.dependencies]\npython = \"^3.10\"\nfastapi = \"^0.104\"\npydantic = \"^2.0\"\n\n[build-system]\nrequires = [\"poetry-core\"]\nbuild-backend = \"poetry.core.masonry.api\"\n",
    "backend/app/main.py": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/health')\ndef health_check():\n    return {\"status\": \"ok\"}\n",
    "schemas/market_data.py": "from pydantic import BaseModel\n\nclass MarketData(BaseModel):\n    timestamp: str\n    open: float\n    high: float\n    low: float\n    close: float\n    volume: float\n",
}

def scaffold():
    os.makedirs(BASE_DIR, exist_ok=True)
    os.chdir(BASE_DIR)
    for d in DIRS:
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, ".gitkeep"), "w").close()
    for path, content in FILES.items():
        with open(path, "w") as f:
            f.write(content)

if __name__ == "__main__":
    scaffold()
    print("Project scaffold created in ./mvp_trader")

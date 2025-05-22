setup:
	poetry install

run-backend:
	uvicorn backend.app.main:app --reload

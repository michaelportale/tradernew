from fastapi import APIRouter
from app.worker.tasks import simulate_training

router = APIRouter()

@router.post("/start/{model}")
async def start_training(model: str):
    task = simulate_training.delay(model)
    return {"message": f"Training started for model: {model}", "task_id": task.id}
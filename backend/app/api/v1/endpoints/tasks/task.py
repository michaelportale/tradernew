from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List, Optional
from celery.result import AsyncResult

from app.tasks.worker import celery_app

router = APIRouter()


@router.get("/{task_id}", response_model=Dict[str, Any])
async def get_task_status(task_id: str):
    """
    Get the status of a Celery task by its ID
    """
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        
        response = {
            "task_id": task_id,
            "status": task_result.status,
        }
        
        # Include the result if the task is completed
        if task_result.ready():
            if task_result.successful():
                response["result"] = task_result.result
            else:
                response["error"] = str(task_result.result)
                
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error retrieving task status: {str(e)}"
        )


@router.post("/{task_id}/revoke", response_model=Dict[str, Any])
async def revoke_task(task_id: str, terminate: bool = False):
    """
    Revoke a running or pending Celery task
    
    - terminate: If True, the task will be forcefully terminated if it's already running
    """
    try:
        celery_app.control.revoke(task_id, terminate=terminate)
        
        return {
            "task_id": task_id,
            "status": "revoked",
            "message": f"Task {task_id} has been revoked"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error revoking task: {str(e)}"
        )


@router.get("/", response_model=Dict[str, Any])
async def get_active_tasks():
    """
    Get a list of currently active tasks
    """
    try:
        # Get active tasks from all workers
        inspector = celery_app.control.inspect()
        
        # Combine active tasks from all workers
        active_tasks = {}
        
        # Get active, reserved, and scheduled tasks
        active = inspector.active() or {}
        reserved = inspector.reserved() or {}
        scheduled = inspector.scheduled() or {}
        
        # Combine the results
        for worker, tasks in active.items():
            active_tasks[worker] = {
                "active": tasks,
                "reserved": reserved.get(worker, []),
                "scheduled": scheduled.get(worker, [])
            }
        
        return {
            "active_workers": list(active_tasks.keys()),
            "tasks": active_tasks
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving active tasks: {str(e)}"
        ) 
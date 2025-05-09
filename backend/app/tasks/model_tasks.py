from celery import Task
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import os
import pickle
import numpy as np
import pandas as pd
from loguru import logger

from app.tasks.worker import celery_app
from app.core.config import settings
from app.models.ml_models import MLModel

# Create a database engine and session for Celery using synchronous connection
sync_db_uri = str(settings.SQLALCHEMY_DATABASE_URI).replace("+asyncpg", "")
engine = create_engine(sync_db_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class ModelTrainingTask(Task):
    """
    Custom Celery Task for model training
    """
    abstract = True
    
    def __init__(self):
        super().__init__()
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """
        Handler called after the task returns
        """
        logger.info(f"Task {task_id} completed with status: {status}")


@celery_app.task(
    base=ModelTrainingTask,
    bind=True,
    max_retries=3,
    default_retry_delay=60 * 5,  # 5 minutes
    queue="model_tasks",
)
def train_model_task(self, model_id: int):
    """
    Train a machine learning model
    """
    logger.info(f"Starting training for model ID: {model_id}")
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Get the model from the database
        model = db.query(MLModel).filter(MLModel.id == model_id).first()
        
        if not model:
            logger.error(f"Model with ID {model_id} not found")
            return {"status": "error", "message": f"Model with ID {model_id} not found"}
        
        # Update model status
        model.is_active = False
        db.commit()
        
        # Placeholder for actual model training logic
        # In a real implementation, you would:
        # 1. Load data from the database
        # 2. Preprocess the data
        # 3. Train the model using the parameters from model.parameters
        # 4. Evaluate the model
        # 5. Save the model to disk
        # 6. Update the model record in the database
        
        # Simulate model training with a delay
        import time
        time.sleep(5)  # Simulate a 5-second training process
        
        # Create a model directory if it doesn't exist
        os.makedirs("models", exist_ok=True)
        
        # Create a dummy model (just a dictionary in this case)
        dummy_model = {
            "name": model.name,
            "type": model.model_type,
            "features": model.features,
            "target": model.target,
            "params": model.parameters,
        }
        
        # Save the dummy model to disk
        model_path = f"models/model_{model_id}.pkl"
        with open(model_path, "wb") as f:
            pickle.dump(dummy_model, f)
        
        # Update the model record in the database
        model.model_path = model_path
        model.trained_at = datetime.utcnow()
        model.is_active = True
        model.metrics = {
            "accuracy": 0.85,
            "precision": 0.82,
            "recall": 0.87,
            "f1": 0.84,
        }
        
        db.commit()
        
        logger.info(f"Training completed for model ID: {model_id}")
        
        return {
            "status": "success",
            "model_id": model_id,
            "message": "Model training completed successfully",
        }
    except Exception as e:
        logger.error(f"Error training model {model_id}: {str(e)}")
        db.rollback()
        
        # Update model status to indicate failure
        model = db.query(MLModel).filter(MLModel.id == model_id).first()
        if model:
            model.is_active = False
            model.metrics = {"error": str(e)}
            db.commit()
            
        # Retry the task
        raise self.retry(exc=e)
    finally:
        db.close() 
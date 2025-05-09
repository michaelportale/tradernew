from celery import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from loguru import logger

from app.tasks.worker import celery_app
from app.core.config import settings
from app.models.market_data import MarketData

# Create a database engine and session for Celery using synchronous connection
sync_db_uri = str(settings.SQLALCHEMY_DATABASE_URI).replace("+asyncpg", "")
engine = create_engine(sync_db_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DataProcessingTask(Task):
    """
    Custom Celery Task for data processing
    """
    abstract = True
    
    def __init__(self):
        super().__init__()
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """
        Handler called after the task returns
        """
        logger.info(f"Data task {task_id} completed with status: {status}")


class DataFetchingTask(Task):
    """
    Custom Celery Task for data fetching
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
    base=DataFetchingTask,
    bind=True,
    max_retries=3,
    default_retry_delay=60 * 5,  # 5 minutes
    queue="data_tasks",
)
def fetch_market_data_task(self, symbol: str, days: int = 30):
    """
    Fetch market data for a symbol for the last X days
    """
    logger.info(f"Fetching market data for symbol: {symbol} for the last {days} days")
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Calculate date range
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # In a real implementation, you would:
        # 1. Call a data provider API to get the data
        # 2. Process the response
        # 3. Insert the data into the database
        
        # Generate dummy data for demonstration
        dummy_data = []
        current_date = start_date
        
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Skip weekends
                # Generate random OHLCV data
                import random
                base_price = random.uniform(100, 200)
                high_price = base_price * random.uniform(1.01, 1.05)
                low_price = base_price * random.uniform(0.95, 0.99)
                close_price = random.uniform(low_price, high_price)
                volume = random.randint(100000, 1000000)
                
                # Create a market data entry
                market_data = MarketData(
                    symbol=symbol,
                    timestamp=datetime.combine(current_date, datetime.min.time()),
                    open=base_price,
                    high=high_price,
                    low=low_price,
                    close=close_price,
                    volume=volume,
                    adjusted_close=close_price,
                )
                
                # Add to the database
                db.add(market_data)
                
                dummy_data.append(market_data)
            
            current_date += timedelta(days=1)
        
        # Commit the changes
        db.commit()
        
        logger.info(f"Fetched {len(dummy_data)} data points for {symbol}")
        
        return {
            "status": "success",
            "symbol": symbol,
            "data_points": len(dummy_data),
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {str(e)}")
        db.rollback()
        
        # Retry the task
        raise self.retry(exc=e)
    finally:
        db.close()


@celery_app.task(
    base=DataProcessingTask,
    bind=True,
    max_retries=3,
    default_retry_delay=60 * 2,  # 2 minutes
    queue="data_tasks",
)
def process_market_data_task(self, symbol: str, start_date: str = None, end_date: str = None):
    """
    Process market data for a symbol
    """
    logger.info(f"Processing market data for {symbol}")
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Set default dates if not provided
        if not end_date:
            end_date = datetime.utcnow().strftime("%Y-%m-%d")
        if not start_date:
            # Default to 30 days before end date
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            start_dt = end_dt - timedelta(days=30)
            start_date = start_dt.strftime("%Y-%m-%d")
        
        # Placeholder for actual data processing logic
        # In a real implementation, you would:
        # 1. Fetch data from an external API or database
        # 2. Process and clean the data
        # 3. Calculate technical indicators
        # 4. Save the processed data to the database
        
        # Simulate data processing with a delay
        import time
        time.sleep(3)  # Simulate a 3-second processing time
        
        # Create dummy processed data
        logger.info(f"Data processing completed for {symbol} from {start_date} to {end_date}")
        
        return {
            "status": "success",
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "message": "Market data processing completed successfully",
        }
    except Exception as e:
        logger.error(f"Error processing data for {symbol}: {str(e)}")
        # Retry the task
        raise self.retry(exc=e)
    finally:
        db.close()


@celery_app.task(
    base=DataProcessingTask,
    bind=True,
    queue="data_tasks",
)
def calculate_indicators_task(self, symbol: str, indicators: list = None):
    """
    Calculate technical indicators for a symbol
    """
    logger.info(f"Calculating indicators for {symbol}")
    
    # Default indicators if none provided
    if not indicators:
        indicators = ["sma", "ema", "rsi", "macd"]
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Placeholder for actual indicator calculation logic
        # In a real implementation, you would:
        # 1. Fetch price data for the symbol
        # 2. Calculate the requested indicators
        # 3. Save the indicators to the database
        
        # Simulate indicator calculation with a delay
        import time
        time.sleep(2)  # Simulate a 2-second processing time
        
        logger.info(f"Indicator calculation completed for {symbol}: {', '.join(indicators)}")
        
        return {
            "status": "success",
            "symbol": symbol,
            "indicators": indicators,
            "message": "Technical indicators calculated successfully",
        }
    except Exception as e:
        logger.error(f"Error calculating indicators for {symbol}: {str(e)}")
        # Retry the task
        raise self.retry(exc=e)
    finally:
        db.close() 
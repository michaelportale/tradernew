import logging
import sys
from typing import Any, Dict, List, Optional

from loguru import logger
from pydantic import BaseModel, Field

class LogConfig(BaseModel):
    """Logging configuration"""
    LOGGER_NAME: str = "ml_trading"
    LOG_FORMAT: str = "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: Optional[str] = None
    JSON_LOGS: bool = False
    
    class Config:
        env_prefix = "LOG_"

log_config = LogConfig()

class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.
    See https://loguru.readthedocs.io/en/stable/overview.html
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging():
    """Configure logging"""
    # Intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(log_config.LOG_LEVEL)
    
    # Remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
        
    # Configure loguru
    logger_config = {
        "handlers": [
            {
                "sink": sys.stdout, 
                "format": log_config.LOG_FORMAT,
                "level": log_config.LOG_LEVEL
            }
        ]
    }
    
    # Add file logger if specified
    if log_config.LOG_FILE_PATH:
        logger_config["handlers"].append({
            "sink": log_config.LOG_FILE_PATH,
            "format": log_config.LOG_FORMAT,
            "level": log_config.LOG_LEVEL,
            "rotation": "20 MB",
            "retention": "1 month"
        })
    
    logger.configure(**logger_config) 
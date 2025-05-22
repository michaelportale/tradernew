# app/core/logging.py
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="DEBUG", format="<green>{time}</green> | <level>{level}</level> | {message}")
import sys
import os
from loguru import logger
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGS_DIR = os.path.join(BASE_DIR, 'app/logs')
os.makedirs(LOGS_DIR, exist_ok=True)

LOGURU_FORMAT = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"

logger.remove()

logger.add(
    sys.stdout,
    format=LOGURU_FORMAT,
    level="DEBUG",
    enqueue=True
)

logger.add(
    os.path.join(LOGS_DIR, "error.log"),
    format=LOGURU_FORMAT,
    level="ERROR",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    enqueue=True
)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = logger.level(record.levelname).name if logger.level(record.levelname) else record.levelno
        message = self.format(record)
        logger.log(level, message)


logging.getLogger().handlers = [InterceptHandler()]


class ErrorLogFilter(logging.Filter):
    def filter(self, record):
        return hasattr(record, 'is_verified') and not record.is_verified


logger.add(
    os.path.join(LOGS_DIR, "info.log"),
    format=LOGURU_FORMAT,
    level="INFO",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    enqueue=True
)


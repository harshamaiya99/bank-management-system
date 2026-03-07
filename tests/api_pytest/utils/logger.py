import sys
import os
from pathlib import Path
from loguru import logger

# Define a central logs directory at the root of the project
LOG_DIR = Path(__file__).parent.parent.parent.parent / "tests" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = str(LOG_DIR / "test_logs_{time:YYYY-MM-DD_HH-mm-ss}.log")


def setup_logger():
    # Remove Loguru's default handler to prevent duplicate logs
    logger.remove()

    # Define a clean, readable format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name: <35}</cyan>:<cyan>{function: <20}</cyan>:<cyan>{line: >4}</cyan> | "
        # "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # 1. Console Sink (For local execution)
    logger.add(
        sys.stdout,
        format=log_format,
        colorize=True,
        level="INFO"  # Keeps terminal clean, showing only high-level steps
    )

    # 2. File Sink (For detailed history)
    logger.add(
        LOG_FILE,
        format=log_format,
        rotation="10 MB",  # Create a new log file if it exceeds 10MB
        retention=5,  # Keep the last 5 test run logs, delete older ones
        level="DEBUG",  # Capture everything, including raw JSON payloads
        enqueue=True  # Makes logging thread-safe for parallel Pytest runs
    )

    return logger


# Export the configured instance
api_logger = setup_logger()
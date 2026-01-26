import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler
from contextvars import ContextVar

# 1. Context Variables (Global)
request_id_ctx = ContextVar("request_id", default="-")
process_id_ctx = ContextVar("process_id", default="-")


class ContextFilter(logging.Filter):
    """
    Injects IDs into every log record (File OR Terminal).
    """

    def filter(self, record):
        record.request_id = request_id_ctx.get()
        record.process_id = process_id_ctx.get()
        return True


def setup_logging():
    # 2. Create 'logs' directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # 3. Define Log Format
    log_format = (
        "[%(asctime)s] [%(levelname)s] "
        "[X-Process-Id:%(process_id)s] [X-Request-Id:%(request_id)s] - %(message)s"
    )
    formatter = logging.Formatter(log_format)

    # 4. Create the Context Filter
    ctx_filter = ContextFilter()

    # --- HANDLER 1: Console (Terminal) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(ctx_filter)

    # --- HANDLER 2: File (Rotating Daily) ---
    file_handler = TimedRotatingFileHandler(
        filename="logs/banking_system.log",
        when="midnight",  # Rotate every night at 00:00
        interval=1,
        backupCount=30,  # Keep logs for 30 days
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(ctx_filter)

    # 5. Configure Root Logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear existing handlers to avoid duplicates on reload
    if logger.handlers:
        logger.handlers = []

    # Add both handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Silence noisy default logs from libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
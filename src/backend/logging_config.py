import logging
import sys
from contextvars import ContextVar

# 1. Global Context Variables (Default to '-' if missing)
request_id_ctx = ContextVar("request_id", default="-")
process_id_ctx = ContextVar("process_id", default="-")


class ContextFilter(logging.Filter):
    """
    Injects IDs into every log record automatically.
    """

    def filter(self, record):
        record.request_id = request_id_ctx.get()
        record.process_id = process_id_ctx.get()
        return True


def setup_logging():
    # 2. Define Log Format: [Time] [Level] [ProcessID] [RequestID] Message
    log_format = (
        "[%(asctime)s] [%(levelname)s] "
        "[X-Process-Id:%(process_id)s] [X-Request-Id:%(request_id)s] - %(message)s"
    )

    # 3. Configure the Logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Reset handlers to prevent duplicate logs on reload
    if logger.handlers:
        logger.handlers = []

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(log_format))
    handler.addFilter(ContextFilter())  # <--- Add the magic filter

    logger.addHandler(handler)

    # Silence noisy default logs
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
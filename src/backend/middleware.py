import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from logging_config import request_id_ctx, process_id_ctx

logger = logging.getLogger(__name__)


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. EXTRACT OR GENERATE IDs
        # If frontend sent X-Request-Id, use it; otherwise generate new UUID
        req_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())

        # If frontend sent X-Process-Id, use it; otherwise mark as N/A
        proc_id = request.headers.get("X-Process-Id") or "N/A"

        # 2. SET CONTEXT (So logs can see them)
        req_token = request_id_ctx.set(req_id)
        proc_token = process_id_ctx.set(proc_id)

        # 3. LOG THE START
        logger.info(f"Incoming Request: {request.method} {request.url.path}")

        try:
            # 4. PROCESS THE REQUEST
            response = await call_next(request)

            # 5. INJECT HEADERS INTO RESPONSE
            response.headers["X-Request-Id"] = req_id
            if proc_id != "N/A":
                response.headers["X-Process-Id"] = proc_id

            return response

        finally:
            # 6. CLEANUP (Reset context variables)
            request_id_ctx.reset(req_token)
            process_id_ctx.reset(proc_token)
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from logging_config import request_id_ctx, process_id_ctx

logger = logging.getLogger(__name__)


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. EXTRACT OR GENERATE IDs
        req_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
        proc_id = request.headers.get("X-Process-Id") or "N/A"

        # 2. SET CONTEXT
        req_token = request_id_ctx.set(req_id)
        proc_token = process_id_ctx.set(proc_id)

        try:
            # 3. PROCESS THE REQUEST
            response = await call_next(request)

            # --- NEW LOG LINE HERE ---
            logger.info(f"{request.method} {request.url.path} - HTTP/1.1 {response.status_code}")

            # 4. INJECT HEADERS INTO RESPONSE
            response.headers["X-Request-Id"] = req_id
            if proc_id != "N/A":
                response.headers["X-Process-Id"] = proc_id

            return response

        finally:
            # 5. CLEANUP
            request_id_ctx.reset(req_token)
            process_id_ctx.reset(proc_token)
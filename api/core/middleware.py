import time
import uuid
import logging
from fastapi import Request

logger = logging.getLogger("request_logger")


async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    # Attach request id to request state
    request.state.request_id = request_id

    logger.info({
        "event": "request_start",
        "method": request.method,
        "url": str(request.url),
        "request_id": request_id
    })

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info({
        "event": "request_end",
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "process_time_sec": round(process_time, 4),
        "request_id": request_id
    })

    return response

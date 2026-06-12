from fastapi import Request
from fastapi.responses import JSONResponse
from api.exceptions import DatabaseError


async def database_exception_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )

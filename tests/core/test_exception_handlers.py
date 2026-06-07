from starlette.requests import Request

from api.core.exception_handlers import (database_exception_handler)
from api.exceptions import DatabaseError

import pytest


@pytest.mark.asyncio
async def test_database_exception_handler():

    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/"
        }
    )

    exc = DatabaseError("Database failure")

    response = await database_exception_handler(
        request,
        exc
    )

    assert response.status_code == 500

    assert response.body == (
        b'{"error":"Database failure"}'
    )
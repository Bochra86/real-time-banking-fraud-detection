from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest

from api.main import app
from api.database.dependencies import get_db


def override_get_db():
    db = MagicMock()
    yield db


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


@pytest.fixture
def test_client():
    return client

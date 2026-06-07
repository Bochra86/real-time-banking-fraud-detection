from fastapi.testclient import TestClient
from api.main import app
import pytest

client = TestClient(app)

@pytest.fixture
def test_client():
    return client
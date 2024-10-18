import pytest
from fastapi.testclient import TestClient
from fastapi import Response
from unittest.mock import MagicMock

from user_microservice.routes.user_route import user_route, is_authenticate

client = TestClient(user_route)

@pytest.fixture
def mock_is_authenticate():
    return MagicMock()


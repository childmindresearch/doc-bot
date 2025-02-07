"""Endpoint tests for the embeddings endpoints."""

from typing import Any

import moto
import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core import auth
from app.main import app

client = TestClient(app)

app.dependency_overrides[auth.check_api_key] = lambda: None


@pytest.fixture
def valid_post_tts_payload() -> dict[str, Any]:
    """A valid payload for the POStT /v1/embeddings endpoint."""
    return {"model": "...", "input": "example text", "voice": "Ruth"}


@moto.mock_aws
def test_post_tts_endpoint(
    valid_post_tts_payload: dict[str, Any],
) -> None:
    """Tests the happy-path of the post-audio endpoint."""
    response = client.post("/v1/audio/speech", json=valid_post_tts_payload)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.content, bytes)

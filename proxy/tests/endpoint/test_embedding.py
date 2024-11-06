"""Endpoint tests for the embeddings endpoints."""

import io
import json
from typing import Any

import pytest
import pytest_mock
from app.core import auth
from app.main import app
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)

app.dependency_overrides[auth.check_api_key] = lambda: None


@pytest.fixture
def valid_post_embedding_payload() -> dict[str, Any]:
    """A valid payload for the POStT /v1/embeddings endpoint."""
    return {
        "model": "aws/cohere.embed-english-v3",
        "input": ["example text"],
    }


def test_post_embedding_endpoint(
    valid_post_embedding_payload: dict[str, Any],
    mocker: pytest_mock.MockerFixture,
) -> None:
    """Tests the happy-path of the post-embedding endpoint."""
    mock_boto_client = mocker.patch("app.routers.embeddings.controller.boto3.client")
    mock_boto_client.return_value.invoke_model.return_value = {
        "body": io.StringIO(
            json.dumps(
                {
                    "embeddings": [[0.1, 0.2, 0.3]],
                    "id": "123",
                    "response_type": "embedding",
                    "texts": ["example text"],
                },
            ),
        ),
    }

    response = client.post("/v1/embeddings", json=valid_post_embedding_payload)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["model"] == valid_post_embedding_payload["model"]
    assert response_data["data"][0]["embedding"] == [0.1, 0.2, 0.3]

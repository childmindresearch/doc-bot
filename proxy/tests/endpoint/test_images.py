"""Endpoint tests for the embeddings endpoints."""

import io
import json
from typing import Any

import pytest
import pytest_mock
from fastapi import status
from fastapi.testclient import TestClient

from app.core import auth
from app.main import app

client = TestClient(app)

app.dependency_overrides[auth.check_api_key] = lambda: None


@pytest.fixture
def valid_post_embedding_payload() -> dict[str, Any]:
    """A valid payload for the POStT /v1/embeddings endpoint."""
    return {
        "model": "aws/stability.sd3-large-v1:0",
        "prompt": "example text",
        "n": 1,
        "size": "512x512",
        "response_format": "b64_json",
    }


def test_post_image_generation_endpoint(
    valid_post_embedding_payload: dict[str, Any],
    mocker: pytest_mock.MockerFixture,
) -> None:
    """Tests the happy-path of the post-embedding endpoint."""
    mock_boto_client = mocker.patch("app.routers.images.controller.boto3.client")
    mock_boto_client.return_value.invoke_model.return_value = {
        "body": io.StringIO(
            json.dumps(
                {
                    "images": ["abc"],
                },
            ),
        ),
    }

    response = client.post("/v1/images/generations", json=valid_post_embedding_payload)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["data"][0]["b64_json"] == "abc"
    assert (
        response_data["data"][0]["revised_prompt"]
        == valid_post_embedding_payload["prompt"]
    )

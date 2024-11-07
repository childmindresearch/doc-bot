"""Controller for the embeddings endpoints."""

import json
from collections.abc import Iterable

import boto3
import fastapi
import pydantic
from fastapi import status

from app.core import config
from app.routers.embeddings import schemas

settings = config.get_settings()
logger = config.get_logger()


def post_embedding(
    payload: schemas.PostEmbeddingRequest,
) -> schemas.PostEmbeddingResponse:
    """Gets the embedding of a string.

    Args:
        payload: The request body.

    Returns:
        The embedding response.
    """
    if payload.provider == "aws":
        logger.debug("Running Azure Embedding.")
        return _run_aws_embedding(payload)
    raise fastapi.HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unknown provider.",
    )


@pydantic.dataclasses.dataclass
class CohereEmbeddingResponse:
    """Dataclass for the response of Cohere's embedding models."""

    embeddings: list[list[float]]
    id: str
    response_type: str
    texts: list[str]


def _run_aws_embedding(
    payload: schemas.PostEmbeddingRequest,
) -> schemas.PostEmbeddingResponse:
    """Runs an embedding on AWS.

    Args:
        payload: The payload as provided to the POST embedding endpoint.

    Returns:
        The embedding response.
    """
    if isinstance(payload.input, str):
        payload.input = [payload.input]

    responses = []
    n_chunks_per_request = 64
    for index in range(0, len(payload.input), n_chunks_per_request):
        inputs = payload.input[
            index : min(index + n_chunks_per_request, len(payload.input))
        ]
        responses.append(
            _get_cohere_response(inputs, payload.model_name),
        )

    position = 0
    embedding_data = []
    for response in responses:
        for index, text in enumerate(response.texts):
            embedding_data.append(
                schemas.EmbeddingData(
                    index=position,
                    embedding=response.embeddings[index],
                ),
            )
            position += len(text)

    return schemas.PostEmbeddingResponse(
        data=embedding_data,
        model=payload.model,
    )


def _get_cohere_response(inputs: Iterable[str], model: str) -> CohereEmbeddingResponse:
    """Gets the AWS response for Cohere models.

    Args:
        inputs: List of strings to embed.
        model: The model to use for embedding.

    Returns:
        The embedding response.
    """
    body = json.dumps(
        {
            "texts": inputs,
            "input_type": "search_document",
        },
    )

    bedrock = boto3.client(
        service_name="bedrock-runtime",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY.get_secret_value(),
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY.get_secret_value(),
    )

    response = bedrock.invoke_model(
        body=body,
        modelId=model,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    return CohereEmbeddingResponse(**response_body)

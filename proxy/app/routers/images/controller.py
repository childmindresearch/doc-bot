"""Business logic of the images router."""

import json

import boto3
import fastapi
from fastapi import status

from app.core import config
from app.routers.images import schemas

settings = config.get_settings()


def post_image_generation(
    payload: schemas.PostImageGenerationRequest,
) -> schemas.PostImageGenerationResponse:
    """Performs the image generation business logic.

    Args:
        payload: The request body.

    Returns:
        The images, following OpenAI's API specification.
    """
    if payload.provider == "aws":
        images = [_aws_image_generation(payload) for _ in range(payload.n)]
    else:
        raise fastapi.HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Unknown provider.",
        )
    return schemas.PostImageGenerationResponse(data=images)


def _aws_image_generation(
    payload: schemas.PostImageGenerationRequest,
) -> schemas.PostImageGenerationImage:
    """Runs image generation on AWS.

    Args:
        payload: The request body.

    Returns:
        A single image and its (revised) prompt. For the curent models, revised and
        input prompts are identical.
    """
    body = json.dumps(
        {
            "prompt": payload.prompt,
            "mode": "text-to-image",
            "aspect_ratio": "1:1",
            "output_format": "jpeg",
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
        modelId=payload.model_name,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    return schemas.PostImageGenerationImage(
        b64_json=response_body["images"][0],
        revised_prompt=payload.prompt,
    )

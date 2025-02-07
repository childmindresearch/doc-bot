"""Controller for the embeddings endpoints."""

import boto3
import fastapi
from fastapi import status

from app.core import config
from app.routers.audio import schemas

settings = config.get_settings()
logger = config.get_logger()


def post_tts(
    payload: schemas.PostTtsRequest,
) -> fastapi.Response:
    """Gets the audio bytes as mp3 for a given text.

    Args:
        payload: The request body.

    Returns:
        The bytes encoded as mp3.
    """
    client = boto3.client(
        "polly",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY.get_secret_value(),
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY.get_secret_value(),
    )
    response = client.synthesize_speech(
        Engine="neural",
        LanguageCode="en-US",
        OutputFormat="mp3",
        Text=payload.input,
        VoiceId=payload.voice,
    )

    return fastapi.Response(
        status_code=status.HTTP_200_OK,
        content=response["AudioStream"].read(),
        media_type=response["ContentType"],
    )

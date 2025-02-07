"""Views for the embeddings router."""

import fastapi
from fastapi import status

from app.core import config
from app.routers.audio import controller, schemas

router = fastapi.APIRouter(prefix="/audio/speech")

logger = config.get_logger()


@router.post(
    "",
    description="Runs text-to-speech on a string using Amazon Polly.",
    response_description="The speech bytes encoded as mp3.",
    responses={
        status.HTTP_200_OK: {"description": "OK."},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid Request."},
    },
)
def post_tts(
    payload: schemas.PostTtsRequest,
) -> fastapi.Response:
    """Gets the embedding of a string.

    Args:
        payload: The message body, c.f. the model for details.

    Returns:
        The embedding response in OpenAI's formatting.
    """
    logger.debug("Entering post-audio endpoint.")
    response = controller.post_tts(payload)
    logger.debug("Exiting post-audio endpoint.")
    return response

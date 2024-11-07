"""Views for the embeddings router."""

import fastapi
from fastapi import status

from app.core import config
from app.routers.embeddings import controller, schemas

router = fastapi.APIRouter(prefix="/embeddings")

logger = config.get_logger()


@router.post(
    "",
    description="Fetches the embedding of a string.",
    response_description="The requested embedding.",
    responses={
        status.HTTP_200_OK: {"description": "OK."},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid Request."},
    },
)
def post_embedding(
    payload: schemas.PostEmbeddingRequest,
) -> schemas.PostEmbeddingResponse:
    """Gets the embedding of a string.

    Args:
        payload: The message body, c.f. the model for details.

    Returns:
        The embedding response in OpenAI's formatting.
    """
    logger.debug("Entering post-embedding endpoint.")
    response = controller.post_embedding(payload)
    logger.debug("Exiting post-embeding endpoint.")
    return response

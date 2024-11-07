"""Views for the embeddings router."""

import fastapi

from app.core import config
from app.routers.images import controller, schemas

router = fastapi.APIRouter(prefix="/images")

logger = config.get_logger()


@router.post(
    "/generations",
    description="Fetches the images generated for a prompt.",
    response_description="The requested images.",
)
def post_images(
    payload: schemas.PostImageGenerationRequest,
) -> schemas.PostImageGenerationResponse:
    """Gets the embedding of a string.

    Args:
        payload: The message body, c.f. the model for details.

    Returns:
        The embedding response in OpenAI's formatting.
    """
    logger.debug("Entering post-images endpoint.")
    response = controller.post_image_generation(payload)
    logger.debug("Exiting post-images endpoint.")
    return response

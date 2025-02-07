"""Entrypoint for the server."""

import fastapi
from fastapi import status

from app.core import auth, config
from app.routers.audio import views as tts_views
from app.routers.embeddings import views as embeddings_views
from app.routers.images import views as images_views

logger = config.get_logger()

app = fastapi.FastAPI(
    title="Model Proxy",
    description=(
        "A proxy for AI models not well supported by LiteLLM. The goal is to "
        "convert these to LiteLLM if/when their support improves."
    ),
    dependencies=[fastapi.Depends(auth.check_api_key)],
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized."}},
)

version_router = fastapi.APIRouter(prefix="/v1")
version_router.include_router(embeddings_views.router)
version_router.include_router(images_views.router)
version_router.include_router(tts_views.router)

app.include_router(version_router)

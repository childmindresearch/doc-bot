"""Type definitions used across multiple files in the embeddings router."""

import time
from typing import Literal

import pydantic

IMAGE_GENERATION_MODELS = Literal[
    "aws/stability.sd3-large-v1:0", "aws/stability.sd3-5-large-v1:0"
]


class PostImageGenerationRequest(pydantic.BaseModel):
    """Post request for image generation."""

    model: IMAGE_GENERATION_MODELS
    prompt: str
    n: Literal[1]
    size: str
    response_format: Literal["b64_json"]

    @property
    def provider(self) -> str:
        """The model provider."""
        return self.model.split("/")[0]

    @property
    def model_name(self) -> str:
        """The model name."""
        return self.model.split("/")[1]


class PostImageGenerationImage(pydantic.BaseModel):
    """An image object for the image generation response."""

    b64_json: str
    revised_prompt: str


class PostImageGenerationResponse(pydantic.BaseModel):
    """The response for image generation."""

    data: list[PostImageGenerationImage]
    created: int = pydantic.Field(default_factory=lambda: int(time.time()))

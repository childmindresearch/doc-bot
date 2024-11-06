"""Type definitions used across multiple files in the embeddings router."""

from typing import Literal

import pydantic

PROVIDER = Literal["aws"]
MODEL_NAME = Literal["cohere.embed-english-v3"]
EMBEDDING_MODEL = Literal["aws/cohere.embed-english-v3"]


class PostEmbeddingRequest(pydantic.BaseModel):
    """The post embedding body."""

    model: EMBEDDING_MODEL
    input: str | list[str] | list[int] | list[list[int]] = pydantic.Field(
        max_length=None,
    )

    @property
    def provider(self) -> PROVIDER:
        """The model provider."""
        return self.model.split("/")[0]

    @property
    def model_name(self) -> MODEL_NAME:
        """The model name."""
        return self.model.split("/")[1]


class EmbeddingData(pydantic.BaseModel):
    """Object within the Embedding Response."""

    object: Literal["embedding"] = "embedding"
    index: int
    embedding: list[float]


class PostEmbeddingResponse(pydantic.BaseModel):
    """The post embedding response, following OpenAI's protocol."""

    object: Literal["list"] = "list"
    data: list[EmbeddingData]
    model: EMBEDDING_MODEL

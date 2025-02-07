"""Type definitions used across multiple files in the embeddings router."""

from typing import Literal

import pydantic

EMBEDDING_MODEL = Literal["aws/cohere.embed-english-v3", "azure/text-embedding-3-small"]


class PostEmbeddingRequest(pydantic.BaseModel):
    """The post embedding body."""

    model: EMBEDDING_MODEL
    input: str | list[str] = pydantic.Field(
        max_length=None,
    )

    @property
    def provider(self) -> str:
        """The model provider."""
        return self.model.split("/")[0]

    @property
    def model_name(self) -> str:
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

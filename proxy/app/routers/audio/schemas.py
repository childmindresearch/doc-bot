"""Type definitions used across multiple files in the embeddings router."""

import pydantic


class PostTtsRequest(pydantic.BaseModel):
    """The post embedding body."""

    voice: str = "Ruth"
    model: str
    input: str

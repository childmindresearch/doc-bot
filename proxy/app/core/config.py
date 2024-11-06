"""Configurations for the application."""

import functools
import logging

import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """App settings."""

    PROXY_KEY: pydantic.SecretStr = pydantic.Field(...)

    AWS_REGION: str = pydantic.Field(...)
    AWS_ACCESS_KEY: pydantic.SecretStr = pydantic.Field(...)
    AWS_SECRET_ACCESS_KEY: pydantic.SecretStr = pydantic.Field(...)

    LOGGER_VERBOSITY: int = logging.INFO


@functools.lru_cache
def get_settings() -> Settings:
    """Gets the app settings."""
    return Settings()


def get_logger() -> logging.Logger:
    """Gets the logger."""
    logger = logging.getLogger("ai-proxy")
    if logger.hasHandlers():
        return logger

    logger.setLevel(get_settings().LOGGER_VERBOSITY)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(funcName)s - %(message)s",  # noqa: E501
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

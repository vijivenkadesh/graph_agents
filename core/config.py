from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pydantic import SecretStr
from typing import Optional
from functools import lru_cache




class EnvSettings(BaseSettings):

    OPENAI_API_KEY: Optional[SecretStr] = Field(description="This is the API key for OpenAI",
                                                strict=True,
                                                default=None)

    WEATHER_API_KEY: Optional[SecretStr] = Field(description="This is the API key for the weather api service",
                                                strict=True,
                                                default=None)

    MODEL: str = ""

    LANGSMITH_TRACING: str = "true"
    LANGSMITH_ENDPOINT: str = ""
    LANGSMITH_API_KEY: str = ""
    LANGSMITH_PROJECT: str = ""
    PASS_CODE: str = ""

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8")



@lru_cache
def get_settings() -> EnvSettings:
    """Return the settings"""
    return EnvSettings()

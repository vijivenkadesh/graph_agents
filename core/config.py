from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from pydantic import SecretStr
from typing import Optional
import os



class EnvSettings(BaseSettings):
    OPENAI_API_KEY: Optional[SecretStr] = Field(description="This is the API key for OpenAI",
                                                strict=True,
                                                default=None)

    MODEL: str = ""

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8")

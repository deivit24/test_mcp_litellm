from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    base_url: Optional[str] = None
    base_url_docs: str = "http://localhost:8000/openapi.json"
    mcp_url: str = "http://localhost:8001/mcp"
    openai_key: Optional[str] = None
    litellm_url: Optional[str] = None
    mcp_port: int = 8001


settings = Settings()

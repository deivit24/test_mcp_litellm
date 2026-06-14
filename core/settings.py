from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    base_url: str
    base_url_docs: str = "http://localhost:8000/openapi.json"
    mcp_url: str = "http://localhost:8001/mcp"
    openai_key: str
    litellm_url: str


settings = Settings()

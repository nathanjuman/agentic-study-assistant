from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Inherits Pydantic BaseSettings class"""

    # Sets .env config.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Basic Runtime Config.
    app_name: str = "agentic-study-assistant-backend"
    environment: str = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Local folders for app data and logs
    data_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "data")
    logs_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "logs")

    # Storage paths for uploads, SQLite, local Qdrant data
    uploads_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "data" / "uploads")
    sqlite_path: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "data" / "study_assistant.db")
    qdrant_path: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[1] / "data" / "qdrant")

    # VectorDB Collection Name
    qdrant_collection: str = "study_chunks"

    # Model Settings
    openai_api_key: str | None = None
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4.1-mini"

    # Guardrails
    max_file_size_bytes: int = 10 * 1024 * 1024
    max_chunks_per_document: int = 200
    chunk_size: int = 800
    chunk_overlap: int = 120
    retrieval_limit: int = 5
    min_retrieval_score: float = 0.15


@lru_cache
def get_settings() -> Settings:
    """
    Ensures settings are built once and reused

    Creates singleton settings object and ensures app data
    and logs folder exists.
    """
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    settings.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    settings.qdrant_path.mkdir(parents=True, exist_ok=True)
    return settings

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB in bytes

    # AI API Keys (for cloud deployment)
    huggingface_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    cohere_api_key: Optional[str] = None

    # n8n Webhook URL for embedding generation
    n8n_webhook_url: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    upload_dir: str = "uploads"
    max_file_size: int = 10485760  # 10MB in bytes

    class Config:
        env_file = ".env"

settings = Settings()

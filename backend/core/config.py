"""Application configuration management"""
import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Vader AI Voice Assistant"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4

    # Security
    SECRET_KEY: str = "vader-secret-key-change-in-production"
    JWT_SECRET_KEY: str = "vader-jwt-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./vader_ai.db"

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Audio Settings
    SAMPLE_RATE: int = 16000
    AUDIO_FORMAT: str = "wav"
    MAX_AUDIO_LENGTH_SECONDS: int = 30

    # Vader Voice Settings
    VADER_VOICE_PITCH: int = -50
    VADER_VOICE_SPEED: float = 0.9
    VADER_BREATHING_ENABLED: bool = True

    # ESP32
    ESP32_WEBSOCKET_PATH: str = "/ws/esp32"
    ESP32_API_KEY: str = "change-this-esp32-api-key"

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_FOLDER: str = "./uploads"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()

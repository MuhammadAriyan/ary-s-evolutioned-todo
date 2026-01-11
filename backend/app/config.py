"""Application configuration using Pydantic Settings."""
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # JWT Configuration
    jwt_secret_key: str = "dev-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # Better Auth Configuration
    better_auth_url: str = "http://localhost:3004"

    # Database
    database_url: str = ""

    # CORS - accepts comma-separated string, JSON array, or single URL
    cors_origins: List[str] = ["http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if v is None:
            return ["http://localhost:3000"]
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            v = v.strip()
            # Try JSON array first
            if v.startswith("["):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Comma-separated
            if "," in v:
                return [origin.strip() for origin in v.split(",") if origin.strip()]
            # Single URL
            if v:
                return [v]
        return ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()

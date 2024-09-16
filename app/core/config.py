from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(env="PROJECT_NAME")
    FRONTEND_URL: str = Field(..., env="FRONTEND_URL")

    # firebase
    FIREBASE_CONFIG_PATH: str = Field(
        ..., env="FIREBASE_CONFIG_PATH", description="Firebase config path"
    )
    FIREBASE_STORAGE_BUCKET: str = Field(
        ..., env="FIREBASE_STORAGE_BUCKET", description="Firebase storage bucket url"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

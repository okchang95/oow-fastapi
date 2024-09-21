from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(env="PROJECT_NAME")
    FRONTEND_URL: str = Field(..., env="FRONTEND_URL")

    # Firebase
    FIREBASE_PROJECT_ID: str = Field(..., env="FIREBASE_PROJECT_ID")
    FIREBASE_PRIVATE_KEY_ID: str = Field(..., env="FIREBASE_PRIVATE_KEY_ID")
    FIREBASE_PRIVATE_KEY: str = Field(..., env="FIREBASE_PRIVATE_KEY")
    FIREBASE_CLIENT_EMAIL: str = Field(..., env="FIREBASE_CLIENT_EMAIL")
    FIREBASE_CLIENT_ID: str = Field(..., env="FIREBASE_CLIENT_ID")
    FIREBASE_AUTH_URI: str = Field(..., env="FIREBASE_AUTH_URI")
    FIREBASE_TOKEN_URI: str = Field(..., env="FIREBASE_TOKEN_URI")
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL: str = Field(
        ..., env="FIREBASE_AUTH_PROVIDER_X509_CERT_URL"
    )
    FIREBASE_CLIENT_X509_CERT_URL: str = Field(..., env="FIREBASE_CLIENT_X509_CERT_URL")
    FIREBASE_STORAGE_BUCKET: str = Field(..., env="FIREBASE_STORAGE_BUCKET")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

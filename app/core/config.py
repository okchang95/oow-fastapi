from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str = "OOW Challenge Project"

    # firebase
    FIREBASE_CONFIG_PATH: str = Field(
        "./firebase_credentials.json", description="Firebase config path"
    )
    FIREBASE_STORAGE_BUCKET: str = Field(
        "oow-challenge.appspot.com", description="Firebase storage bucket url"
    )

    # API_V1_STR: str = "/api/v1"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    # FIREBASE_STORAGE_BUCKET: str = Field(..., env="FIREBASE_STORAGE_BUCKET")

    # jwt
    # SECRET_KEY: str = Field(..., env="SECRET_KEY")
    # ALGORITHM: str = "HS256"

    # class Config:
    #     env_file = ".env"
    #     case_sensitive = True


settings = Settings()

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


settings = Settings()

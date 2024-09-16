import firebase_admin
from firebase_admin import credentials, storage, auth
from app.core.config import settings


def initialize_firebase():
    cred = credentials.Certificate(settings.FIREBASE_CONFIG_PATH)
    firebase_admin.initialize_app(
        cred, {"storageBucket": settings.FIREBASE_STORAGE_BUCKET}
    )
    bucket = storage.bucket()
    return bucket


bucket = initialize_firebase()

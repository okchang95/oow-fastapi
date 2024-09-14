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


# def verify_firebase_token(token: str):
#     try:
#         decoded_token = auth.verify_id_token(token)
#         return decoded_token
#     except Exception as e:
#         raise ValueError("Invalid Firebase token")

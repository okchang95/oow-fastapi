import firebase_admin
from firebase_admin import credentials, storage
from app.core.config import settings


def initialize_firebase():
    cred = credentials.Certificate(
        {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
            "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "client_id": settings.FIREBASE_CLIENT_ID,
            "auth_uri": settings.FIREBASE_AUTH_URI,
            "token_uri": settings.FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": settings.FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": settings.FIREBASE_CLIENT_X509_CERT_URL,
        }
    )
    firebase_admin.initialize_app(
        cred, {"storageBucket": settings.FIREBASE_STORAGE_BUCKET}
    )
    bucket = storage.bucket()
    return bucket


bucket = initialize_firebase()

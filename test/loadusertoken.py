import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin._auth_utils import UserNotFoundError

# Firebase Admin SDK 초기화
cred = credentials.Certificate("./firebase_credentials.json")
firebase_admin.initialize_app(cred)


email = input("Email:")

try:
    # 이미 존재하는 사용자의 정보를 가져옴
    existing_user = auth.get_user_by_email(email)
    custom_token = auth.create_custom_token(existing_user.uid)
    print(f"Custom Token for existing user ({email}): {custom_token.decode('utf-8')}")
except UserNotFoundError:
    # 사용자가 없을 때 처리
    print(f"No user found for the provided email: {email}")
except Exception as e:
    # 다른 모든 예외 처리
    print(f"An error occurred: {e}")

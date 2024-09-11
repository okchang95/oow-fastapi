import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin._auth_utils import EmailAlreadyExistsError

# Firebase Admin SDK 초기화
cred = credentials.Certificate("./firebase_credentials.json")
firebase_admin.initialize_app(cred)

email = input("Email:")
password = input("Password:")
# Firebase 사용자 생성 (테스트용)
try:
    user = auth.create_user(email=email, password=password)
except EmailAlreadyExistsError:
    # 이미 존재하는 사용자 처리
    user = auth.get_user_by_email(email)
    print(f"User {email} already exists.")

# Firebase 사용자에 대한 커스텀 토큰 생성
custom_token = auth.create_custom_token(user.uid)
print("Custom Token:", custom_token.decode("utf-8"))

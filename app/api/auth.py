import firebase_admin
from firebase_admin import credentials, auth
from fastapi import APIRouter, HTTPException
from app.core.config import settings


router = APIRouter()


@router.post("/auth")
async def authenticate_user(email: str, password: str):
    try:
        # 1. 사용자 정보로 Firebase에서 사용자 찾기
        try:
            user = auth.get_user_by_email(email)
        except firebase_admin._auth_utils.UserNotFoundError:
            # 사용자가 없을 경우 새로 생성
            user = auth.create_user(email=email, password=password)

        # 2. Firebase 커스텀 토큰 생성 (ID 토큰 대신 커스텀 토큰을 생성할 수 있음)
        custom_token = auth.create_custom_token(user.uid)

        # 클라이언트에게 커스텀 토큰 반환
        return {"custom_token": custom_token.decode("utf-8")}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

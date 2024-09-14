from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import upload_image
from app.core.config import settings

import os
from dotenv import load_dotenv

load_dotenv()


origins = [
    os.getenv("FRONTEND_URL"),
    "http://localhost:3000",
    "http://0.0.0.0:3000",
    "https://0.0.0.0:3000",
]

app = FastAPI(title=settings.PROJECT_NAME)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # React 앱의 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(upload_image.router)


@app.get("/")
async def root():
    return {"message": "hihi"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)  # host="0.0.0.0"


# from fastapi import  Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from app.api import dummyuser, auth

# app.include_router(dummyuser.router)
# app.include_router(auth.router)

# # JWT 설정
# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = settings.ALGORITHM

# # OAuth2PasswordBearer를 사용하여 JWT가 Authorization 헤더에서 추출되도록 설정
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # JWT 검증 함수
# def verify_jwt_token(token: str = Depends(oauth2_scheme)):
#     try:
#         # JWT 디코딩 및 서명 검증
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         return user_id  # 유효한 경우 사용자 ID 반환
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# # 보호된 엔드포인트에 JWT 검증 적용 예시
# @app.get("/protected-endpoint")
# async def protected_endpoint(user_id: str = Depends(verify_jwt_token)):
#     return {"message": f"Hello, user {user_id}! This is a protected endpoint."}

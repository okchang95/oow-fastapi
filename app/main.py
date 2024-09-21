from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.mypage import mypage
from app.api.calendar import calendar
from app.api.notice import notice


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
app.include_router(mypage.router, prefix="/api/mypage", tags=["MyPage"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["Calendar"])
app.include_router(notice.router, prefix="/api/notice", tags=["Notice"])


# @app.get("/")
# async def root():
#     return {"message": "hihi"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)

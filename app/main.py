from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.api.routes import auth, workouts, users, notifications, ocr
from app.api import process_img, dummyuser
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 앱의 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 라우터 등록
app.include_router(process_img.router)
app.include_router(dummyuser.router)


@app.get("/")
async def root():
    return {"message": "hihi"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)  # host="0.0.0.0"

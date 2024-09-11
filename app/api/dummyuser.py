from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from app.db.firebase import db

router = APIRouter()


@router.post("/create_dummy_user/")
async def create_dummy_user(user_id: int, user_name: str, user_password: str):
    try:
        # Firestore의 users 컬렉션에 유저 데이터를 삽입
        doc_ref = db.collection("users").document(str(user_id))
        doc_ref.set(
            {
                "user_id": user_id,
                "user_name": user_name,
                "user_password": user_password,
                "created_at": firestore.SERVER_TIMESTAMP,
            }
        )
        return {"message": f"유저 {user_name}(ID: {user_id})가 생성되었습니다."}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"유저 데이터 생성 중 오류 발생: {e}"
        )


@router.get("/get_user/{user_id}")
async def get_user(user_id: int):
    try:
        # Firestore에서 유저 데이터 조회
        doc_ref = db.collection("users").document(str(user_id))
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="유저 정보를 찾을 수 없습니다.")

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"유저 데이터 조회 중 오류 발생: {e}"
        )

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.db.firebase import bucket
import json

router = APIRouter()


class NotificationCreate(BaseModel):
    title: str
    content: str


class Notification(NotificationCreate):
    id: str
    created_at: datetime


def get_current_user(user_type: str):
    """
    "admin" or "user"
    """
    return user_type


# 공지사항 작성
@router.post("/", response_model=Notification)
async def create_notification(
    notification: NotificationCreate, user_type: str = Depends(get_current_user)
):
    """
    공지사항 작성 - json으로 저장
    key: title, content
    """
    # 일반유저면 접근 x
    if user_type != "admin":
        raise HTTPException(
            status_code=403, detail="관리자만 공지사항을 생성할 수 있습니다."
        )
    try:
        now = datetime.now()
        # TODO: id형식 고려(지금 보기 좀 그럼)
        notification_id = (
            f"{notification.title.replace(' ', '')}_{now.strftime('%Y%m%d%H%M%S')}"
        )
        blob = bucket.blob(f"notice/{notification_id}")

        notification_data = {
            "title": notification.title,
            "content": notification.content,
            "created_at": now.isoformat(),
        }

        # 저장
        blob.upload_from_string(
            json.dumps(notification_data), content_type="application/json"
        )

        return Notification(
            **notification.model_dump(), id=notification_id, created_at=now
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"공지사항 생성 중 오류 발생: {str(e)}"
        )


# 조회
@router.get("/", response_model=List[Notification])
async def get_notifications():
    """
    공지사항 조회: 모든 공지사항의 title, content, id, created_at을 리스트로 반환
    """
    try:
        blobs = bucket.list_blobs(prefix="notice/")
        notifications = []
        for blob in blobs:
            content = json.loads(blob.download_as_string())
            notification = Notification(
                id=blob.name.split("/")[-1],
                title=content["title"],
                content=content["content"],
                created_at=datetime.fromisoformat(content["created_at"]),
            )
            notifications.append(notification)
        return notifications
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"공지사항 조회 중 오류 발생: {str(e)}"
        )


# 수정
@router.put("/{notification_id}", response_model=Notification)
async def update_notification(
    notification_id: str,
    notification: NotificationCreate,
    user_name: str = Depends(get_current_user),
):
    """
    notification_id -> 조회에서 확인 가능
    """
    if user_name != "admin":
        raise HTTPException(
            status_code=403, detail="관리자만 공지사항을 수정할 수 있습니다."
        )
    try:
        blob = bucket.blob(f"notice/{notification_id}")
        if not blob.exists():
            raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")

        content = json.loads(blob.download_as_string())
        content["title"] = notification.title
        content["content"] = notification.content

        blob.upload_from_string(json.dumps(content), content_type="application/json")

        return Notification(
            id=notification_id,
            title=notification.title,
            content=notification.content,
            created_at=datetime.fromisoformat(content["created_at"]),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"공지사항 수정 중 오류 발생: {str(e)}"
        )


# 삭제
@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str, user_name: str = Depends(get_current_user)
):
    if user_name != "admin":
        raise HTTPException(
            status_code=403, detail="관리자만 공지사항을 삭제할 수 있습니다."
        )
    try:
        blob = bucket.blob(f"notice/{notification_id}")
        if not blob.exists():
            raise HTTPException(status_code=404, detail="공지사항을 찾을 수 없습니다.")

        # 해당 blob 삭제
        blob.delete()

        return {"message": "공지사항이 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"공지사항 삭제 중 오류 발생: {str(e)}"
        )

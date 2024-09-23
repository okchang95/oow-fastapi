from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import unicodedata

from app.db.firebase import bucket  # initialization
import time

router = APIRouter()


def normalize_string(s):
    return unicodedata.normalize("NFC", s).encode("utf-8")


@router.get("/user/{user_name}/total_uploads")
async def get_total_uploads(user_name: str):
    print(f"Request received at: {time.time()}")
    """
    "누적인증일수"와 "이미지 이름 리스트" 반환
    """
    try:
        blobs = bucket.list_blobs(prefix="images/")

        print(f"User name received: '{user_name}'")
        print(f"User name encoded: {user_name.encode()}")

        normalized_user_name = normalize_string(user_name)
        user_images = []

        for blob in blobs:
            filename = blob.name.split("/")[-1]
            normalized_filename = normalize_string(filename)

            print(f"Checking blob: '{filename}'")
            print(f"Filename encoded: {filename.encode()}")

            comparison_string = b"images/" + normalized_user_name + b"_"
            print(f"Comparison string: '{comparison_string}'")

            if normalize_string(blob.name).startswith(comparison_string):
                print(f"Adding image: {filename}")
                user_images.append(filename)
            else:
                print(f"Not matching: {filename}")

        print(user_images)

        total_uploads = len(user_images)

        return {
            "user_name": user_name,
            "total_uploads": total_uploads,
            "image_names": user_images,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"누적인증일수 및 이미지 목록 조회 중 오류 발생: {str(e)}",
        )


@router.get("/user/{user_name}/uploads_this_week")
async def get_uploads_this_week(user_name: str):
    """
    "이번 주 인증일 수" 반환
    """
    try:
        blobs = bucket.list_blobs(prefix="images/")
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        normalized_user_name = normalize_string(user_name)
        uploads_this_week = sum(
            1
            for blob in blobs
            if normalize_string(blob.name).startswith(
                b"images/" + normalized_user_name + b"_"
            )
            and start_of_week
            <= datetime.strptime(
                blob.name.split("_")[-1].split(".")[0], "%Y%m%d"
            ).date()
            <= end_of_week
        )
        return {"user_name": user_name, "uploads_this_week": uploads_this_week}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"이번주인증일수 조회 중 오류 발생: {str(e)}"
        )


@router.get("/user/{user_name}/fine_amount")
async def get_fine_amount(user_name: str):
    """
    "벌금 금액" 반환
    """
    try:
        blobs = bucket.list_blobs(prefix="images/")
        normalized_user_name = normalize_string(user_name)
        # 총 업로드 수
        total_uploads = sum(
            1
            for blob in blobs
            if normalize_string(blob.name).startswith(
                b"images/" + normalized_user_name + b"_"
            )
        )
        # 현재 날짜를 기준으로 이번 주의 시작일을 계산
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        # 이번 주의 종료일을 계산
        weeks_passed = (today - start_of_week).days // 7 + 1
        # 누적 업로드 수와 예상 업로드 수의 차이를 계산
        expected_uploads = weeks_passed * 3
        missed_days = max(0, expected_uploads - total_uploads)
        # 벌금 금액 계산
        fine_amount = missed_days * 5000
        return {"user_name": user_name, "fine_amount": fine_amount}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"벌금금액 조회 중 오류 발생: {str(e)}"
        )


@router.get("/user/{user_name}/images")
async def get_user_images(user_name: str):
    """
    "사용자가 업로드한 이미지 목록" 반환
    """
    try:
        blobs = bucket.list_blobs(prefix="images/")
        normalized_user_name = normalize_string(user_name)
        user_images = [
            blob.public_url
            for blob in blobs
            if normalize_string(blob.name).startswith(
                b"images/" + normalized_user_name + b"_"
            )
        ]
        return {"user_name": user_name, "user_images": user_images}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"사용자 이미지 조회 중 오류 발생: {str(e)}"
        )

from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime, timedelta

from .timecheck.ocr import perform_ocr
from app.db.firebase import bucket  # initialization


router = APIRouter()


# @router.get("/user/{user_name}")
# async def get_user_status(user_name: str):
#     """
#     "누적인증일수", "이번주인증일수", "벌금금액" 반환
#     """
#     try:
#         # bucket 불러오기
#         blobs = bucket.list_blobs(prefix="images/")

#         # debugs
#         print(f"Searching for blobs with prefix: {user_name}")

#         # 이번주 날짜
#         today = datetime.now().date()
#         start_of_week = today - timedelta(days=today.weekday())
#         end_of_week = start_of_week + timedelta(days=6)
#         print(f"이번 주 시작일: {start_of_week}, 종료일: {end_of_week}")

#         # 전체업로드, 이번주 업로드 계산
#         total_uploads = 0
#         uploads_this_week = 0
#         last_upload_date = None
#         user_images = []

#         for blob in blobs:
#             # 사용자 이름으로 시작하는 파일만 처리
#             if blob.name.startswith(f"images/{user_name}_"):
#                 print(f"Blob name: {blob.name}")
#                 date_str = blob.name.split("_")[-1].split(".")[0]

#                 try:
#                     upload_date = datetime.strptime(date_str, "%Y%m%d").date()
#                     print(f"Extracted date: {upload_date}")

#                     total_uploads += 1
#                     user_images.append(blob.public_url)

#                     if start_of_week <= upload_date <= end_of_week:
#                         uploads_this_week += 1

#                     if last_upload_date is None or upload_date > last_upload_date:
#                         last_upload_date = upload_date
#                 except ValueError as e:
#                     print(f"Error parsing date from blob name: {e}")

#         print(f"Total uploads: {total_uploads}")
#         print(f"Uploads this week: {uploads_this_week}")
#         # print(f"Last upload date: {last_upload_date}")

#         # 벌금계산
#         weeks_passed = (today - start_of_week).days // 7 + 1
#         expected_uploads = weeks_passed * 3

#         missed_days = max(0, expected_uploads - total_uploads)
#         fine_amount = missed_days * 5000  # 5000원 per missed day

#         return {
#             "user_name": user_name,  # 이름
#             "total_uploads": total_uploads,  # 누적 인증일 수
#             "uploads_this_week": uploads_this_week,  # 이번주 인증일 수
#             "fine_amount": fine_amount,  # 벌금 금액
#             "user_images": user_images,  # 사용자가 업로드한 이미지 목록 추가
#             # TODO: 이부분은 나중에 "님 운동 안한지 ~~일 째잖아요 운동하러가세요!" 할수있지않을까
#             # "last_upload_date": (
#             #     last_upload_date.strftime("%Y-%m-%d") if last_upload_date else None
#             # ),
#         }

#     except Exception as e:
#         print(f"Error in get_user_status: {str(e)}")
#         raise HTTPException(
#             status_code=500, detail=f"사용자 상태 조회 중 오류가 발생했습니다: {str(e)}"
#         )


@router.get("/user/{user_name}/total_uploads")
async def get_total_uploads(user_name: str):
    try:
        blobs = bucket.list_blobs(prefix="images/")
        total_uploads = sum(
            1 for blob in blobs if blob.name.startswith(f"images/{user_name}_")
        )
        return {"user_name": user_name, "total_uploads": total_uploads}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"누적인증일수 조회 중 오류 발생: {str(e)}"
        )


@router.get("/user/{user_name}/uploads_this_week")
async def get_uploads_this_week(user_name: str):
    try:
        blobs = bucket.list_blobs(prefix="images/")
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        uploads_this_week = sum(
            1
            for blob in blobs
            if blob.name.startswith(f"images/{user_name}_")
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
    try:
        blobs = bucket.list_blobs(prefix="images/")
        total_uploads = sum(
            1 for blob in blobs if blob.name.startswith(f"images/{user_name}_")
        )
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        weeks_passed = (today - start_of_week).days // 7 + 1
        expected_uploads = weeks_passed * 3
        missed_days = max(0, expected_uploads - total_uploads)
        fine_amount = missed_days * 5000
        return {"user_name": user_name, "fine_amount": fine_amount}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"벌금금액 조회 중 오류 발생: {str(e)}"
        )


@router.get("/user/{user_name}/images")
async def get_user_images(user_name: str):
    try:
        blobs = bucket.list_blobs(prefix="images/")
        user_images = [
            blob.public_url
            for blob in blobs
            if blob.name.startswith(f"images/{user_name}_")
        ]
        return {"user_name": user_name, "user_images": user_images}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"사용자 이미지 조회 중 오류 발생: {str(e)}"
        )

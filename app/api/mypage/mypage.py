from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime, timedelta

from .timecheck.ocr import perform_ocr
from app.db.firebase import bucket  # initialization


router = APIRouter()


@router.post("/upload_image")
async def upload_image(imagefile: UploadFile = File(...)):
    """
    이미지 파일받아서 파일 내 날짜정보만 확인 후 버킷에 저장
    """
    try:
        # 파일 확장자 확인
        extension = imagefile.filename.split(".")[-1] in ("jpg", "jpeg", "png")
        if not extension:
            raise HTTPException(
                status_code=400, detail="이미지 파일만 업로드 가능합니다."
            )
        # 파일 내용을 bytes로 읽기
        file_bytes = await imagefile.read()

        # byte를 받아서 result를 dict로 반환  {"verified": Bool, "date": date or None}
        result_ocr = perform_ocr(file_bytes)

        if result_ocr["verified"]:
            # 이미지 파일을 Firebase Storage에 업로드
            blob = bucket.blob(f"images/{imagefile.filename}")
            blob.upload_from_string(file_bytes, content_type=imagefile.content_type)

            # 업로드 완료 후 파일 URL 반환
            blob.make_public()
            file_url = blob.public_url

            return {
                "message": "파일 업로드 완료",
                "file_url": file_url,
                "ocr_result": result_ocr,
            }
        else:
            return {
                "message": "OCR 인증 실패. 파일은 업로드되지 않았습니다.",
                "ocr_result": result_ocr,
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"파일 업로드 중 오류가 발생했습니다: {e}"
        )


@router.get("/user/{user_name}")
async def get_user_status(user_name: str):
    """
    "누적인증일수", "이번주인증일수", "벌금금액" 반환
    """
    try:
        # bucket 불러오기
        blobs = bucket.list_blobs(prefix="images/")

        # debugs
        print(f"Searching for blobs with prefix: {user_name}_")

        # 이번주 날짜
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        print(f"이번 주 시작일: {start_of_week}, 종료일: {end_of_week}")

        # 전체업로드, 이번주 업로드 계산
        total_uploads = 0
        uploads_this_week = 0
        last_upload_date = None

        for blob in blobs:
            print(f"Blob name: {blob.name}")
            date_str = blob.name.split("_")[-1].split(".")[0]

            try:
                upload_date = datetime.strptime(date_str, "%Y%m%d").date()
                print(f"Extracted date: {upload_date}")

                total_uploads += 1

                if start_of_week <= upload_date <= end_of_week:
                    uploads_this_week += 1

                if last_upload_date is None or upload_date > last_upload_date:
                    last_upload_date = upload_date
            except ValueError as e:
                print(f"Error parsing date from blob name: {e}")

        print(f"Total uploads: {total_uploads}")
        print(f"Uploads this week: {uploads_this_week}")
        # print(f"Last upload date: {last_upload_date}")

        # 벌금계산
        weeks_passed = (today - start_of_week).days // 7 + 1
        expected_uploads = weeks_passed * 3

        missed_days = max(0, expected_uploads - total_uploads)
        fine_amount = missed_days * 5000  # 5000원 per missed day

        return {
            "user_name": user_name,  # 이름
            "total_uploads": total_uploads,  # 누적 인증일 수
            "uploads_this_week": uploads_this_week,  # 이번주 인증일 수
            "fine_amount": fine_amount,  # 벌금 금액
            # TODO: 이부분은 나중에 "님 운동 안한지 ~~일 째잖아요 운동하러가세요!" 할수있지않을까
            # "last_upload_date": (
            #     last_upload_date.strftime("%Y-%m-%d") if last_upload_date else None
            # ),
        }

    except Exception as e:
        print(f"Error in get_user_status: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"사용자 상태 조회 중 오류가 발생했습니다: {str(e)}"
        )

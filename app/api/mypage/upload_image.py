from fastapi import APIRouter, UploadFile, File, HTTPException

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

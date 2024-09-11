from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from firebase_admin import storage
from datetime import datetime

from .timecheck.ocr import perform_ocr  # 위에서 제공한 OCR 함수를 import 합니다.


class UserInput(BaseModel):
    user_id: int  # pk
    user_name: str  # 회원 이름


router = APIRouter()


@router.post("/upload_image")
async def upload_image(user_input: UserInput, imagefile: UploadFile = File(...)):
    try:
        user_id = user_input.user_id
        user_name = user_input.user_name
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
            # filename 지정
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"{user_id}_{user_name}_{current_time}.{imagefile.filename.split('.')[-1]}"

            # 이미지 파일을 Firebase Storage에 업로드
            blob = storage.bucket().blob(f"users/{user_id}/{file_name}")
            blob.upload_from_file(imagefile.file, content_type=imagefile.content_type)

            # 업로드 완료 후 파일 URL 반환
            blob.make_public()
            file_url = blob.public_url

            return {
                "message": "파일 업로드 완료",
                "file_url": file_url,
                "ocr_result": result_ocr,
            }
        else:
            # OCR 결과가 verified=False일 경우 파일 다시 처음으로 되돌리기
            await imagefile.seek(0)
            return {
                "message": "OCR 인증 실패. 파일은 업로드되지 않았습니다.",
                "ocr_result": result_ocr,
            }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"파일 업로드 중 오류가 발생했습니다: {e}"
        )


# # 이미지 다운로드 함수
# def download_image(image_name: str) -> bytes:
#     bucket = storage.bucket()
#     blob = bucket.blob(image_name)

#     if not blob.exists():
#         raise HTTPException(status_code=404, detail="Image not found")

#     return blob.download_as_bytes()


# # 이미지 다운로드 라우터
# @router.get("/download-image/{image_name}")
# async def download_image_route(image_name: str):
#     try:
#         image_bytes = download_image(image_name)
#         return Response(content=image_bytes, media_type="image/jpeg")
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # 모든 이미지 목록 가져오기
# @router.get("/list-images/")
# async def list_images():
#     bucket = storage.bucket()
#     blobs = bucket.list_blobs()

#     image_list = [{"name": blob.name, "url": blob.public_url} for blob in blobs]
#     return {"images": image_list}


# # 이미지 삭제 라우터
# @router.delete("/delete-image/{image_name}")
# async def delete_image(image_name: str):
#     try:
#         bucket = storage.bucket()
#         blob = bucket.blob(image_name)

#         if not blob.exists():
#             raise HTTPException(status_code=404, detail="Image not found")

#         blob.delete()
#         return {"message": "Image deleted successfully"}
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

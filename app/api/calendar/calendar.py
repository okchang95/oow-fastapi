# storage 읽어서 날짜별로 json 반환
from fastapi import APIRouter, HTTPException
from datetime import datetime
import calendar

from app.db.firebase import bucket


router = APIRouter()


@router.get("/")
async def get_calendar():
    """
    storage에서 이미지파일 날짜별로 분류해서 json형식으로 반환
    filename: name_yyyymmdd.jpg
    """
    try:
        blobs = bucket.list_blobs(prefix="images/")

        # 현재 년도와 월 가져오기
        today = datetime.now()
        year, month = today.year, today.month

        # 해당 월의 첫 날과 마지막 날 구하기
        _, last_day = calendar.monthrange(year, month)

        # 캘린더 초기화(모든 날짜 생성)
        calendar_data = {
            f"{year}-{month:02d}-{day:02d}": [] for day in range(1, last_day + 1)
        }

        for blob in blobs:

            print(blob.name)
            date_str = blob.name.split(".")[0].split("_")[-1]
            name_str = blob.name.split("_")[0]
            print(date_str)

            try:
                date = datetime.strptime(date_str, "%Y%m%d").date()
                # 출력하려는 현재 날짜 확인
                if date.year == year and date.month == month:
                    key = date.strftime("%Y-%m-%d")
                    if key in calendar_data:
                        calendar_data[key].append(name_str)
            except ValueError:
                continue

        return calendar_data

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"캘린더 데이터 조회 중 오류가 발생했습니다: {str(e)}",
        )

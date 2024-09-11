from fastapi import HTTPException
from io import BytesIO
from PIL import Image
import numpy as np
import easyocr
import re


def extract_date(text):
    # 다양한 날짜 형식을 처리하기 위한 정규 표현식 패턴들
    patterns = [
        r"\d{4}[-./]\d{1,2}[-./]\d{1,2}",  # YYYY-MM-DD, YYYY/MM/DD, YYYY.MM.DD
        r"\d{1,2}[-./]\d{1,2}[-./]\d{4}",  # DD-MM-YYYY, MM/DD/YYYY, DD.MM.YYYY
        r"\d{4}년\s?\d{1,2}월\s?\d{1,2}일",  # YYYY년 MM월 DD일
        r"\d{1,2}월\s?\d{1,2}일,?\s?\d{4}년?",  # MM월 DD일, YYYY년
        r"\d{4}[-.]\d{1,2}[-.]\d{1,2}\s\d{1,2}:\d{2}:\d{2}",  # YYYY-MM-DD HH:MM:SS
        r"\d{1,2}[-.]\d{1,2}[-.]\d{4}\s\d{1,2}:\d{2}:\d{2}",  # DD-MM-YYYY HH:MM:SS
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return None


def perform_ocr(file_content: bytes):
    try:
        # 바이트 데이터 => 이미지 => numpyarray
        image = Image.open(BytesIO(file_content))
        image_np = np.array(image)

        # EasyOCR 리더 초기화 (한국어와 영어 지원)
        print("Initialize OCR...")
        reader = easyocr.Reader(["ko", "en"])

        # EasyOCR로 텍스트 추출
        print("OCR Start...")
        results = reader.readtext(image_np)
        print("OCR End...")

        # 추출된 모든 텍스트를 하나의 문자열로 결합
        full_text = " ".join([result[1] for result in results])

        # 정규식을 사용하여 날짜 추출
        date = extract_date(full_text)
        print(
            f"""Full Text: 
================================================================
    {full_text}
================================================================
Date Found: {date}"""
        )

        if date:
            return {"verified": True, "date": date}  # , "full_text": full_text}
        else:
            return {"verified": False, "date": None}  # , "full_text": full_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

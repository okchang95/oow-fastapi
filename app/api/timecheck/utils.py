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

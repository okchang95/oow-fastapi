# Python 3.11 이미지를 기반으로 합니다
FROM python:3.11-slim

# 작업 디렉토리를 설정합니다
WORKDIR /app

# 필요한 패키지를 설치합니다
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 프로젝트 의존성을 복사하고 설치합니다
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 파일을 복사합니다
COPY . .

# 포트 8080 노출합니다
EXPOSE 8080

# 애플리케이션을 실행합니다
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
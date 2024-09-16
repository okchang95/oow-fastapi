# oow fastapi server
```
python==3.11.0
numpy==1.26.4
```

## 환경설정

### 필수 파일
프로젝트 루트 디렉토리에 다음 파일들이 필요합니다:
- `.env`
- `serviceAccountKey.json` (Firebase 서비스 계정 키)
### `.env` 파일 설정
```
FRONTEND_URL=http://{ip or localhost}:3000
PROJECT_NAME=your-project-name
FIREBASE_CONFIG_PATH=./your-firebase-key-filename.json
FIREBASE_STORAGE_BUCKET=your-bucket-url
```

## 설치 및 실행

### 도커 이미지 빌드
```bash
docker build -t [your-image-name] .
```
```bash
# builded image 
REPOSITORY               TAG       IMAGE ID       CREATED         SIZE
your-image-name          latest    d61c21d4dd75   2 minutes ago   6.2GB
```

### 도커 컨테이너 실행
```bash
# Linux/macOS
docker run -p 8000:8000 \
  -n [your-container-name]
  --env-file .env \
  -v $(pwd)/[your-firebase-key-filename.json]:/app/[your-firebase-key-filename.json]:ro \
  [your-image-name]

# Windows
docker run -p 8000:8000 \
  -n [your-container-name]
  --env-file .env \
  -v ${PWD}/[your-firebase-key-filename.json]:/app/[your-firebase-key-filename.json]:ro \
  [your-image-name]
```
<!--
docker run -p 8000:8000 \
  --name oow-test-container \
  --env-file .env \
  -v $(pwd)/firebase_credentials.json:/app/firebase_credentials.json:ro \
  oow-test
-->

## 프로젝트 구조
```bash
.
├── app/
│   ├── api/ # routers
│   │   ├── calendar/ # 전체 인증 출력
│   │   │   └── calendar.py # Read
│   │   ├── mypage/
│   │   │   ├── mypage.py # ocr인증 후 upload, 인증 수, 벌금 출력
│   │   │   └── timecheck/
│   │   │       └── ocr.py
│   │   └── notice/
│   │       └── notice.py # 공지사항 CRUD, admin만 입력, 수정, 삭제 가능
│   ├── core/
│   │   └── config.py # 환경변수 pydantic
│   ├── db/
│   │   └── firebase.py # firebase initializers
│   └── main.py
│
├── serviceAccountKey.json # firebase credentials key
├── .env # environment: frontend url
├── .gitignore
├── .docerignore
├── Dockerfile
├── requirements.txt
└── README.md
```
## 주요 기능

### MyPage
- 오운완 인증 이미지 업로드
- 사용자별 인증 및 벌금 정보 조회

### Calendar
- 날짜별 인증 현황 조회

### Notice
- 공지사항 CRUD (관리자 전용)

## API 문서
서버 실행 후 `http://localhost:8000/docs`에서 Swagger UI를 통해 API 문서를 확인할 수 있습니다.

## 개발 현황
- [x] 불필요한 로직 제거
- [x] 캘린더 조회 기능 추가
- [x] 공지사항 CRUD 기능 추가
- [x] Storage에서 인증 이미지와 공지사항 경로 분리

<img width="302" alt="image" src="https://github.com/user-attachments/assets/256ff235-604c-4203-8aea-31cf1f45202a">


## swagger

<img width="600" alt="image" src="images/swagger.png">

## MyPage
- 이미지 첨부하면 오운완 인증 후 업로드
- 누적인증, 이번주 인증, 벌금 

> ### [POST] /mypage/upload_image 
> ---
> #### Request
> - 이미지 첨부("오운완 인증하기" 클릭)
> - filename: `"이름_YYYYMMDD.jpg" (jpeg, png)`
> 
> #### Reponse
> ```bash
> {
>   "message": "파일 업로드 완료",
>   "file_url": "https://storage.googleapis.com/[FIREBASE_PROJCT_NAME].appspot.com/images/[ENCODED_USERNAME_YYYYMMDD.jpg]",
>   "ocr_result": {
>     "verified": true,
>     "date": "yyyy년 mm월 dd일" # ocr이 찾은 날짜
>   }
> }
> ```

<br>

> ### [GET] /mypage/user/{user_name}
> ---
> #### Parameters: `user_name: 회원이름`
> ```bash
> {
>   "user_name": "이름임",
>   "total_uploads": 2,    # 누적 인증 수
>   "uploads_this_week": 0,    # 이번 주 인증 수
>   "fine_amount": 5000    # 누적 벌금
> }
> ```

## Calendar
- 저장된 이미지 반복문으로 처리후 날짜별로 이름이 담긴 json으로 반환
> ### [GET] /calendar/
> ---
> ```bash
> {
>  ...,
>   "2024-09-11": [],
>   "2024-09-12": [],
>   "2024-09-13": [
>     "이름1",
>     "이름2",
>     ...
>   ],
>   "2024-09-14": [],
>   "2024-09-15": [],
>   ...
> }
> ```

## Notice
- 공지사항 CRUD
- 조회는 전체 가능
- 입력, 수정, 삭제는 `user_type: "admin"` 만 가능 (일반유저는 `"user"`)
- 공지사항 등록, 수정 시에 `title`, `content` 입력 
- 등록된 공지사항은 storage에 `notification_id` 로 저장
- 수정, 삭제 시에 `notification_id` 로 접근

> ### [POST] /notice/
> ---
> Create Notification
>
> #### Parameters 
> - `user_type: "admin" or "user"`
> 
> #### Request
> ```bash
> {
>   "title": "string",
>   "content": "string"
> }
> ```
> 
> #### Response
> ```bash
> {
>   "title": "string",
>   "content": "string",
>   "id": "string",    # title_yyyymmddhhmmss
>   "created_at": "2024-09-16T13:31:31.733Z"    #  ISO 8601 형식의 UTC 시간
> }
> ```

<br>

> ### [GET] /notice/
> ---
> Get Notification
> ```bash
> [
>   ... ,
>   {
>     "title": "test1",
>     "content": "test1",
>     "id": "test1_20240916200627",
>     "created_at": "2024-09-16T20:06:27.279163"
>   },
>   {
>     "title": "test2",
>     "content": "test2",
>     "id": "test2_20240916200256",
>     "created_at": "2024-09-16T20:02:56.187862"
>   },
>   ...
> ]
> ```

<br>

> ### [PUT] /notice/{notification_id}
> ---
> Update Notification
> 
> #### Parameters: 
> - `user_type: "admin" or "user"`
> - `notification_id: "title_date"`
> 
> #### Request
> ```bash
> {
>   "title": "string",
>   "content": "string"
> }
> ```
> 
> #### Response
> ```bash
> {
>   "title": "string",
>   "content": "string",
>   "id": "string",    # title_yyyymmddhhmmss
>   "created_at": "2024-09-16T13:31:31.733Z"    #  ISO 8601 형식의 UTC 시간
> }
> ```

<br>

> ### [DELETE] /notice/{notification_id}
> ---
> Delete Notification
> #### Parameters: 
> - `user_type: "admin" or "user"`
> 
> #### Response
>  string: 삭제완료

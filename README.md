python==3.11.0
numpy==1.26.4

### tree(09/12)
```bash
.
├── app
│   ├── api # routers
│   │   ├── auth.py # firebase id token 생성 관련 라우터(test)
│   │   ├── upload_image.py # 메인기능: 오운완 인증, 이미지 업로드, 인증일 로직
│   │   └── timecheck # ocr 관련 모듈(process_img.py에서 사용, 정리 필요)
│   │       └── ocr.py # inference module
│   ├── core # 공통으로 사용 
│   │   └── config.py # 환경변수 pydantic
│   ├── db
│   │   └── firebase.py # firebase initializers, firebase 토큰 인증
│   └── main.py # entry point
│
├── test
│   ├── dummyusertoken.py # 더미 회원 생성, firebase id token 발급
│   └── loadusertoken.py # firestore에 생성된 회원 조회, firebase token 조회
├── images 
│   └── test.jpg # test image
│
├── firebase_credentials.json # firebase credentials key
├── requirements.txt
├── .env # environment
├── .gitignore
└── README.md
```

## post("/upload_image")

### Request

![alt text](image.png)

### Response

```bash
{
  "message": "파일 업로드 완료",
  "file_url": "https://storage.googleapis.com/oow-challenge.appspot.com/[ENCODED_NAME]_[DATE].jpg",
  "ocr_result": {
    "verified": true,
    "date": "2024년 7월 29일"
  }
}
```


## get("/mypage/{user_name}")

```text
Searching for blobs with prefix: 옥창우
Blob name: 김김김_20240911.jpg
Extracted date: 2024-09-11
Blob name: 김김김_20240912.jpg
Extracted date: 2024-09-12
Blob name: 김김김_20240913.jpg
Extracted date: 2024-09-13
Total uploads: 3
Uploads this week: 3
Last upload date: 2024-09-13

```

### Response

```bash
{
  "user_name": "옥창우",
  "total_uploads": 3,
  "uploads_this_week": 3,
  "fine_amount": 0,
  "last_upload_date": "2024-09-13"
}
```
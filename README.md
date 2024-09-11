python==3.11.0
numpy==1.26.4

### tree(09/12)
```bash
.
├── app
│   ├── api # routers
│   │   ├── auth.py # firebase id token 생성 관련 라우터(test)
│   │   ├── dummyuser.py # 더미유저정보 생성, 조회 라우터
│   │   ├── process_img.py # 메인기능: 오운완 인증, 이미지 업로드, CRUD 라우터
│   │   └── timecheck # ocr 관련 모듈(process_img.py에서 사용, 정리 필요)
│   │       └── ocr.py # inference module
│   ├── core # 공통으로 사용 
│   │   ├── config.py # 환경변수 pydantic
│   │   └── jwt.py # jwt 토큰 생성(test)
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
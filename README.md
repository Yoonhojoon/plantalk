stAPI 서버

이 프로젝트는 FastAPI를 사용한 기본 웹 서버입니다.

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 실행 방법

서버 실행:
```bash
uvicorn main:app --reload
```

서버가 실행되면 다음 URL에서 접근할 수 있습니다:
- API 서버: http://localhost:8000
- API 문서: http://localhost:8000/docs
- 대체 API 문서: http://localhost:8000/redoc

## API 엔드포인트

- GET `/`: 기본 환영 메시지
- GET `/health`: 서버 상태 확인 
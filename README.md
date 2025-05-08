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




1. 인증 (Authentication)
| 엔드포인트 | 메서드 | 설명 | 요청 본문 | 응답 |
|------------|--------|------|------------|------|
| /api/auth/login | POST | 로그인 | { "email": string, "password": string } | { "access_token": string, "token_type": "bearer", "user_id": string } |
| /api/auth/signup | POST | 회원가입 | { "email": string, "password": string } | { "message": string } |

2. 사용자 (Users)
| 엔드포인트 | 메서드 | 설명 | 요청 본문 | 응답 |
|------------|--------|------|------------|------|
| /api/me | GET | 현재 사용자 정보 조회 | - | { "id": string, "nickname": string, "created_at": datetime } |
| /api/me | PATCH | 닉네임 수정 | { "nickname": string } | { "id": string, "nickname": string, "created_at": datetime } |

3. 식물 종 (Plant Species)
| 엔드포인트 | 메서드 | 설명 | 요청 본문 | 응답 |
|------------|--------|------|------------|------|
| /api/species | GET | 식물 종 목록 조회 | - | [{ "id": string, "name": string, "scientific_name": string, "description": string, "image_url": string, "temp_range_min": number, "temp_range_max": number, "humidity_range_min": number, "humidity_range_max": number, "light_range_min": number, "light_range_max": number, "created_at": datetime }] |

4. 식물 (Plants)
| 엔드포인트 | 메서드 | 설명 | 요청 본문 | 응답 |
|------------|--------|------|------------|------|
| /api/plants | GET | 사용자의 식물 목록 조회 | - | [{ "id": string, "user_id": string, "species_id": string, "name": string, "location": string, "watering_cycle_days": number, "last_watered_at": datetime, "next_watering_date": datetime, "temp_range_min": number, "temp_range_max": number, "humidity_range_min": number, "humidity_range_max": number, "light_range_min": number, "light_range_max": number, "created_at": datetime }] |
| /api/plants | POST | 새 식물 등록 | { "species_id": string(선택), "name": string(선택), "location": string, "watering_cycle_days": number, "last_watered_at": string(ISO 형식), "temp_range_min": number(선택), "temp_range_max": number(선택), "humidity_range_min": number(선택), "humidity_range_max": number(선택), "light_range_min": number(선택), "light_range_max": number(선택) } | 식물 객체 |
| /api/plants/{plant_id} | GET | 특정 식물 정보 조회 | - | 식물 객체 |
| /api/plants/{plant_id} | PATCH | 식물 정보 수정 | { "name": string(선택), "location": string(선택), "watering_cycle_days": number(선택), "temp_range_min": number(선택), "temp_range_max": number(선택), "humidity_range_min": number(선택), "humidity_range_max": number(선택), "light_range_min": number(선택), "light_range_max": number(선택) } | 식물 객체 |
| /api/plants/{plant_id} | DELETE | 식물 삭제 | - | { "message": string } |
| /api/plants/{plant_id}/water | POST | 식물 물주기 | - | 식물 객체 |

5. 알림 (Notifications)
| 엔드포인트 | 메서드 | 설명 | 요청 본문 | 응답 |
|------------|--------|------|------------|------|
| /api/notifications | GET | 사용자의 알림 목록 조회 | - | [{ "id": string, "user_id": string, "plant_id": string, "title": string, "type": string, "status": string, "created_at": datetime, "read_at": datetime }] |
| /api/notifications/{notification_id} | PATCH | 알림 읽음 처리 | - | 알림 객체 |

주의사항
모든 API 요청에는 인증이 필요합니다. Authorization 헤더에 Bearer {access_token} 형식으로 토큰을 포함해야 합니다.
location 필드는 다음 값들만 허용됩니다: "거실", "침실", "주방", "화장실", "베란다", "정원", "실내", "실외"
species_id를 제공하지 않는 경우, 모든 기준값(temp_range_min/max, humidity_range_min/max, light_range_min/max)을 직접 입력해야 합니다.
날짜/시간 필드는 ISO 8601 형식의 문자열을 사용합니다 (예: "2024-03-14T10:00:00").
이 API 명세서를 기반으로 프론트엔드 개발을 진행하시면 됩니다. 추가적인 질문이 있으시다면 말씀해 주세요!
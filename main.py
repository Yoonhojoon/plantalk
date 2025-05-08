from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user

app = FastAPI(
    title="Plant Care API",
    description="식물 관리를 위한 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 도메인 지정 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(user.router, prefix="/api", tags=["users"])

@app.get("/")
async def root():
    return {"message": "식물 관리 API에 오신 것을 환영합니다!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"} 
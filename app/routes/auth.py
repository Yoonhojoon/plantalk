from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from ..database import supabase

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        # Supabase 로그인
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        if not response.user:
            raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
        
        # users 테이블에 사용자 정보가 있는지 확인
        user_check = supabase.table("users").select("*").eq("id", response.user.id).execute()
        
        # 사용자 정보가 없으면 생성
        if not user_check.data:
            new_user = {
                "id": response.user.id,
                "nickname": None
            }
            supabase.table("users").insert(new_user).execute()
        
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user_id": response.user.id
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/signup")
async def signup(request: LoginRequest):
    try:
        # Supabase 회원가입
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        
        if not response.user:
            raise HTTPException(status_code=400, detail="회원가입에 실패했습니다.")
        
        # users 테이블에 사용자 정보 생성
        new_user = {
            "id": response.user.id,
            "nickname": None
        }
        supabase.table("users").insert(new_user).execute()
        
        return {"message": "회원가입이 완료되었습니다. 이메일을 확인해주세요."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
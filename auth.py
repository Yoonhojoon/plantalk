from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import supabase

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        # Bearer 토큰에서 실제 토큰 추출
        token = credentials.credentials
        
        # Supabase에서 사용자 정보 가져오기
        try:
            user = supabase.auth.get_user(token)
            if not user or not user.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="인증되지 않은 사용자입니다.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return user.user
        except Exception as auth_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 인증 정보입니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 처리 중 오류가 발생했습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
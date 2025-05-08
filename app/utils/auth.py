from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..database import get_user_by_id

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    현재 인증된 사용자 정보를 가져옵니다.
    Supabase의 토큰을 사용하여 사용자를 식별합니다.
    """
    try:
        # 토큰에서 사용자 ID 추출 (Supabase 토큰 사용)
        token = credentials.credentials
        # TODO: Supabase 토큰 검증 및 사용자 ID 추출 로직 구현
        
        user = await get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        return user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 정보입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
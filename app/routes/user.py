from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from ..schemas.user import UserResponse, UserUpdate
from ..database import get_user_by_id, update_user
from ..utils.auth import get_current_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    로그인한 사용자 정보 조회
    """
    return current_user

@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    닉네임 수정
    """
    if not user_update.nickname:
        raise HTTPException(status_code=400, detail="수정할 내용이 없습니다.")
    
    updated_user = await update_user(
        current_user["id"],
        {"nickname": user_update.nickname}
    )
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    return updated_user[0] 
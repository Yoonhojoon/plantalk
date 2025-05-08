from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from database import supabase
from models import User
from auth import get_current_user

router = APIRouter(
    prefix="/me",
    tags=["users"]
)

class UpdateNicknameRequest(BaseModel):
    nickname: str

@router.get("", response_model=User)
async def get_current_user_info(user = Depends(get_current_user)):
    try:
        # users 테이블에서 추가 정보 가져오기
        response = supabase.table("users").select("*").eq("id", user.id).single().execute()
        
        if not response.data:
            # 사용자가 users 테이블에 없는 경우 새로 생성
            new_user = {
                "id": user.id,
                "nickname": None
            }
            response = supabase.table("users").insert(new_user).execute()
            return response.data[0]
            
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("", response_model=User)
async def update_nickname(request: UpdateNicknameRequest, user = Depends(get_current_user)):
    try:
        response = supabase.table("users").update({"nickname": request.nickname}).eq("id", user.id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
            
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models import Notification
from ..database import supabase

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

async def get_current_user_id():
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="인증되지 않은 사용자입니다.")
    return user.user.id

@router.get("", response_model=List[Notification])
async def get_notifications(user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("notifications").select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{notification_id}")
async def update_notification(notification_id: str, user_id: str = Depends(get_current_user_id)):
    try:
        # 알림 존재 여부 확인
        notification = supabase.table("notifications").select("*").eq("id", notification_id).eq("user_id", user_id).single().execute()
        if not notification.data:
            raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다.")

        # 알림을 읽음 상태로 업데이트
        from datetime import datetime
        update_data = {
            "read_at": datetime.now()
        }
        
        response = supabase.table("notifications").update(update_data).eq("id", notification_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
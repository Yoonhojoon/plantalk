from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from models import Plant
from database import supabase

router = APIRouter(
    prefix="/plants",
    tags=["plants"]
)

class CreatePlantRequest(BaseModel):
    species_id: str
    name: Optional[str] = None
    location: str
    watering_cycle_days: int

class UpdatePlantRequest(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    watering_cycle_days: Optional[int] = None
    temp_range_min: Optional[float] = None
    temp_range_max: Optional[float] = None
    humidity_range_min: Optional[float] = None
    humidity_range_max: Optional[float] = None
    light_range_min: Optional[float] = None
    light_range_max: Optional[float] = None

async def get_current_user_id():
    user = supabase.auth.get_user()
    if not user:
        raise HTTPException(status_code=401, detail="인증되지 않은 사용자입니다.")
    return user.user.id

@router.get("", response_model=List[Plant])
async def get_plants(user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("plants").select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=Plant)
async def create_plant(request: CreatePlantRequest, user_id: str = Depends(get_current_user_id)):
    try:
        # 식물 종 정보 가져오기
        species = supabase.table("plant_species").select("*").eq("id", request.species_id).single().execute()
        if not species.data:
            raise HTTPException(status_code=404, detail="식물 종을 찾을 수 없습니다.")

        # 새 식물 데이터 생성
        new_plant = {
            "user_id": user_id,
            "species_id": request.species_id,
            "name": request.name,
            "location": request.location,
            "watering_cycle_days": request.watering_cycle_days,
            "last_watered_at": datetime.now(),
            "next_watering_date": datetime.now() + timedelta(days=request.watering_cycle_days),
            "temp_range_min": species.data.get("temp_range_min"),
            "temp_range_max": species.data.get("temp_range_max"),
            "humidity_range_min": species.data.get("humidity_range_min"),
            "humidity_range_max": species.data.get("humidity_range_max"),
            "light_range_min": species.data.get("light_range_min"),
            "light_range_max": species.data.get("light_range_max")
        }

        response = supabase.table("plants").insert(new_plant).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{plant_id}", response_model=Plant)
async def get_plant(plant_id: str, user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("plants").select("*").eq("id", plant_id).eq("user_id", user_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="식물을 찾을 수 없습니다.")
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{plant_id}", response_model=Plant)
async def update_plant(plant_id: str, request: UpdatePlantRequest, user_id: str = Depends(get_current_user_id)):
    try:
        # 식물 존재 여부 확인
        plant = supabase.table("plants").select("*").eq("id", plant_id).eq("user_id", user_id).single().execute()
        if not plant.data:
            raise HTTPException(status_code=404, detail="식물을 찾을 수 없습니다.")

        # 업데이트할 데이터 준비
        update_data = request.dict(exclude_unset=True)
        
        response = supabase.table("plants").update(update_data).eq("id", plant_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{plant_id}")
async def delete_plant(plant_id: str, user_id: str = Depends(get_current_user_id)):
    try:
        response = supabase.table("plants").delete().eq("id", plant_id).eq("user_id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="식물을 찾을 수 없습니다.")
        return {"message": "식물이 삭제되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{plant_id}/water", response_model=Plant)
async def water_plant(plant_id: str, user_id: str = Depends(get_current_user_id)):
    try:
        # 식물 정보 가져오기
        plant = supabase.table("plants").select("*").eq("id", plant_id).eq("user_id", user_id).single().execute()
        if not plant.data:
            raise HTTPException(status_code=404, detail="식물을 찾을 수 없습니다.")

        # 물주기 정보 업데이트
        now = datetime.now()
        next_watering = now + timedelta(days=plant.data["watering_cycle_days"])
        
        update_data = {
            "last_watered_at": now,
            "next_watering_date": next_watering
        }
        
        response = supabase.table("plants").update(update_data).eq("id", plant_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
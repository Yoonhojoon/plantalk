from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from ..models import Plant
from ..database import supabase

router = APIRouter(
    prefix="/plants",
    tags=["plants"]
)

class CreatePlantRequest(BaseModel):
    species_id: Optional[str] = None
    name: Optional[str] = None
    location: str
    watering_cycle_days: int
    last_watered_at: str  # ISO 형식의 문자열로 받음
    # species_id가 없을 때 필요한 필드들
    temp_range_min: Optional[float] = None
    temp_range_max: Optional[float] = None
    humidity_range_min: Optional[float] = None
    humidity_range_max: Optional[float] = None
    light_range_min: Optional[float] = None
    light_range_max: Optional[float] = None

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
        # ISO 형식의 문자열을 datetime으로 변환
        last_watered_at = datetime.fromisoformat(request.last_watered_at.replace('Z', '+00:00'))
        
        # 기본 데이터 준비
        new_plant = {
            "user_id": user_id,
            "name": request.name,
            "location": request.location,
            "watering_cycle_days": request.watering_cycle_days,
            "last_watered_at": last_watered_at.isoformat(),
            "next_watering_date": (last_watered_at + timedelta(days=request.watering_cycle_days)).isoformat(),
        }

        # species_id가 있는 경우와 없는 경우 분기 처리
        if request.species_id:
            # 식물 종 정보 가져오기
            species = supabase.table("plant_species").select("*").eq("id", request.species_id).single().execute()
            if not species.data:
                raise HTTPException(status_code=404, detail="식물 종을 찾을 수 없습니다.")
            
            # species_id와 기준값 설정
            new_plant.update({
                "species_id": request.species_id,
                "temp_range_min": species.data.get("temp_range_min"),
                "temp_range_max": species.data.get("temp_range_max"),
                "humidity_range_min": species.data.get("humidity_range_min"),
                "humidity_range_max": species.data.get("humidity_range_max"),
                "light_range_min": species.data.get("light_range_min"),
                "light_range_max": species.data.get("light_range_max")
            })
        else:
            # species_id가 없는 경우, 직접 입력한 기준값 사용
            if not all([
                request.temp_range_min is not None,
                request.temp_range_max is not None,
                request.humidity_range_min is not None,
                request.humidity_range_max is not None,
                request.light_range_min is not None,
                request.light_range_max is not None
            ]):
                raise HTTPException(
                    status_code=400,
                    detail="species_id가 없는 경우 모든 기준값(temp_range_min/max, humidity_range_min/max, light_range_min/max)을 입력해야 합니다."
                )
            
            new_plant.update({
                "temp_range_min": request.temp_range_min,
                "temp_range_max": request.temp_range_max,
                "humidity_range_min": request.humidity_range_min,
                "humidity_range_max": request.humidity_range_max,
                "light_range_min": request.light_range_min,
                "light_range_max": request.light_range_max
            })

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
            "last_watered_at": now.isoformat(),
            "next_watering_date": next_watering.isoformat()
        }
        
        response = supabase.table("plants").update(update_data).eq("id", plant_id).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
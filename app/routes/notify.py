from fastapi import APIRouter, HTTPException
from typing import Dict
import uuid
from datetime import datetime

from app.database import get_plant_by_sensor_id, supabase
from app.schemas.notify import SensorData, NotifyResponse

router = APIRouter()

def analyze_plant_emotion(plant: dict, temp: float, humid: float, light: float) -> Dict[str, str]:
    emotions = []
    messages = []
    
    # 온도 분석
    if temp < plant["temp_range_min"]:
        emotions.append("추움")
        messages.append(f"온도가 너무 낮습니다. (현재: {temp}°C, 권장: {plant['temp_range_min']}~{plant['temp_range_max']}°C)")
    elif temp > plant["temp_range_max"]:
        emotions.append("더움")
        messages.append(f"온도가 너무 높습니다. (현재: {temp}°C, 권장: {plant['temp_range_min']}~{plant['temp_range_max']}°C)")
    
    # 습도 분석
    if humid < plant["humidity_range_min"]:
        emotions.append("건조함")
        messages.append(f"습도가 너무 낮습니다. (현재: {humid}%, 권장: {plant['humidity_range_min']}~{plant['humidity_range_max']}%)")
    elif humid > plant["humidity_range_max"]:
        emotions.append("습함")
        messages.append(f"습도가 너무 높습니다. (현재: {humid}%, 권장: {plant['humidity_range_min']}~{plant['humidity_range_max']}%)")
    
    # 조도 분석
    if light < plant["light_range_min"]:
        emotions.append("어두움")
        messages.append(f"빛이 너무 부족합니다. (현재: {light}lux, 권장: {plant['light_range_min']}~{plant['light_range_max']}lux)")
    elif light > plant["light_range_max"]:
        emotions.append("밝음")
        messages.append(f"빛이 너무 강합니다. (현재: {light}lux, 권장: {plant['light_range_min']}~{plant['light_range_max']}lux)")
    
    if not emotions:
        return {
            "emotion": "행복",
            "message": "식물이 적절한 환경에서 잘 자라고 있습니다."
        }
    
    return {
        "emotion": ", ".join(emotions),
        "message": " ".join(messages)
    }

@router.post("/notify", response_model=NotifyResponse)
async def notify_sensor_data(data: SensorData):
    # 센서 ID로 식물 찾기
    plant = await get_plant_by_sensor_id(data.sensor_id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    # 식물 상태 분석
    analysis = analyze_plant_emotion(plant, data.temperature, data.humidity, data.light)
    
    # 상태 로그 데이터 준비
    status_log_data = {
        "plant_id": plant["id"],
        "sensor_id": data.sensor_id,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "light": data.light,
        "emotion": analysis["emotion"],
        "created_at": datetime.now().isoformat()
    }
    
    try:
        # 기존 레코드가 있는지 확인
        existing_log = supabase.table("plant_status_logs").select("*").eq("plant_id", plant["id"]).execute()
        
        if existing_log.data and len(existing_log.data) > 0:
            # 기존 레코드 업데이트
            status_log = supabase.table("plant_status_logs").update(status_log_data).eq("plant_id", plant["id"]).execute()
        else:
            # 새 레코드 생성
            status_log_data["id"] = str(uuid.uuid4())
            status_log = supabase.table("plant_status_logs").insert(status_log_data).execute()
        
        return {
            "status": "success",
            "emotion": analysis["emotion"],
            "message": analysis["message"],
            "plant_status_log": status_log.data[0] if status_log.data else None
        }
    except Exception as e:
        print(f"Error: {str(e)}")  # 에러 로깅 추가
        raise HTTPException(status_code=500, detail=str(e)) 
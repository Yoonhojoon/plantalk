from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class SensorData(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    light: float

class PlantStatusLogResponse(BaseModel):
    id: str
    plant_id: str
    temperature: float
    humidity: float
    light: float
    emotion: str
    created_at: datetime

    class Config:
        from_attributes = True

class NotifyResponse(BaseModel):
    status: str
    emotion: str
    message: str
    plant_status_log: Optional[Dict[str, Any]] 
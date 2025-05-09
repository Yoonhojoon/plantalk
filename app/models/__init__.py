from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class User(BaseModel):
    id: UUID
    nickname: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class PlantSpecies(BaseModel):
    id: UUID
    name: str
    scientific_name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    temp_range_min: Optional[float] = None
    temp_range_max: Optional[float] = None
    humidity_range_min: Optional[float] = None
    humidity_range_max: Optional[float] = None
    light_range_min: Optional[float] = None
    light_range_max: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)

class Plant(BaseModel):
    id: UUID
    user_id: UUID
    species_id: Optional[UUID] = None
    name: Optional[str] = None
    image_url: Optional[str] = None
    location: str
    sensor_id: Optional[str] = None
    watering_cycle_days: Optional[int] = None
    last_watered_at: Optional[datetime] = None
    next_watering_date: Optional[datetime] = None
    temp_range_min: Optional[float] = None
    temp_range_max: Optional[float] = None
    humidity_range_min: Optional[float] = None
    humidity_range_max: Optional[float] = None
    light_range_min: Optional[float] = None
    light_range_max: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)

class PlantStatusLog(BaseModel):
    id: UUID
    plant_id: UUID
    sensor_id: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    light: Optional[float] = None
    emotion: Optional[str] = None
    emotion_icon: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

class Notification(BaseModel):
    id: UUID
    user_id: UUID
    plant_id: UUID
    title: str
    type: str
    status: str
    created_at: datetime = Field(default_factory=datetime.now)
    read_at: Optional[datetime] = None

# Supabase 테이블 정의
TABLES = {
    "users": {
        "id": "uuid",
        "email": "text",
        "password": "text",
        "nickname": "text",
        "created_at": "timestamp with time zone"
    },
    "plants": {
        "id": "uuid",
        "user_id": "uuid",
        "species_id": "uuid",
        "name": "text",
        "location": "text",
        "sensor_id": "text",
        "watering_cycle_days": "integer",
        "last_watered_at": "timestamp with time zone",
        "next_watering_date": "timestamp with time zone",
        "temp_range_min": "float",
        "temp_range_max": "float",
        "humidity_range_min": "float",
        "humidity_range_max": "float",
        "light_range_min": "float",
        "light_range_max": "float",
        "created_at": "timestamp with time zone"
    },
    "plant_status_logs": {
        "id": "uuid",
        "plant_id": "uuid",
        "sensor_id": "text",
        "temperature": "float",
        "humidity": "float",
        "light": "float",
        "emotion": "text",
        "created_at": "timestamp with time zone"
    },
    "species": {
        "id": "uuid",
        "name": "text",
        "scientific_name": "text",
        "description": "text",
        "image_url": "text",
        "temp_range_min": "float",
        "temp_range_max": "float",
        "humidity_range_min": "float",
        "humidity_range_max": "float",
        "light_range_min": "float",
        "light_range_max": "float",
        "created_at": "timestamp with time zone"
    },
    "notifications": {
        "id": "uuid",
        "user_id": "uuid",
        "plant_id": "uuid",
        "title": "text",
        "type": "text",
        "status": "text",
        "created_at": "timestamp with time zone",
        "read_at": "timestamp with time zone"
    }
} 
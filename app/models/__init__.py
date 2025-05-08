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
    species_id: UUID
    name: Optional[str] = None
    image_url: Optional[str] = None
    location: str
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
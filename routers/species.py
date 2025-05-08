from fastapi import APIRouter, HTTPException
from typing import List
from models import PlantSpecies
from database import supabase

router = APIRouter(
    prefix="/species",
    tags=["species"]
)

@router.get("", response_model=List[PlantSpecies])
async def get_species_list():
    try:
        response = supabase.table("plant_species").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
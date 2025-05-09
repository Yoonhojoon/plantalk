import os
from dotenv import load_dotenv
from supabase import create_client, Client

# .env 파일 로드
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL과 SUPABASE_KEY가 .env 파일에 설정되어 있어야 합니다.")

supabase: Client = create_client(url, key)

# 데이터베이스 헬퍼 함수들
async def get_user_by_id(user_id: str):
    response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    return response.data

async def update_user(user_id: str, data: dict):
    response = supabase.table("users").update(data).eq("id", user_id).execute()
    return response.data

async def get_plant_by_sensor_id(sensor_id: str):
    try:
        response = supabase.table("plants").select("*").eq("sensor_id", sensor_id).single().execute()
        return response.data
    except Exception as e:
        if "PGRST116" in str(e):  # 결과가 없는 경우
            return None
        raise e  # 다른 오류는 그대로 전파

async def create_plant_status_log(data: dict):
    response = supabase.table("plant_status_logs").insert(data).execute()
    return response.data 
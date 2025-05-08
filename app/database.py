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
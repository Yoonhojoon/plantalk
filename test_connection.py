from app.database import supabase
import os

def test_connection():
    try:
        print("Supabase 연결 테스트 시작...")
        print(f"URL: {os.environ.get('SUPABASE_URL')}")
        
        # plant_species 테이블 조회
        response = supabase.table('plant_species').select("*").execute()
        print("\n연결 성공!")
        print("\nplant_species 테이블 데이터:")
        for row in response.data:
            print(row)
        return True
    except Exception as e:
        print("\n연결 실패:")
        print(f"에러 메시지: {str(e)}")
        
        if "'code': '42P01'" in str(e):
            print("\n참고: 'users' 테이블이 없는 것 같습니다.")
            print("이는 정상적인 상황일 수 있습니다. 데이터베이스에 연결은 성공했지만 테이블이 아직 생성되지 않았을 수 있습니다.")
        return False

if __name__ == "__main__":
    test_connection() 
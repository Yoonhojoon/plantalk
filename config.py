from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str = "https://xzoaccsuzkrkowlqkmpb.supabase.co"
    SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh6b2FjY3N1emtya293bHFrbXBiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NjcxMTExNSwiZXhwIjoyMDYyMjg3MTE1fQ.M_EV_2i4XOdzRrOLVsmQsSNrOYTcAScD40jfInNyeD8"

    class Config:
        env_file = ".env"

settings = Settings() 
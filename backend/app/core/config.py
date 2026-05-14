from pydantic import BaseModel
import os

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://agento:agento@db:5432/agento")
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

settings = Settings()

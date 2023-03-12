from functools import lru_cache
import os
from pydantic import BaseSettings, PostgresDsn
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: PostgresDsn = os.getenv("DATABASE_URL", '')
    hugging_face_api: str = os.getenv('HUGGING_FACE_API', '')
    hugging_face_token: str = os.getenv("HUGGING_FACE_TOKEN", '')
    easy_ocr_api: str = os.getenv('EASY_OCR_API', '')
    easy_ocr_token: str = os.getenv('EASY_OCR_TOKEN', '')


@lru_cache
def settings() -> Settings:
    settings = Settings()
    return settings
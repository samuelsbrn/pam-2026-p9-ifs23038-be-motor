import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_PORT = int(os.getenv("APP_PORT", "5000"))
    BASE_URL = (os.getenv("LLM_BASE_URL") or "").strip()
    LLM_TOKEN = (os.getenv("LLM_TOKEN") or "").strip()
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-key-minimum-32chars")
    JWT_EXPIRES_IN_HOURS = int(os.getenv("JWT_EXPIRES_IN_HOURS", "24"))
    DEFAULT_ADMIN_USERNAME = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
    DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")
    DEFAULT_ADMIN_ROLE = os.getenv("DEFAULT_ADMIN_ROLE", "admin")
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

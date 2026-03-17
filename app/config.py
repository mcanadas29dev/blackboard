import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-insegura")
    PIZARRA_DB_PATH = os.environ.get("PIZARRA_DB_PATH", "data/ipizarra.db")
    USERS_DB_PATH = os.environ.get("USERS_DB_PATH", "data/users.db")
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

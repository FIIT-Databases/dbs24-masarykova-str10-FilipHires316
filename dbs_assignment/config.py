from pydantic_settings import BaseSettings
import dotenv
import os


class Settings(BaseSettings):
    class Config:
        case_sensitive = True

    dotenv.load_dotenv()
    DATABASE_HOST: str = os.getenv("DATABASE_HOST")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    DATABASE_USER: str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")


settings = Settings()

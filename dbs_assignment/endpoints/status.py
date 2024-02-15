import psycopg2
import dotenv
import os
from fastapi import APIRouter
from dbs_assignment.config import settings


router = APIRouter()

dotenv.load_dotenv()
settings.DATABASE_HOST = os.getenv("DATABASE_HOST")
settings.DATABASE_PORT = os.getenv("DATABASE_PORT")
settings.DATABASE_NAME = os.getenv("DATABASE_NAME")
settings.DATABASE_USER = os.getenv("DATABASE_USER")
settings.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")


@router.get('/v1/status')
async def get_status():
    postgres_version = get_postgres_version()
    response = {
        "version": postgres_version
    }
    return response


def get_postgres_version():
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    connection.close()
    return version

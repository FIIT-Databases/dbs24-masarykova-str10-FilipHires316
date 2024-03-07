import psycopg2
from fastapi import APIRouter
from dbs_assignment.config import settings


router = APIRouter()


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

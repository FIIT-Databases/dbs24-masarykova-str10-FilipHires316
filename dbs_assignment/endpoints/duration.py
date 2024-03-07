import psycopg2
from fastapi import APIRouter, Query
from dbs_assignment.config import settings


router = APIRouter()


query = """
SELECT id, creationdate, viewcount, lasteditdate, lastactivitydate, title, closeddate, ROUND(EXTRACT(EPOCH FROM (closeddate - creationdate)) / 60, 2) AS duration  FROM posts
WHERE closeddate IS NOT null and ROUND(EXTRACT(EPOCH FROM (closeddate - creationdate)) / 60, 2) < %s
ORDER BY creationdate DESC
LIMIT %s;
"""


@router.get('/v2/posts/')
async def get_duration(duration: int = Query(...), limit: int = Query(...)):
    postgres_duration = get_postgres_duration(duration, limit)
    response = [
        {
         "id": row[0],
         "creationdate": row[1].isoformat() if row[1] is not None else None,
         "viewcount": row[2],
         "lasteditdate": row[3] if row[3] is not None else None,
         "lastactivitydate": row[4].isoformat() if row[4] is not None else None,
         "title": row[5],
         "closeddate": row[6].isoformat() if row[6] is not None else None,
         "duration": row[7]
         }
        for row in postgres_duration
    ]
    return {"items": response}


def get_postgres_duration(duration, limit):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = connection.cursor()
    cursor.execute(query, (duration, limit,))
    version = cursor.fetchall()
    connection.close()
    return version

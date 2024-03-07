import psycopg2
from fastapi import APIRouter, Query
from dbs_assignment.config import settings


router = APIRouter()


query = """
SELECT closeddate, creationdate, ROUND(EXTRACT(EPOCH FROM (closeddate - creationdate)) / 60, 2) AS duration, id, lastactivitydate, lasteditdate, title, viewcount FROM posts
WHERE closeddate IS NOT null and ROUND(EXTRACT(EPOCH FROM (closeddate - creationdate)) / 60, 2) < %s
ORDER BY creationdate DESC
LIMIT %s;
"""


@router.get('/v2/posts/')
async def get_duration(duration: int = Query(...), limit: int = Query(...)):
    postgres_duration = get_postgres_duration(duration, limit)
    response = [
        {
         "closeddate": row[0].isoformat().split('+')[0].rstrip('0') + row[0].isoformat()[26:29] if row[0] is not None else None,
         "creationdate": row[1].isoformat().split('+')[0].rstrip('0') + row[1].isoformat()[26:29] if row[1] is not None else None,
         "duration": row[2],
         "id": row[3],
         "lastactivitydate": row[4].isoformat().split('+')[0].rstrip('0') + row[4].isoformat()[26:29] if row[4] is not None else None,
         "lasteditdate": row[5].isoformat().split('+')[0].rstrip('0') + row[5].isoformat()[26:29] if row[5] is not None else None,
         "title": row[6],
         "viewcount": row[7],
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

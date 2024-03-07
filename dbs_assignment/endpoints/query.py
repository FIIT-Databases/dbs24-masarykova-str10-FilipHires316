import psycopg2
from fastapi import APIRouter, Query
from dbs_assignment.config import settings


router = APIRouter()


my_query = """
WITH temp AS (SELECT posts.id, posts.creationdate, posts.viewcount, posts.lasteditdate, posts.lastactivitydate, posts.title, posts.closeddate FROM posts
WHERE (posts.title ILIKE %s OR posts.body ILIKE %s)
ORDER BY creationdate DESC
LIMIT %s)
SELECT temp.id, temp.creationdate, temp.viewcount, temp.lasteditdate, temp.lastactivitydate, temp.title, temp.closeddate, array_agg(tags.tagname) FROM temp
JOIN post_tags ON temp.id = post_tags.post_id
JOIN tags ON post_tags.tag_id = tags.id
GROUP BY temp.id, temp.creationdate, temp.viewcount, temp.lasteditdate, temp.lastactivitydate, temp.title, temp.closeddate;
"""


@router.get('/v2/posts')
async def get_duration(limit: int = Query(...), query: str = Query(...)):
    postgres_duration = get_postgres_duration(limit, query)
    response = [
        {
         "id": row[0],
         "creationdate": row[1].isoformat() if row[1] is not None else None,
         "viewcount": row[2],
         "lasteditdate": row[3] if row[3] is not None else None,
         "lastactivitydate": row[4].isoformat() if row[4] is not None else None,
         "title": row[5],
         "closeddate": row[6].isoformat() if row[6] is not None else None,
         "tags": row[7]
         }
        for row in postgres_duration
    ]
    return {"items": response}


def get_postgres_duration(limit, query):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = connection.cursor()
    cursor.execute(my_query, (f'%{query}%', f'%{query}%', limit,))
    version = cursor.fetchall()
    connection.close()
    return version

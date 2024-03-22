from typing import Optional

import psycopg2
from dbs_assignment.date_formating import date_formating
from fastapi import APIRouter, Query
from dbs_assignment.config import settings


router = APIRouter()


query = """
SELECT users.displayname, posts.body, posts.creationdate FROM posts
JOIN users ON posts.owneruserid = users.id
WHERE posts.id = %s
UNION
(SELECT users.displayname, posts.body, posts.creationdate FROM posts
JOIN users ON posts.owneruserid = users.id
WHERE posts.parentid = %s
ORDER BY posts.creationdate ASC
LIMIT %s - 1);
"""


@router.get('/v3/posts/{postid}')
async def get_postid(postid, limit: Optional[int] = Query(None)):
    postgres_postid = get_postgres_postid(postid, limit)
    response = [
        {
         "displayname": row[0],
         "body": row[1],
         "created_at": date_formating(row[2])
         }
        for row in postgres_postid
    ]
    return {"items": response}


def get_postgres_postid(postid, limit):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = connection.cursor()
    cursor.execute(query, (postid, postid, limit,))
    version = cursor.fetchall()
    connection.close()
    return version

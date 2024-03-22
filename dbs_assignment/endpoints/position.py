from typing import Optional

import psycopg2
from dbs_assignment.date_formating import date_formating
from fastapi import APIRouter, Query
from dbs_assignment.config import settings


router = APIRouter()


query = """
SELECT id, displayname, body, text, score, position FROM
(SELECT comments.id, users.displayname, posts.body, comments.text, comments.score,
ROW_NUMBER() OVER (PARTITION BY posts.id ORDER BY comments.creationdate ASC) AS position
FROM comments
JOIN posts on comments.postid = posts.id
JOIN post_tags ON posts.id = post_tags.post_id
JOIN tags ON post_tags.tag_id = tags.id
JOIN users ON comments.userid = users.id
WHERE tags.tagname = %s
ORDER BY posts.creationdate ASC)
WHERE position = %s
LIMIT %s
"""


@router.get('/v3/tags/{tagname}/comments/{position}')
async def get_position(tagname, position, limit: Optional[int] = Query(None)):
    postgres_position = get_postgres_position(tagname, position, limit)
    response = [
        {
         "id": row[0],
         "displayname": row[1],
         "body": row[2],
         "text": row[3],
         "score": row[4],
         "position": row[5]
         }
        for row in postgres_position
    ]
    return {"items": response}


def get_postgres_position(tagname, position, limit):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = connection.cursor()
    cursor.execute(query, (tagname, position, limit,))
    version = cursor.fetchall()
    connection.close()
    return version

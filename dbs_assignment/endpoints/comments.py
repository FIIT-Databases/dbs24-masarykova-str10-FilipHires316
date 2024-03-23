from typing import Optional

import psycopg2
from dbs_assignment.date_formating import date_formating, time_formating
from fastapi import APIRouter, Query
from dbs_assignment.config import settings


router = APIRouter()


query = """
SELECT posts.id, posts.title, users.displayname, comments.text, posts.creationdate, comments.creationdate,
CASE WHEN comments.creationdate - LAG(comments.creationdate) OVER (PARTITION BY posts.id ORDER BY posts.creationdate ASC, comments.creationdate ASC) IS null THEN comments.creationdate - posts.creationdate
ELSE comments.creationdate - LAG(comments.creationdate) OVER (PARTITION BY posts.id ORDER BY posts.creationdate ASC, comments.creationdate ASC)
END AS diff,
(comments.creationdate - posts.creationdate) / ROW_NUMBER() OVER (PARTITION BY posts.id ORDER BY comments.creationdate) AS avg
FROM comments
JOIN posts on comments.postid = posts.id
JOIN post_tags ON posts.id = post_tags.post_id
JOIN tags ON post_tags.tag_id = tags.id
JOIN users on comments.userid = users.id
WHERE tags.tagname = %s and posts.commentcount > %s
ORDER BY posts.creationdate ASC, comments.creationdate ASC;
"""


@router.get('/v3/tags/{tag}/comments')
async def get_comments(tag, count: Optional[int] = Query(None)):
    postgres_comments = get_postgres_comments(tag, count)
    response = [
        {
         "post_id": row[0],
         "title": row[1],
         "displayname": row[2],
         "text": row[3],
         "post_created_at": date_formating(row[4]),
         "created_at": date_formating(row[5]),
         "diff": time_formating(row[6]),
         "avg": time_formating(row[7])
         }
        for row in postgres_comments
    ]
    return {"items": response}


def get_postgres_comments(tag, count):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = connection.cursor()
    cursor.execute(query, (tag, count,))
    version = cursor.fetchall()
    connection.close()
    return version

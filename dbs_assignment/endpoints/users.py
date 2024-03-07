import psycopg2
from dbs_assignment.date_formating import date_formating
from fastapi import APIRouter
from dbs_assignment.config import settings


router = APIRouter()


query = """
    SELECT users.* FROM users
    JOIN comments on users.id = comments.userid
    WHERE comments.postid = %s
    GROUP BY users.id
    ORDER BY MAX(comments.creationdate) DESC;
"""


@router.get('/v2/posts/{post_id}/users')
async def get_users(post_id):
    postgres_users = get_postgres_users(post_id)
    response = [
        {
         "id": row[0],
         "reputation": row[1],
         "creationdate": date_formating(row[2]),
         "displayname": row[3],
         "lastaccessdate": date_formating(row[4]),
         "websiteurl": row[5],
         "location": row[6],
         "aboutme": row[7],
         "views": row[8],
         "upvotes": row[9],
         "downvotes": row[10],
         "profileimageurl": row[11],
         "age": row[12],
         "accountid": row[13]
         }
        for row in postgres_users
    ]
    return {"items": response}


def get_postgres_users(post_id):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = connection.cursor()
    cursor.execute(query, (post_id,))
    version = cursor.fetchall()
    connection.close()
    return version

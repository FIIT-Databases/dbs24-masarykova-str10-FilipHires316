import psycopg2
from fastapi import APIRouter
from dbs_assignment.config import settings


router = APIRouter()


query = """
SELECT DISTINCT users.* FROM (
    SELECT comments.userid
    FROM users
    JOIN posts ON users.id = posts.owneruserid
    JOIN comments ON posts.id = comments.postid
    WHERE posts.owneruserid = %s or comments.userid = %s
) AS first
JOIN users ON first.userid = users.id
ORDER BY creationdate ASC;
"""


@router.get('/v2/users/{user_id}/friends')
async def get_friends(user_id):
    postgres_friends = get_postgres_friends(user_id)
    response = [
        {
         "id": row[0],
         "reputation": row[1],
         "creationdate": row[2].isoformat(),
         "displayname": row[3],
         "lastaccessdate": row[4].isoformat(),
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
        for row in postgres_friends
    ]
    return {"items": response}


def get_postgres_friends(user_id):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = connection.cursor()
    cursor.execute(query, (user_id, user_id,))
    version = cursor.fetchall()
    connection.close()
    return version

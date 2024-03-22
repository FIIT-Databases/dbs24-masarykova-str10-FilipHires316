import psycopg2
from dbs_assignment.date_formating import date_formating
from fastapi import APIRouter
from dbs_assignment.config import settings


router = APIRouter()


query = """
SELECT id, title, type, created_at,
CASE WHEN MOD(ROW_NUMBER() OVER (ORDER BY created_at ASC), 2) = 0 THEN (ROW_NUMBER() OVER (ORDER BY created_at ASC) - 1) / 2 + 1
ELSE ROW_NUMBER() OVER (ORDER BY created_at ASC) / 2 + 1
END AS position
FROM
(SELECT *, LAG(type) OVER (ORDER BY created_at ASC) AS prev_type, LAG(type) OVER (ORDER BY created_at DESC) AS next_type FROM
(SELECT badges.id, badges.name AS title, 'badge' AS type, badges.date AS created_at FROM users
JOIN badges on users.id = userid
WHERE users.id = %s
UNION
SELECT posts.id, posts.title, 'post' AS type, posts.creationdate AS created_at FROM users
JOIN posts on users.id = posts.owneruserid
JOIN comments on users.id = comments.userid
WHERE users.id = %s
ORDER BY created_at ASC, title DESC))
WHERE (type = 'badge' and prev_type = 'post') or (type = 'post' and next_type = 'badge');
"""


@router.get('/v3/users/{user_id}/badge_history')
async def get_badge(user_id):
    postgres_badge = get_postgres_badge(user_id)
    response = [
        {
         "id": row[0],
         "title": row[1],
         "type": row[2],
         "created_at": date_formating(row[3]),
         "position": row[4]
         }
        for row in postgres_badge
    ]
    return {"items": response}


def get_postgres_badge(user_id):
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

import psycopg2
from fastapi import APIRouter
from dbs_assignment.config import settings

router = APIRouter()

query = """
WITH temp_posts AS (SELECT
CASE WHEN EXTRACT(DOW FROM posts.creationdate::timestamp) = 0 THEN 7
ELSE EXTRACT(DOW FROM posts.creationdate::timestamp)
END AS number_of_week,
SUM(CASE WHEN tags.tagname = %s THEN 1 ELSE 0 END) AS linux_posts,
COUNT(*) AS total_posts
FROM posts
JOIN post_tags ON posts.id = post_tags.post_id
JOIN tags ON post_tags.tag_id = tags.id
GROUP BY number_of_week)
SELECT ROUND(linux_posts * 100.0 / total_posts, 2) AS percentage FROM temp_posts
ORDER BY number_of_week;
"""


@router.get('/v2/tags/{tagname}/stats')
async def get_stats(tagname):
    postgres_stats = get_postgres_stats(tagname)
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    response = {}
    for i in range(len(days_of_week)):
        response[days_of_week[i]] = postgres_stats[i][0]
    return {"result": response}


def get_postgres_stats(tagname):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = connection.cursor()
    cursor.execute(query, (tagname,))
    version = cursor.fetchall()
    connection.close()
    return version

from typing import Union, Optional

import psycopg2
from dbs_assignment.date_formating import date_formating
from fastapi import APIRouter, Query
from dbs_assignment.config import settings

router = APIRouter()

query1 = """
SELECT closeddate, creationdate, ROUND(EXTRACT(EPOCH FROM (closeddate - creationdate)) / 60, 2) AS duration, id, lastactivitydate, lasteditdate, title, viewcount FROM posts
WHERE closeddate IS NOT null and ROUND(EXTRACT(EPOCH FROM (closeddate - creationdate)) / 60, 2) < %s
ORDER BY creationdate DESC
LIMIT %s;
"""
query2 = """
WITH temp AS (SELECT answercount, body, closeddate, creationdate, id, lastactivitydate, lasteditdate, title, viewcount FROM posts
WHERE (posts.title ILIKE %s OR posts.body ILIKE %s)
ORDER BY creationdate DESC
LIMIT %s)
SELECT temp.answercount, temp.body, temp.closeddate, temp.creationdate, temp.id, temp.lastactivitydate, temp.lasteditdate, array_agg(tags.tagname), temp.title, temp.viewcount FROM temp
JOIN post_tags ON temp.id = post_tags.post_id
JOIN tags ON post_tags.tag_id = tags.id
GROUP BY temp.answercount, temp.body, temp.closeddate, temp.creationdate, temp.id, temp.lastactivitydate, temp.lasteditdate, temp.title, temp.viewcount;
"""


@router.get('/v2/posts')
async def identify_params(duration: Optional[int] = Query(None), limit: Optional[int] = Query(None), query: Optional[str] = Query(None)):
    if duration is not None:
        return get_duration(duration, limit)
    elif query is not None:
        return get_query(limit, query)


def get_duration(duration, limit):
    postgres_duration = get_postgres_duration(duration, limit)
    response = [
        {
            "closeddate": date_formating(row[0]),
            "creationdate": date_formating(row[1]),
            "duration": row[2],
            "id": row[3],
            "lastactivitydate": date_formating(row[4]),
            "lasteditdate": date_formating(row[5]),
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
    cursor.execute(query1, (duration, limit,))
    version = cursor.fetchall()
    connection.close()
    return version


def get_query(limit, query):
    postgres_query = get_postgres_query(limit, query)
    response = [
        {
            "answercount": row[0],
            "body": row[1],
            "closeddate": date_formating(row[2]),
            "creationdate": date_formating(row[3]),
            "id": row[4],
            "lastactivitydate": date_formating(row[5]),
            "lasteditdate": date_formating(row[6]),
            "tags": row[7],
            "title": row[8],
            "viewcount": row[9]
        }
        for row in postgres_query
    ]
    return {"items": response}


def get_postgres_query(limit, query):
    connection = psycopg2.connect(
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT
    )
    cursor = connection.cursor()
    cursor.execute(query2, (f'%{query}%', f'%{query}%', limit,))
    version = cursor.fetchall()
    connection.close()
    return version

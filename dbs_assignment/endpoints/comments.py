from typing import Optional

import psycopg2
from dbs_assignment.date_formating import date_formating
from fastapi import APIRouter, Query
from dbs_assignment.config import settings


router = APIRouter()


query = """

"""


@router.get('/v3/tags/{tag}/comments')
async def get_comments(tag, count: Optional[int] = Query(None)):
    postgres_comments = get_postgres_comments(tag, count)
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

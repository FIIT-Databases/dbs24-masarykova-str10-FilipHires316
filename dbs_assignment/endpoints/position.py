from typing import Optional

import psycopg2
from dbs_assignment.date_formating import date_formating
from fastapi import APIRouter, Query
from dbs_assignment.config import settings


router = APIRouter()


query = """

"""


@router.get('/v3/tags/{tagname}/comments/{position}')
async def get_position(tagname, position, limit: Optional[int] = Query(None)):
    postgres_position = get_postgres_position(tagname, position, limit)
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

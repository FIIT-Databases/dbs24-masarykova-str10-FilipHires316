from dbs_assignment.config import settings
from fastapi import APIRouter
router = APIRouter()


@router.get("/v1/hello")
async def hello():
    return {
        'hello': settings.NAME
    }

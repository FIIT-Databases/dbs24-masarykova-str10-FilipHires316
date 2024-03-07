from fastapi import APIRouter
from dbs_assignment.endpoints import status, users, friends, stats, duration, query

router = APIRouter()
router.include_router(status.router, tags=["status"])
router.include_router(users.router, tags=["users"])
router.include_router(friends.router, tags=["friends"])
router.include_router(stats.router, tags=["stats"])
router.include_router(duration.router, tags=["duration"])
router.include_router(query.router, tags=["query"])

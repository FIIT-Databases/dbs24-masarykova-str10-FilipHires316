from fastapi import APIRouter
from dbs_assignment.endpoints import status, users, friends, stats, posts

router = APIRouter()
router.include_router(status.router, tags=["status"])
router.include_router(users.router, tags=["users"])
router.include_router(friends.router, tags=["friends"])
router.include_router(stats.router, tags=["stats"])
router.include_router(posts.router, tags=["posts"])

from fastapi import APIRouter
from dbs_assignment.endpoints import status, users, friends, stats, posts, badge, comments, position, postid

router = APIRouter()
router.include_router(status.router)
router.include_router(users.router)
router.include_router(friends.router)
router.include_router(stats.router)
router.include_router(posts.router)
router.include_router(badge.router)
router.include_router(comments.router)
router.include_router(position.router)
router.include_router(postid.router)

from fastapi import APIRouter
from dbs_assignment.endpoints import status, users, friends, stats, posts, badge, comments, position, postid

router = APIRouter()
router.include_router(status.router, tags=["status"])
router.include_router(users.router, tags=["users"])
router.include_router(friends.router, tags=["friends"])
router.include_router(stats.router, tags=["stats"])
router.include_router(posts.router, tags=["posts"])
router.include_router(badge.router, tags=["badge"])
router.include_router(comments.router, tags=["comments"])
router.include_router(position.router, tags=["position"])
router.include_router(postid.router, tags=["postid"])

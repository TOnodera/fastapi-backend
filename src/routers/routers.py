from fastapi import APIRouter
from src.routers.users import router as users_router
from src.routers.storages import router as storages_router

router = APIRouter()

router.include_router(users_router, tags=["ユーザー"])
router.include_router(storages_router, tags=["ストレージ"])

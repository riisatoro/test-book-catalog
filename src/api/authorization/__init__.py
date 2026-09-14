from fastapi import APIRouter

from api.authorization.login import router as login_router
from api.authorization.register import router as register_router

router = APIRouter(tags=["Authorization"])
router.include_router(login_router)
router.include_router(register_router)

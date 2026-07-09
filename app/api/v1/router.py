"""v1 路由聚合。"""

from fastapi import APIRouter

from app.api.v1.endpoints.template import router as template_router

router = APIRouter()
router.include_router(template_router, tags=["template"])

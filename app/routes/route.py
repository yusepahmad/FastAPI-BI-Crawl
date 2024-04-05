from fastapi import APIRouter
from ..service.service_code import router as dana_inflasi


router = APIRouter()

router.include_router(dana_inflasi, tags=["Automation Playwright"], prefix="/api/v1")
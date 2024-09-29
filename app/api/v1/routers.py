from fastapi import APIRouter

from app.core.config import settings
from .endpoints.cat import router as cat_router
from .endpoints.breed import router as breed_router


api_router = APIRouter()

# REST
api_router.include_router(cat_router)
api_router.include_router(breed_router)

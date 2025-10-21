from fastapi import APIRouter

from app.api.v1.endpoints import personas

api_router = APIRouter()

api_router.include_router(personas.router, prefix="/personas", tags=["personas"])

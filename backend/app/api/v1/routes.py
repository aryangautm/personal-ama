from fastapi import APIRouter, Depends

from app.api.v1.endpoints import personas, chat
from app.core.auth import require_api_key

api_router = APIRouter()

api_router.include_router(personas.router, prefix="/personas", tags=["personas"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

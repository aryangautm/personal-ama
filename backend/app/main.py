from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.core.config import settings
from app.api.v1.routes import api_router
from app.memory.checkpointers import pg_checkpointer
from app.core.security import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the application's lifespan events.
    """
    pg_checkpointer.setup()
    yield


app = FastAPI(title="AMA API", lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

allowed_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to the AMA API"}

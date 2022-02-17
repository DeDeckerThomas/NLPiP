from functools import lru_cache
from fastapi import FastAPI
from routers.api_router import api_router
from core.config import settings


app = FastAPI(title=settings.APP_NAME)
app.include_router(api_router)

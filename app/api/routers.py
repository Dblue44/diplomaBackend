from fastapi import APIRouter
from app.core import settings
from app.api.v1 import react_app

v1 = APIRouter(prefix=settings.API_V1_STR)

v1.include_router(react_app, prefix='/react', tags=['React'])

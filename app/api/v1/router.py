from fastapi import APIRouter
from app.api.v1.endpoints import idea

api_router = APIRouter()

api_router.include_router(idea.router, prefix="/idea", tags=["Project Ideas"])

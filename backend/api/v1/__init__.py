"""
API v1 router configuration
"""
from fastapi import APIRouter
from backend.api.v1.endpoints import auth

api_router = APIRouter()

# Include auth endpoints
api_router.include_router(auth.router)

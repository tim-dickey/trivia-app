"""
Authentication Pydantic schemas
"""
from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    """Schema for token responses"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class LoginRequest(BaseModel):
    """Schema for login requests"""
    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenPayload(BaseModel):
    """Schema for JWT token payload"""
    sub: str  # user_id
    org_id: str  # organization_id
    roles: list[str]  # user roles

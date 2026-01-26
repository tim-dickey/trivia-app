"""
User Pydantic schemas for validation and serialization
"""
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from backend.models.user import UserRole
from backend.schemas.organization import OrganizationOut


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)
    organization_slug: str = Field(..., min_length=1, max_length=100)


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    email: EmailStr | None = None
    name: str | None = Field(None, min_length=1, max_length=255)


class PasswordChange(BaseModel):
    """Schema for password change"""
    current_password: str = Field(..., min_length=8, max_length=100)
    new_password: str = Field(..., min_length=8, max_length=100)


class UserOut(UserBase):
    """Schema for user responses (password excluded)"""
    id: UUID
    organization_id: UUID
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class UserWithOrganization(UserOut):
    """Schema for user with nested organization data"""
    organization: OrganizationOut

    class Config:
        from_attributes = True

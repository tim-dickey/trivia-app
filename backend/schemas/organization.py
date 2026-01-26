"""
Organization Pydantic schemas for validation and serialization
"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from backend.models.organization import PlanType


class OrganizationBase(BaseModel):
    """Base organization schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=100, pattern=r'^[a-z0-9-]+$')


class OrganizationCreate(OrganizationBase):
    """Schema for creating a new organization"""
    plan: PlanType = PlanType.FREE


class OrganizationUpdate(BaseModel):
    """Schema for updating an organization"""
    name: str | None = Field(None, min_length=1, max_length=255)
    plan: PlanType | None = None


class OrganizationOut(OrganizationBase):
    """Schema for organization responses"""
    id: UUID
    plan: PlanType
    created_at: datetime

    class Config:
        from_attributes = True

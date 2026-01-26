"""
Organization database model
Multi-tenant isolation root entity
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from backend.core.database import Base


class PlanType(str, enum.Enum):
    """Organization subscription plan types"""
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class Organization(Base):
    """
    Organization model for multi-tenant architecture
    Root entity for data isolation
    """
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    plan = Column(Enum(PlanType), nullable=False, default=PlanType.FREE)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}', slug='{self.slug}', plan='{self.plan}')>"

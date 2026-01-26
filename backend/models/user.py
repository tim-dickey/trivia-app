"""
User database model
Multi-tenant user entity with role-based access
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from backend.core.database import Base


class UserRole(str, enum.Enum):
    """User role types for authorization"""
    PARTICIPANT = "participant"
    FACILITATOR = "facilitator"
    ADMIN = "admin"


class User(Base):
    """
    User model with multi-tenant isolation
    All users belong to an organization
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.PARTICIPANT)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}', org_id={self.organization_id})>"

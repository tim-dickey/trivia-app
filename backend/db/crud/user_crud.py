"""
CRUD operations for User model with multi-tenant filtering
"""
from sqlalchemy.orm import Session
from uuid import UUID
from backend.models.user import User, UserRole
from backend.schemas.user import UserCreate, UserUpdate
from backend.core.security import hash_password


def get_user_by_id(db: Session, user_id: UUID, organization_id: UUID) -> User | None:
    """Get user by ID with organization filtering"""
    return db.query(User).filter(
        User.id == user_id,
        User.organization_id == organization_id
    ).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get user by email (global lookup for authentication)"""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, organization_id: UUID, skip: int = 0, limit: int = 100) -> list[User]:
    """Get list of users for an organization"""
    return db.query(User).filter(
        User.organization_id == organization_id
    ).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate, organization_id: UUID) -> User:
    """Create a new user with hashed password"""
    hashed_pwd = hash_password(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        password_hash=hashed_pwd,
        organization_id=organization_id,
        role=UserRole.PARTICIPANT  # Default role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: UUID, organization_id: UUID, user_update: UserUpdate) -> User | None:
    """Update user details"""
    db_user = get_user_by_id(db, user_id, organization_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def update_password(db: Session, user_id: UUID, organization_id: UUID, new_password: str) -> User | None:
    """Update user password"""
    db_user = get_user_by_id(db, user_id, organization_id)
    if not db_user:
        return None
    
    db_user.password_hash = hash_password(new_password)
    db.commit()
    db.refresh(db_user)
    return db_user

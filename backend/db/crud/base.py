"""
Base CRUD classes with automatic multi-tenant organization scoping
Provides generic CRUD operations with built-in organization filtering
"""
from typing import Generic, TypeVar, Type, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from backend.core.database import Base

# Type variable for SQLAlchemy model
ModelType = TypeVar("ModelType", bound=Base)


class MultiTenantCRUD(Generic[ModelType]):
    """
    Base CRUD class with automatic organization scoping
    
    Provides common database operations that automatically filter
    by organization_id for multi-tenant data isolation.
    
    Usage:
        ```python
        from backend.db.crud.base import MultiTenantCRUD
        from backend.models.session import Session as SessionModel
        
        class SessionCRUD(MultiTenantCRUD[SessionModel]):
            pass
        
        session_crud = SessionCRUD(SessionModel)
        ```
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD with a SQLAlchemy model
        
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
        
        # Verify model has organization_id column for multi-tenancy
        mapper = inspect(model)
        if not hasattr(mapper.columns, 'organization_id'):
            raise ValueError(
                f"Model {model.__name__} must have 'organization_id' column for multi-tenant CRUD"
            )
    
    def get_by_id(
        self,
        db: Session,
        id: UUID,
        organization_id: UUID
    ) -> ModelType | None:
        """
        Get a single record by ID with organization filtering
        
        Args:
            db: Database session
            id: Record primary key
            organization_id: Organization UUID for filtering
            
        Returns:
            Model instance or None if not found
        """
        return db.query(self.model).filter(
            self.model.id == id,
            self.model.organization_id == organization_id
        ).first()
    
    def get_multi(
        self,
        db: Session,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> list[ModelType]:
        """
        Get multiple records with organization filtering and pagination
        
        Args:
            db: Database session
            organization_id: Organization UUID for filtering
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        return db.query(self.model).filter(
            self.model.organization_id == organization_id
        ).offset(skip).limit(limit).all()
    
    def create(
        self,
        db: Session,
        obj_in: dict[str, Any],
        organization_id: UUID
    ) -> ModelType:
        """
        Create a new record with automatic organization assignment
        
        Args:
            db: Database session
            obj_in: Dictionary of field values
            organization_id: Organization UUID to assign
            
        Returns:
            Created model instance
            
        Note:
            Automatically sets organization_id to prevent cross-tenant writes
        """
        # Ensure organization_id is set (prevent accidental cross-tenant writes)
        obj_in["organization_id"] = organization_id
        
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self,
        db: Session,
        id: UUID,
        organization_id: UUID,
        obj_in: dict[str, Any]
    ) -> ModelType | None:
        """
        Update a record with organization filtering
        
        Args:
            db: Database session
            id: Record primary key
            organization_id: Organization UUID for filtering
            obj_in: Dictionary of fields to update
            
        Returns:
            Updated model instance or None if not found
            
        Note:
            Cannot change organization_id to prevent moving records between tenants
        """
        # Prevent changing organization_id
        if "organization_id" in obj_in:
            del obj_in["organization_id"]
        
        db_obj = self.get_by_id(db, id, organization_id)
        if not db_obj:
            return None
        
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(
        self,
        db: Session,
        id: UUID,
        organization_id: UUID
    ) -> bool:
        """
        Delete a record with organization filtering
        
        Args:
            db: Database session
            id: Record primary key
            organization_id: Organization UUID for filtering
            
        Returns:
            True if deleted, False if not found
        """
        db_obj = self.get_by_id(db, id, organization_id)
        if not db_obj:
            return False
        
        db.delete(db_obj)
        db.commit()
        return True
    
    def count(
        self,
        db: Session,
        organization_id: UUID
    ) -> int:
        """
        Count records for an organization
        
        Args:
            db: Database session
            organization_id: Organization UUID for filtering
            
        Returns:
            Number of records
        """
        return db.query(self.model).filter(
            self.model.organization_id == organization_id
        ).count()

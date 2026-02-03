"""
Multi-tenancy middleware and dependencies
Provides automatic organization scoping for security and data isolation
"""
from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.security import decode_token
from backend.db.crud import user_crud, organization_crud
from backend.models.user import User
from backend.models.organization import Organization

# OAuth2 scheme for JWT tokens
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Extract and validate user from JWT token
    
    Args:
        credentials: Bearer token from Authorization header
        db: Database session
        
    Returns:
        Authenticated user object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    # Decode JWT token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "Could not validate credentials"
                }
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract user ID from token
    user_id_str: str | None = payload.get("sub")
    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "Token missing user ID"
                }
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "Invalid user ID format"
                }
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get organization ID from token
    org_id_str: str | None = payload.get("org_id")
    if not org_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "Token missing organization ID"
                }
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        org_id = UUID(org_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "Invalid organization ID format"
                }
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Fetch user from database with organization filtering
    user = user_crud.get_user_by_id(db, user_id, org_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "USER_NOT_FOUND",
                    "message": "User not found or access denied"
                }
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_organization(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Organization:
    """
    Get the organization of the current authenticated user
    
    Args:
        current_user: Authenticated user from get_current_user dependency
        db: Database session
        
    Returns:
        Organization object
        
    Raises:
        HTTPException: If organization not found
    """
    org = organization_crud.get_organization_by_id(db, current_user.organization_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "ORG_NOT_FOUND",
                    "message": "Organization not found"
                }
            }
        )
    
    return org


def require_organization_access(
    current_user: User = Depends(get_current_user),
) -> UUID:
    """
    Extract organization ID from current user for multi-tenant filtering
    
    This dependency should be used in endpoints that need to filter
    queries by organization_id for security and data isolation.
    
    Args:
        current_user: Authenticated user from get_current_user dependency
        
    Returns:
        Organization UUID for filtering queries
        
    Example:
        ```python
        @router.get("/users")
        async def list_users(
            org_id: UUID = Depends(require_organization_access),
            db: Session = Depends(get_db)
        ):
            users = user_crud.get_users(db, org_id)
            return users
        ```
    """
    return current_user.organization_id


# Type aliases for cleaner endpoint signatures
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentOrganization = Annotated[Organization, Depends(get_current_organization)]
OrganizationId = Annotated[UUID, Depends(require_organization_access)]

"""
Authentication API endpoints
Handles user registration, login, token refresh, and logout
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from backend.schemas.user import UserCreate, UserWithOrganization
from backend.schemas.auth import LoginRequest, TokenResponse
from backend.db.crud import user_crud, organization_crud
from backend.models.user import UserRole

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


@router.post("/register", response_model=UserWithOrganization, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    
    - Validates organization exists
    - Checks email uniqueness
    - Validates password strength (≥8 characters)
    - Hashes password with bcrypt
    - Creates user with default 'participant' role
    """
    # Validate organization exists
    org = organization_crud.get_organization_by_slug(db, user_data.organization_slug)
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
    
    # Check if email already exists
    existing_user = user_crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": "EMAIL_ALREADY_EXISTS",
                    "message": "Email already registered"
                }
            }
        )
    
    # Password strength is validated by Pydantic schema (min_length=8)
    # Create user
    db_user = user_crud.create_user(db, user_data, org.id)
    
    # Return user with organization data
    return db_user


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Login user with email and password
    
    - Returns JWT access token (15 min expiration)
    - Sets httpOnly refresh token cookie (7 day expiration)
    - Returns 401 for invalid credentials (same message to prevent enumeration)
    """
    # Get user by email
    user = user_crud.get_user_by_email(db, credentials.email)
    
    # Verify user exists and password is correct
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid email or password"
                }
            }
        )
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "org_id": str(user.organization_id),
            "roles": [user.role.value]
        }
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    # Set refresh token in httpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax",
        max_age=7 * 24 * 60 * 60  # 7 days in seconds
    )
    
    # Return access token
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",  # noqa: S106, B106 - OAuth2 token type, not a password
        expires_in=15 * 60  # 15 minutes in seconds
    )


@router.post("/logout")
async def logout(response: Response):
    """
    Logout user by clearing refresh token cookie
    """
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully"}

# Multi-Tenancy Architecture Guide

## Overview

The trivia-app implements **row-level multi-tenancy** with automatic organization scoping to ensure complete data isolation between tenants. This guide explains how to use the multi-tenancy middleware and base CRUD classes.

## Security Model

### Key Principles

1. **JWT-Based Organization Context**: Every authenticated request carries an `org_id` claim in the JWT token
2. **Automatic Filtering**: All database queries are automatically filtered by `organization_id`
3. **Defense in Depth**: Multiple layers prevent cross-tenant data access:
   - JWT validation
   - User-organization verification
   - CRUD-level filtering
   - Database-level foreign keys

### Threat Model Protection

This implementation protects against:
- ❌ **Cross-tenant data access**: Users cannot query other organizations' data
- ❌ **Token tampering**: Modified `org_id` in JWT will fail authentication
- ❌ **Accidental data leakage**: Developers cannot forget to filter by organization
- ❌ **Privilege escalation**: Organization boundaries cannot be crossed

## Architecture Components

### 1. Multi-Tenancy Middleware (`backend/core/multi_tenancy.py`)

#### Dependencies

##### `get_current_user`
Extracts and validates the user from JWT token.

```python
from backend.core.multi_tenancy import get_current_user, CurrentUser

@router.get("/profile")
async def get_profile(current_user: CurrentUser):
    """Get current user profile"""
    return current_user
```

**Validation Steps**:
1. Extract JWT from `Authorization: Bearer <token>` header
2. Decode and validate JWT signature
3. Extract `sub` (user_id) and `org_id` claims
4. Verify user exists in database with matching organization
5. Return authenticated `User` object

**Error Responses**:
- `401 INVALID_TOKEN`: Invalid or expired JWT
- `401 USER_NOT_FOUND`: User doesn't exist or wrong organization

##### `get_current_organization`
Returns the organization of the authenticated user.

```python
from backend.core.multi_tenancy import CurrentOrganization

@router.get("/organization")
async def get_my_organization(org: CurrentOrganization):
    """Get current user's organization details"""
    return org
```

##### `require_organization_access`
Extracts organization ID for query filtering.

```python
from backend.core.multi_tenancy import OrganizationId
from backend.db.crud import user_crud

@router.get("/users")
async def list_users(
    org_id: OrganizationId,
    db: Session = Depends(get_db)
):
    """List users in current organization"""
    users = user_crud.get_users(db, org_id)
    return users
```

#### Type Aliases

For cleaner endpoint signatures, use these annotated types:

```python
from backend.core.multi_tenancy import CurrentUser, CurrentOrganization, OrganizationId

# Instead of:
async def endpoint(current_user: User = Depends(get_current_user)):
    pass

# Use:
async def endpoint(current_user: CurrentUser):
    pass
```

### 2. Base CRUD Class (`backend/db/crud/base.py`)

#### `MultiTenantCRUD` Generic Class

Provides automatic organization scoping for all database operations.

##### Features

✅ **Automatic Organization Filtering**: All queries include `organization_id` filter  
✅ **Create Safety**: Prevents cross-tenant writes by enforcing `organization_id`  
✅ **Update Protection**: Prevents moving records between organizations  
✅ **Delete Isolation**: Only deletes records in the correct organization  
✅ **Model Validation**: Ensures model has `organization_id` column at initialization

##### Usage

```python
from backend.db.crud.base import MultiTenantCRUD
from backend.models.session import Session

# Create CRUD instance
session_crud = MultiTenantCRUD(Session)

# Use in endpoints
@router.post("/sessions")
async def create_session(
    session_data: SessionCreate,
    org_id: OrganizationId,
    db: Session = Depends(get_db)
):
    """Create new trivia session"""
    session = session_crud.create(
        db,
        obj_in=session_data.model_dump(),
        organization_id=org_id
    )
    return session

@router.get("/sessions")
async def list_sessions(
    org_id: OrganizationId,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List sessions for organization"""
    sessions = session_crud.get_multi(db, org_id, skip, limit)
    return sessions

@router.get("/sessions/{session_id}")
async def get_session(
    session_id: UUID,
    org_id: OrganizationId,
    db: Session = Depends(get_db)
):
    """Get session by ID (only if in user's organization)"""
    session = session_crud.get_by_id(db, session_id, org_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
```

#### Methods

##### `create(db, obj_in, organization_id)`
Creates a new record with automatic organization assignment.

```python
session = session_crud.create(
    db,
    obj_in={"name": "Weekly Trivia", "max_participants": 50},
    organization_id=org_id
)
```

**Security**: Automatically sets `organization_id`, ignoring any value in `obj_in`

##### `get_by_id(db, id, organization_id)`
Retrieves a record by ID, scoped to organization.

```python
session = session_crud.get_by_id(db, session_id, org_id)
# Returns None if session doesn't exist or belongs to another org
```

##### `get_multi(db, organization_id, skip=0, limit=100)`
Retrieves multiple records with pagination.

```python
sessions = session_crud.get_multi(db, org_id, skip=0, limit=20)
```

##### `update(db, id, organization_id, obj_in)`
Updates a record, scoped to organization.

```python
updated = session_crud.update(
    db,
    session_id,
    org_id,
    {"name": "Updated Trivia"}
)
```

**Security**: Prevents changing `organization_id` to move records between tenants

##### `delete(db, id, organization_id)`
Deletes a record, scoped to organization.

```python
success = session_crud.delete(db, session_id, org_id)
# Returns False if not found in organization
```

##### `count(db, organization_id)`
Counts records for an organization.

```python
total = session_crud.count(db, org_id)
```

## Implementation Examples

### Example 1: Simple CRUD Endpoint

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from backend.core.database import get_db
from backend.core.multi_tenancy import OrganizationId
from backend.db.crud.base import MultiTenantCRUD
from backend.models.question import Question
from backend.schemas.question import QuestionCreate, QuestionOut

router = APIRouter(prefix="/questions", tags=["questions"])

# Initialize CRUD
question_crud = MultiTenantCRUD(Question)

@router.post("", response_model=QuestionOut)
async def create_question(
    question: QuestionCreate,
    org_id: OrganizationId,
    db: Session = Depends(get_db)
):
    """Create a new trivia question"""
    return question_crud.create(db, question.model_dump(), org_id)

@router.get("", response_model=list[QuestionOut])
async def list_questions(
    org_id: OrganizationId,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List all questions for organization"""
    return question_crud.get_multi(db, org_id, skip, limit)

@router.get("/{question_id}", response_model=QuestionOut)
async def get_question(
    question_id: UUID,
    org_id: OrganizationId,
    db: Session = Depends(get_db)
):
    """Get question by ID"""
    question = question_crud.get_by_id(db, question_id, org_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
```

### Example 2: Custom CRUD with Extended Methods

```python
from backend.db.crud.base import MultiTenantCRUD
from backend.models.session import Session
from sqlalchemy.orm import Session as DBSession

class SessionCRUD(MultiTenantCRUD[Session]):
    """Extended CRUD for Session with custom methods"""
    
    def get_active_sessions(
        self,
        db: DBSession,
        organization_id: UUID
    ) -> list[Session]:
        """Get only active sessions for organization"""
        return db.query(self.model).filter(
            self.model.organization_id == organization_id,
            self.model.status == "active"
        ).all()
    
    def get_by_code(
        self,
        db: DBSession,
        code: str,
        organization_id: UUID
    ) -> Session | None:
        """Get session by join code"""
        return db.query(self.model).filter(
            self.model.organization_id == organization_id,
            self.model.code == code
        ).first()

# Use in endpoints
session_crud = SessionCRUD(Session)
```

### Example 3: Endpoint with User Context

```python
from backend.core.multi_tenancy import CurrentUser, OrganizationId

@router.post("/sessions/{session_id}/join")
async def join_session(
    session_id: UUID,
    current_user: CurrentUser,  # Full user object
    org_id: OrganizationId,      # Just the org ID
    db: Session = Depends(get_db)
):
    """Join a trivia session"""
    # Get session (automatically scoped to org)
    session = session_crud.get_by_id(db, session_id, org_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Add current user as participant
    add_participant(db, session, current_user)
    return {"message": "Joined successfully"}
```

## Database Model Requirements

All models that need multi-tenant isolation must include:

```python
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

class YourModel(Base):
    __tablename__ = "your_table"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # REQUIRED: Organization foreign key with index
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id"),
        nullable=False,
        index=True  # Performance: Always index organization_id
    )
    
    # ... other fields
```

## Testing Multi-Tenancy

### Unit Tests

```python
def test_get_by_id_with_wrong_org_returns_none(
    db: Session,
    sample_organization: Organization,
    premium_organization: Organization
):
    """Test that queries fail across organization boundaries"""
    # Create record in org A
    obj = crud.create(db, {"name": "Test"}, sample_organization.id)
    
    # Try to get from org B
    result = crud.get_by_id(db, obj.id, premium_organization.id)
    
    # Should return None (not accessible)
    assert result is None
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_tampered_token_fails(
    client: TestClient,
    sample_user: User,
    premium_organization: Organization
):
    """Test that tampering with org_id in token fails"""
    # Create token with wrong org_id
    token = create_access_token(
        data={
            "sub": str(sample_user.id),
            "org_id": str(premium_organization.id),  # Wrong org!
            "roles": [sample_user.role.value]
        }
    )
    
    # Request should fail authentication
    response = client.get(
        "/api/v1/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 401
```

## Security Best Practices

### ✅ DO

1. **Always use dependencies**: Never manually extract organization from JWT
   ```python
   # ✅ Good
   async def endpoint(org_id: OrganizationId):
       pass
   ```

2. **Use MultiTenantCRUD for scoped models**: Ensures automatic filtering
   ```python
   # ✅ Good
   crud = MultiTenantCRUD(Question)
   questions = crud.get_multi(db, org_id)
   ```

3. **Verify organization access**: Double-check sensitive operations
   ```python
   # ✅ Good
   session = session_crud.get_by_id(db, session_id, org_id)
   if not session:
       raise HTTPException(status_code=404)
   ```

4. **Test tenant isolation**: Write tests that verify cross-tenant access fails
   ```python
   # ✅ Good - Test should fail access
   result = crud.get_by_id(db, obj_id, other_org_id)
   assert result is None
   ```

### ❌ DON'T

1. **Don't bypass organization filtering**: Never query without organization check
   ```python
   # ❌ Bad - Bypasses multi-tenancy
   db.query(Question).filter(Question.id == id).first()
   
   # ✅ Good
   question_crud.get_by_id(db, id, org_id)
   ```

2. **Don't trust client-provided org_id**: Always use JWT-extracted organization
   ```python
   # ❌ Bad - Client can send any org_id
   @router.get("/users")
   async def list_users(org_id: UUID, db: Session = Depends(get_db)):
       pass
   
   # ✅ Good - Org ID from authenticated token
   async def list_users(org_id: OrganizationId, db: Session = Depends(get_db)):
       pass
   ```

3. **Don't allow organization_id in updates**: Prevents moving records
   ```python
   # ❌ Bad - Allows changing organization
   crud.update(db, id, org_id, {"organization_id": other_org_id})
   
   # ✅ Good - MultiTenantCRUD automatically strips organization_id
   ```

## Common Patterns

### Pattern 1: Nested Resource Access

```python
@router.get("/sessions/{session_id}/questions")
async def get_session_questions(
    session_id: UUID,
    org_id: OrganizationId,
    db: Session = Depends(get_db)
):
    """Get questions for a session"""
    # 1. Verify session exists and is in user's org
    session = session_crud.get_by_id(db, session_id, org_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # 2. Get questions (also filtered by org through session)
    questions = question_crud.get_multi(db, org_id)
    return questions
```

### Pattern 2: Admin-Only Operations

```python
from backend.models.user import UserRole

def require_admin(current_user: CurrentUser) -> User:
    """Dependency that requires admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: UUID,
    current_user: User = Depends(require_admin),
    org_id: OrganizationId,
    db: Session = Depends(get_db)
):
    """Delete session (admin only)"""
    success = session_crud.delete(db, session_id, org_id)
    if not success:
        raise HTTPException(status_code=404)
    return {"message": "Session deleted"}
```

## Migration Guide

### Existing Endpoints

To add multi-tenancy to existing endpoints:

1. **Add organization dependency**:
   ```python
   # Before
   async def endpoint(db: Session = Depends(get_db)):
       pass
   
   # After
   async def endpoint(
       org_id: OrganizationId,
       db: Session = Depends(get_db)
   ):
       pass
   ```

2. **Replace manual queries with CRUD**:
   ```python
   # Before
   items = db.query(Item).all()
   
   # After
   items = item_crud.get_multi(db, org_id)
   ```

3. **Add organization to creates**:
   ```python
   # Before
   item = Item(**data)
   db.add(item)
   
   # After
   item = item_crud.create(db, data, org_id)
   ```

## Troubleshooting

### Issue: `ValueError: Model must have 'organization_id' column`

**Cause**: Trying to use `MultiTenantCRUD` with a model that doesn't have `organization_id`

**Solution**: Add `organization_id` column to the model:
```python
organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False, index=True)
```

### Issue: `401 INVALID_TOKEN`

**Causes**:
- Expired JWT token
- Invalid JWT signature
- Missing `sub` or `org_id` claim
- Corrupted token

**Solution**: Generate a new token via `/api/v1/auth/login`

### Issue: `401 USER_NOT_FOUND`

**Causes**:
- User doesn't exist in database
- `org_id` in token doesn't match user's organization
- User was deleted

**Solution**: Verify user exists and token has correct `org_id`

### Issue: `404` when resource should exist

**Cause**: Resource exists but in a different organization

**Solution**: This is correct behavior - resources from other organizations should not be accessible

## Performance Considerations

### Index Requirements

Always index `organization_id` for performance:

```python
organization_id = Column(
    UUID(as_uuid=True),
    ForeignKey("organizations.id"),
    nullable=False,
    index=True  # REQUIRED for query performance
)
```

### Query Optimization

For complex queries, add composite indexes:

```sql
-- Example: Frequently query by org + status
CREATE INDEX idx_sessions_org_status 
ON sessions (organization_id, status);

-- Example: Frequently query by org + created_at
CREATE INDEX idx_questions_org_created 
ON questions (organization_id, created_at);
```

## Compliance & Auditing

### GDPR Data Isolation

Multi-tenancy ensures:
- ✅ Data is isolated per organization
- ✅ No cross-organization data access
- ✅ Easy to export/delete organization data

### SOC 2 Controls

Implemented controls:
- ✅ **Access Control**: JWT-based authentication with organization context
- ✅ **Data Segregation**: Automatic organization filtering
- ✅ **Audit Trail**: All queries include organization_id for logging

### Audit Logging

Example audit log pattern:

```python
import logging

logger = logging.getLogger(__name__)

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: UUID,
    current_user: CurrentUser,
    org_id: OrganizationId,
    db: Session = Depends(get_db)
):
    """Delete session with audit logging"""
    session = session_crud.get_by_id(db, session_id, org_id)
    if not session:
        raise HTTPException(status_code=404)
    
    # Audit log
    logger.info(
        "Session deleted",
        extra={
            "user_id": str(current_user.id),
            "org_id": str(org_id),
            "session_id": str(session_id),
            "action": "delete_session"
        }
    )
    
    session_crud.delete(db, session_id, org_id)
    return {"message": "Session deleted"}
```

## Summary

The multi-tenancy architecture provides:

✅ **Security**: Automatic organization scoping prevents data leakage  
✅ **Developer Experience**: Simple dependencies and base classes  
✅ **Type Safety**: Type-annotated dependencies catch errors at development time  
✅ **Performance**: Indexed queries ensure fast filtering  
✅ **Compliance**: GDPR and SOC 2 controls built-in  
✅ **Testing**: Comprehensive test coverage validates isolation

For questions or issues, see the test files:
- `tests/core/test_multi_tenancy.py` - Middleware tests
- `tests/crud/test_base.py` - CRUD tests

"""
CRUD operations for Organization model
"""
from sqlalchemy.orm import Session
from uuid import UUID
from backend.models.organization import Organization
from backend.schemas.organization import OrganizationCreate


def get_organization_by_id(db: Session, organization_id: UUID) -> Organization | None:
    """Get organization by ID"""
    return db.query(Organization).filter(Organization.id == organization_id).first()


def get_organization_by_slug(db: Session, slug: str) -> Organization | None:
    """Get organization by slug"""
    return db.query(Organization).filter(Organization.slug == slug).first()


def create_organization(db: Session, org: OrganizationCreate) -> Organization:
    """Create a new organization"""
    db_org = Organization(
        name=org.name,
        slug=org.slug,
        plan=org.plan
    )
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


def get_organizations(db: Session, skip: int = 0, limit: int = 100) -> list[Organization]:
    """Get list of organizations"""
    return db.query(Organization).offset(skip).limit(limit).all()

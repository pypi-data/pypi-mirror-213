from enum import Enum
from pydantic import BaseModel

from getajob.vendor.clerk.companies.models import ClerkCompanyCreated
from getajob.vendor.clerk.models import (
    ClerkBaseModel,
    ClerkWebhookEvent,
    ClerkCompanyMemberType,
)


class ClerkCompanyMembershipWebhookType(str, Enum):
    organization_membership_created = "organizationMembership.created"
    organization_membership_deleted = "organizationMembership.deleted"
    organization_membership_updated = "organizationMembership.updated"


class ClerkCompanyMembershipWebhookEvent(ClerkWebhookEvent):
    type: ClerkCompanyMembershipWebhookType


class CreateClerkCompanyMember(BaseModel):
    first_name: str
    identifier: str
    image_url: str | None = None
    last_name: str
    profile_image_url: str | None = None
    user_id: str


class ClerkCompanyMember(CreateClerkCompanyMember):
    id: str
    role: ClerkCompanyMemberType


class UpdateClerkCompanyMember(BaseModel):
    first_name: str | None = None
    identifier: str | None = None
    image_url: str | None = None
    last_name: str | None = None
    profile_image_url: str | None = None
    user_id: str | None = None


class UpdateClerkCompanyMemberWithRole(UpdateClerkCompanyMember):
    role: ClerkCompanyMemberType | None = None


class ClerkCompanyMembership(ClerkBaseModel):
    created_at: int
    organization: ClerkCompanyCreated
    public_user_data: CreateClerkCompanyMember
    role: ClerkCompanyMemberType
    updated_at: int


class DeleteClerkCompanyMember(BaseModel):
    id: str


class ClerkUpdateCompanyMembership(ClerkBaseModel):
    created_at: int
    organization: ClerkCompanyCreated
    public_user_data: UpdateClerkCompanyMember
    role: ClerkCompanyMemberType
    updated_at: int

import typing as t
from datetime import datetime
import requests
from pydantic import BaseModel
from enum import Enum

from getajob.config.settings import SETTINGS


class ClerkRole(str, Enum):
    ADMIN = "admin"
    MEMBER = "basic_member"


class OrganizationInvitationRequest(BaseModel):
    email_address: str
    invited_user_id: str
    role: ClerkRole


class BulkOrganizationInviteRequest(BaseModel):
    invitations: t.List[OrganizationInvitationRequest]


class OrganizationMember(BaseModel):
    id: str
    email_address: str
    role: ClerkRole
    organization_id: str
    status: str
    created_at: datetime
    updated_at: datetime


class BulkOrganizationMemberResponse(BaseModel):
    data: t.List[OrganizationMember]
    total_count: int


class Invitation(BaseModel):
    id: str
    email_address: str
    revoked: bool
    status: str
    created_at: datetime
    updated_at: datetime


class CreateOrganizationRequest(BaseModel):
    name: str
    created_by: str  # user_id
    slug: str


class ClerkOrganization(BaseModel):
    id: str
    name: str
    slug: str
    members_count: int
    max_allowed_memberships: int
    public_metadata: dict
    private_metadata: dict
    created_by: str
    created_at: datetime
    updated_at: datetime


class ClerkAPI:
    headers = {
        "Authorization": "Bearer " + SETTINGS.CLERK_SECRET_KEY,
    }

    def create_organization(self, data: CreateOrganizationRequest):
        resp = requests.post(
            f"{SETTINGS.CLERK_API_BASE_URL}/organizations",
            json=data.dict(),
            headers=self.headers,
        )
        resp.raise_for_status()
        return ClerkOrganization(**resp.json())

    def get_organization_by_id_or_slug(self, id_or_slug: str):
        resp = requests.get(
            f"{SETTINGS.CLERK_API_BASE_URL}/organizations/{id_or_slug}",
            headers=self.headers,
        )
        resp.raise_for_status()
        return ClerkOrganization(**resp.json())

    def delete_organization_by_id(self, id: str):
        resp = requests.delete(
            f"{SETTINGS.CLERK_API_BASE_URL}/organizations/{id}",
            headers=self.headers,
        )
        resp.raise_for_status()
        return resp.json()["deleted"]

    def send_user_invitation(self, email: str):
        resp = requests.post(
            f"{SETTINGS.CLERK_API_BASE_URL}/invitations",
            json={"email_address": email},
            headers=self.headers,
        )
        resp.raise_for_status()
        return Invitation(**resp.json())

    def send_organization_invitation(
        self, organization_id: str, data: OrganizationInvitationRequest
    ):
        resp = requests.post(
            f"{SETTINGS.CLERK_API_BASE_URL}/organizations/{organization_id}/invitations",
            json=data.dict(),
            headers=self.headers,
        )
        resp.raise_for_status()
        return OrganizationMember(**resp.json())

    def bulk_send_organization_invitations(
        self, organization_id: str, data: BulkOrganizationInviteRequest
    ):
        resp = requests.post(
            f"{SETTINGS.CLERK_API_BASE_URL}/organizations/{organization_id}/invitations/bulk",
            json=data.dict()["invitations"],
            headers=self.headers,
        )
        resp.raise_for_status()
        return BulkOrganizationMemberResponse(**resp.json())

    def revoke_organization_invitation(self, organization_id: str, invitation_id: str):
        resp = requests.post(
            f"{SETTINGS.CLERK_API_BASE_URL}/organizations/{organization_id}/invitations/{invitation_id}/revoke",
            headers=self.headers,
        )
        resp.raise_for_status()
        return OrganizationMember(**resp.json())

    def update_organization_membership(
        self, organization_id: str, user_id: str, new_role: ClerkRole
    ) -> ClerkRole:
        resp = requests.patch(
            f"{SETTINGS.CLERK_API_BASE_URL}/organizations/{organization_id}/memberships/{user_id}",
            json={"role": new_role},
            headers=self.headers,
        )
        resp.raise_for_status()
        return ClerkRole(resp.json()["role"])

    def remove_user_from_organization(self, organization_id: str, user_id: str):
        resp = requests.delete(
            f"{SETTINGS.CLERK_API_BASE_URL}/organizations/{organization_id}/memberships/{user_id}",
            headers=self.headers,
        )
        resp.raise_for_status()
        return resp.json()

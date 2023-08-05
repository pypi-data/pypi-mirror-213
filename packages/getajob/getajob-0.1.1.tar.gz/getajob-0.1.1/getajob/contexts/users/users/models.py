import typing as t
from enum import Enum
from pydantic import BaseModel

from getajob.abstractions.models import EntityModels
from getajob.contexts.users.clerk_webhook.models import ClerkWebhookUserCreated


class User(ClerkWebhookUserCreated):
    company_admin: t.Optional[bool]
    company_id: t.Optional[str]


class UpdateUser(BaseModel):
    company_admin: t.Optional[bool]
    company_id: t.Optional[str]


entity_models = EntityModels(entity=User, update=UpdateUser)


class UserRegistrationStatus(str, Enum):
    REGISTERED = "registered"
    INVITED = "invited"
    CANCELLED = "cancelled"
    REMOVED = "removed"
    BLOCKED = "blocked"


class UserRecruiter(BaseModel):
    user_id: str
    is_admin: bool = False

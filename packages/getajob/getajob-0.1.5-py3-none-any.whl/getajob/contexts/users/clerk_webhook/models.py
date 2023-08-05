import typing as t

from pydantic import BaseModel

from getajob.abstractions.models import EntityModels


class ClerkWebhookEvent(BaseModel):
    data: dict
    object: str
    type: t.Literal["user.created", "user.updated", "user.deleted"]


class ClerkUserEmailAddresses(BaseModel):
    email_address: str
    id: str
    linked_to: list
    object: str
    verification: dict


class ClertkUserPhoneNumbers(BaseModel):
    id: str
    linked_to: list
    object: str
    phone_number: str
    verification: dict


class ClerkWekhooks(BaseModel):
    id: str
    object: str


class ClerkWebhookUserCreated(ClerkWekhooks):
    created_at: int
    primary_email_address: str
    primary_email_address_id: str
    email_addresses: list[ClerkUserEmailAddresses]
    phone_numbers: list[ClertkUserPhoneNumbers]
    first_name: str
    last_name: str
    gender: str
    external_id: t.Optional[str]
    birthday: str


class ClerkWebhookUserUpdated(ClerkWebhookUserCreated):
    updated_at: int


class ClerkWebhookUserDeleted(ClerkWekhooks):
    deleted: bool


entity_models = EntityModels(entity=ClerkWebhookUserCreated)

from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity

from .models import (
    ClerkWebhookUserCreated,
    ClerkWebhookEvent,
    entity_models,
)


class WebhookUserRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.USERS.value, entity_models)

    def handle_webhook_event(self, event: ClerkWebhookEvent):
        event_dict = {"user.created": self.create_user}
        if event.type not in event_dict:
            raise Exception("Invalid event type")
        return event_dict[event.type](event)

    def create_user(self, event: ClerkWebhookEvent):
        create_event = ClerkWebhookUserCreated(**event.data)
        return self.create(data=create_event, provided_id=create_event.id)

import typing as t

from getajob.vendor.firebase import FirestoreDB
from getajob.vendor.kafka.repository import KafkaRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity, EntityModels

from .models import (
    ClerkCompanyInvitation,
    ClerkCompanyInvitationsWebhookEvent,
    ClerkCompanyInvitationsWebhookType,
)

entity_models = EntityModels(entity=ClerkCompanyInvitation)


class WebhookCompanyInvitationRepository(BaseRepository):
    def __init__(self, db: FirestoreDB, kafka: t.Optional[KafkaRepository] = None):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.recruiters_invitations,
            create=True,
            update=True,
            delete=True,
        )
        super().__init__(
            db,
            Entity.RECRUITER_INVITATIONS.value,
            entity_models,
            kafka,
            kafka_event_config,
        )

    def handle_webhook_event(self, event: ClerkCompanyInvitationsWebhookEvent):
        event_dict = {
            ClerkCompanyInvitationsWebhookType.organization_invitation_created: self.create_invitation,
            ClerkCompanyInvitationsWebhookType.organization_invitation_revoked: self.revoke_invitation,
            ClerkCompanyInvitationsWebhookType.organization_invitation_accepted: self.accept_invitation,
        }
        return event_dict[event.type](event)

    def create_invitation(self, event: ClerkCompanyInvitationsWebhookEvent):
        create_event = ClerkCompanyInvitation(**event.data)
        return self.create(data=create_event, provided_id=create_event.id)

    def revoke_invitation(self, event: ClerkCompanyInvitationsWebhookEvent):
        update_event = ClerkCompanyInvitation(**event.data)
        return self.update(doc_id=update_event.id, data=update_event)

    def accept_invitation(self, event: ClerkCompanyInvitationsWebhookEvent):
        update_event = ClerkCompanyInvitation(**event.data)
        return self.update(doc_id=update_event.id, data=update_event)

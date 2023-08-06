import typing as t

from getajob.vendor.firebase import FirestoreDB
from getajob.vendor.kafka.repository import KafkaRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity, EntityModels

from .models import (
    ClerkCompanyMembershipWebhookEvent,
    ClerkCompanyMembership,
    ClerkCompanyMembershipWebhookType,
    CreateClerkCompanyMember,
    UpdateClerkCompanyMember,
    ClerkUpdateCompanyMembership,
    ClerkCompanyMember,
)

entity_models = EntityModels(entity=ClerkCompanyMember)


class WebhookCompanyMembershipRepository(BaseRepository):
    def __init__(self, db: FirestoreDB, kafka: t.Optional[KafkaRepository] = None):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.recruiters,
            create=True,
            update=True,
            delete=True,
        )
        super().__init__(
            db, Entity.RECRUITERS.value, entity_models, kafka, kafka_event_config
        )

    def handle_webhook_event(self, event: ClerkCompanyMembershipWebhookEvent):
        event_dict = {
            ClerkCompanyMembershipWebhookType.organization_membership_created: self.create_recruiter,
            ClerkCompanyMembershipWebhookType.organization_membership_updated: self.update_recruiter,
            ClerkCompanyMembershipWebhookType.organization_membership_deleted: self.delete_recruiter,
        }
        return event_dict[event.type](event)

    def create_recruiter(self, event: ClerkCompanyMembershipWebhookEvent):
        create_event = ClerkCompanyMembership(**event.data)
        recruiter = CreateClerkCompanyMember(**create_event.public_user_data.dict())
        return self.create(
            data=recruiter,
            provided_id=create_event.id,
            parent_collections={"companies": create_event.organization.id},
        )

    def delete_recruiter(self, event: ClerkCompanyMembershipWebhookEvent):
        delete_event = ClerkUpdateCompanyMembership(**event.data)
        return self.delete(
            doc_id=delete_event.id,
            parent_collections={"companies": delete_event.organization.id},
        )

    def update_recruiter(self, event: ClerkCompanyMembershipWebhookEvent):
        update_event = ClerkUpdateCompanyMembership(**event.data)
        recruiter = UpdateClerkCompanyMember(**update_event.public_user_data.dict())
        return self.update(
            doc_id=update_event.id,
            data=recruiter,
            parent_collections={"companies": update_event.organization.id},
        )

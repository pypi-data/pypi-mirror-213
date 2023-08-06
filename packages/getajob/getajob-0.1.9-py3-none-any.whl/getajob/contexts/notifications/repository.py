from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity

from .models import entity_models


class NotificationRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.USER_NOTIFICATIONS.value, entity_models)

    def get_applicant_notifications(self, company_id: str):
        return self.query(
            parent_collections={
                "companies": company_id,
            }
        )

from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.models.entities import Entity

from .models import entity_models


class AdminUserRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.ADMIN_USERS.value, entity_models)

    def get_by_user_id(self, user_id: str):
        return self.get_one_by_attribute("user_id", user_id)

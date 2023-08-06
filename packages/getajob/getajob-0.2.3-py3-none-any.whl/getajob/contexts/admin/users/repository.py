from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity, EntityModels

from .models import AdminUser, CreateAdminUser, UpdateAdminUser


entity_models = EntityModels(
    entity=AdminUser, create=CreateAdminUser, update=UpdateAdminUser
)


class AdminUserRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.ADMIN_USERS.value, entity_models)

    def get_by_user_id(self, user_id: str):
        return self.get_one_by_attribute("user_id", user_id)

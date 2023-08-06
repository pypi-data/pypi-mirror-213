from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity

from .models import entity_models


class RecruiterRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.RECRUITERS.value, entity_models)

    def get_by_user_id(self, user_id: str):
        return self.get_one_by_attribute("user_id", user_id)

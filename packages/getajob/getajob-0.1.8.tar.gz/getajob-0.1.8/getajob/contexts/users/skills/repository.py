from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.models.entities import Entity

from .models import entity_models


class UserSkillsRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.SKILLS.value, entity_models)

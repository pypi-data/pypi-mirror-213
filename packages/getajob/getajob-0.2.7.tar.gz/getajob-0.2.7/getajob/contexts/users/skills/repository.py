from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity, EntityModels

from .models import CreateSkillSet, UpdateSkillSet, UserSkillsSet

entity_models = EntityModels(
    create=CreateSkillSet, update=UpdateSkillSet, entity=UserSkillsSet
)


class UserSkillsRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.SKILLS.value, entity_models)

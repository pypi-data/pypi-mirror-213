from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity, EntityModels

from .models import Recruiter

entity_models = EntityModels(entity=Recruiter)


class RecruiterRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.RECRUITERS.value, entity_models)

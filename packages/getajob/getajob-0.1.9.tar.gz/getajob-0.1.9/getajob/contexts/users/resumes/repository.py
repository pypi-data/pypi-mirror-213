from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity

from .models import entity_models


class ResumeRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.RESUMES.value, entity_models)

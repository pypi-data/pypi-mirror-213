from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity, EntityModels

from .models import Resume, CreateResume


entity_models = EntityModels(
    entity=Resume,
    create=CreateResume,
    update=CreateResume,
)


class ResumeRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.RESUMES.value, entity_models)

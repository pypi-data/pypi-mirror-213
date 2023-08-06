from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity, EntityModels

from .models import CoverLetter, CreateCoverLetter, UpdateCoverLetter

entity_models = EntityModels(
    entity=CoverLetter,
    create=CreateCoverLetter,
    update=UpdateCoverLetter,
)


class CoverLetterRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.COVER_LETTERS.value, entity_models)

from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity, EntityModels

from .models import Company

entity_models = EntityModels(entity=Company)


class CompanyRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.COMPANIES.value, entity_models)

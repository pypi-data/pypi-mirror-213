from getajob.vendor.firebase import FirestoreDB
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity, EntityModels

from .models import RecruiterInvitation

entity_models = EntityModels(entity=RecruiterInvitation)


class RecruiterInvitationsRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.RECRUITER_INVITATIONS.value, entity_models)

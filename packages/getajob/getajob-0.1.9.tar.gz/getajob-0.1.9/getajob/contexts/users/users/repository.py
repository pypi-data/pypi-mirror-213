import typing as t

from getajob.vendor.firebase import FirestoreDB
from getajob.exceptions import NoCompanyFoundException
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity
from .models import entity_models, User


class UserRepository(BaseRepository):
    def __init__(
        self,
        db: FirestoreDB,
    ):
        super().__init__(db, Entity.USERS.value, entity_models)

    def get_user(self, id: str):
        return super().get(id)

    def get_user_company_id(self, id: str):
        user = self.get_user(id)
        user = t.cast(User, user)
        if not user.company_id:
            raise NoCompanyFoundException
        return user.company_id

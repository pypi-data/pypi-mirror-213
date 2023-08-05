from enum import Enum
from pydantic import BaseModel

from getajob.abstractions.models import EntityModels, BaseDataModel


class RecruiterRole(str, Enum):
    SUPER_ADMIN = "Super Admin"
    ADMIN = "Admin"
    READ_ONLY = "Read Only"

    def get_precedence(self):
        precent_chart = {
            RecruiterRole.SUPER_ADMIN: 300,
            RecruiterRole.ADMIN: 200,
            RecruiterRole.READ_ONLY: 100,
        }
        return precent_chart[self]


class CreateRecruiter(BaseModel):
    user_id: str
    role: RecruiterRole


class UpdateRecruiter(BaseModel):
    role: RecruiterRole


class Recruiter(BaseDataModel, CreateRecruiter):
    ...


entity_models = EntityModels(
    entity=Recruiter, create=CreateRecruiter, update=UpdateRecruiter
)

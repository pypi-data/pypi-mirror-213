from enum import Enum
from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class AdminRole(str, Enum):
    SUPER_ADMIN = "Super Admin"
    ADMIN = "Admin"
    READ_ONLY = "Read Only"

    def get_precedence(self):
        precent_chart = {
            AdminRole.SUPER_ADMIN: 300,
            AdminRole.ADMIN: 200,
            AdminRole.READ_ONLY: 100,
        }
        return precent_chart[self]


class CreateAdminUser(BaseModel):
    user_id: str
    role: AdminRole


class UpdateAdminUser(BaseModel):
    role: AdminRole


class AdminUser(BaseDataModel, CreateAdminUser):
    ...

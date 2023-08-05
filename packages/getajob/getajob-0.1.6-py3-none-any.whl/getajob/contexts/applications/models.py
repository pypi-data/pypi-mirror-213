import typing as t
from enum import Enum

from pydantic import BaseModel

from getajob.abstractions.models import EntityModels, BaseDataModel


class CompanyApplicationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class UserApplicationStatus(str, Enum):
    submitted = "submitted"
    withdrawn = "withdrawn"


class UserCreatedApplication(BaseModel):
    job_id: str
    resume_id: str
    cover_letter_id: t.Optional[str] = None
    cover_letter_content: t.Optional[str] = None


class CreateApplication(UserCreatedApplication):
    user_id: str
    company_id: str
    cover_letter_id: t.Optional[str] = None
    user_application_status: UserApplicationStatus = UserApplicationStatus.submitted
    company_application_status: CompanyApplicationStatus = (
        CompanyApplicationStatus.pending
    )


class UpdateApplication(BaseModel):
    application_details: t.Optional[str] = None
    user_application_status: t.Optional[str] = None
    company_application_status: t.Optional[str] = None


class Application(CreateApplication, BaseDataModel):
    ...


entity_models = EntityModels(
    entity=Application,
    create=CreateApplication,
    update=UpdateApplication,
)


class UserUpdateApplication(BaseModel):
    application_details: t.Optional[UserApplicationStatus] = None
    user_application_status: t.Optional[UserApplicationStatus] = None


class CompanyUpdateApplication(BaseModel):
    company_application_status: t.Optional[CompanyApplicationStatus] = None

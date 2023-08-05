import typing as t
from datetime import datetime
from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel, EntityModels


class GetNotificationFilters(BaseModel):
    include_read: bool = False
    since: t.Optional[datetime] = None
    specific_applicant_id: t.Optional[str] = None
    specific_job_id: t.Optional[str] = None


class CreateGenericNotification(BaseModel):
    title: str
    notification: str
    application_id: str
    is_read: bool = False


class UpdateGenericNotification(BaseModel):
    is_read: bool


class GenericNotification(CreateGenericNotification, BaseDataModel):
    link: t.Optional[str] = None


entity_models = EntityModels(
    create=CreateGenericNotification,
    entity=GenericNotification,
    update=UpdateGenericNotification,
)

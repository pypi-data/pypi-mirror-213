from pydantic import BaseModel

from getajob.abstractions.models import EntityModels, BaseDataModel


class CreateResume(BaseModel):
    resume: str


class Resume(CreateResume, BaseDataModel):
    resume: str


entity_models = EntityModels(
    entity=Resume,
    create=CreateResume,
    update=CreateResume,
)

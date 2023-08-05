from pydantic import BaseModel

from getajob.abstractions.models import EntityModels, BaseDataModel


class CreateCoverLetter(BaseModel):
    cover_letter: str


class UpdateCoverLetter(CreateCoverLetter):
    ...


class CoverLetter(CreateCoverLetter, BaseDataModel):
    cover_letter: str


entity_models = EntityModels(
    entity=CoverLetter,
    create=CreateCoverLetter,
    update=UpdateCoverLetter,
)

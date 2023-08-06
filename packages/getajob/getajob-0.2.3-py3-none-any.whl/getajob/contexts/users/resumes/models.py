from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class CreateResume(BaseModel):
    resume: str


class Resume(CreateResume, BaseDataModel):
    resume: str

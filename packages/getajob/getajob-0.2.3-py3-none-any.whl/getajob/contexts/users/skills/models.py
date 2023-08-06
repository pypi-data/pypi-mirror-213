import typing as t

from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel


class CreateSkillSet(BaseModel):
    name: str
    skills: t.List[str]
    related_resume_id: t.Optional[str]


class UpdateSkillSet(BaseModel):
    skills: t.Optional[t.List[str]] = None
    related_resume_id: t.Optional[str] = None


class UserSkillsSet(CreateSkillSet, BaseDataModel):
    ...

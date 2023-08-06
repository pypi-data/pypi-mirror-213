import typing as t

from pydantic import BaseModel

from getajob.abstractions.models import EntityModels, BaseDataModel
from getajob.abstractions.models import Location


class UserCreateCompany(BaseModel):
    company_name: str
    company_description: str
    company_logo_url: t.Optional[str]
    headquarters_physical_address: Location
    company_phone_number: str
    benefits_offered: t.Optional[t.List[str]]


class CreateCompany(UserCreateCompany):
    company_admin_user_id: str


class UpdateCompany(BaseModel):
    company_admin_user_id: t.Optional[str]
    company_name: t.Optional[str]
    company_description: t.Optional[str]
    company_logo_url: t.Optional[str]
    headquarters_physical_address: t.Optional[Location]
    company_phone_number: t.Optional[str]
    benefits_offered: t.Optional[t.List[str]]


class Company(CreateCompany, BaseDataModel):
    ...


entity_models = EntityModels(entity=Company, create=CreateCompany, update=UpdateCompany)


class AlgoliaSearchableCompany(BaseModel):
    objectID: str
    company_name: str
    headquarters_physical_address: Location
    benefits_offered: t.Optional[t.List[str]]

import typing
from enum import Enum
from datetime import datetime
from dataclasses import dataclass

from pydantic import BaseModel

from getajob.config.settings import SETTINGS

DataSchema = typing.TypeVar("DataSchema", bound=BaseModel)


@dataclass
class PaginatedRequest:
    last: str = None  # type: ignore
    limit: int = SETTINGS.DEFAULT_PAGE_LIMIT


@dataclass
class PaginatedResponse:
    next: typing.Optional[dict]
    data: typing.List[DataSchema]  # type: ignore


@dataclass
class EntityModels:
    entity: DataSchema  # type: ignore
    create: typing.Optional[DataSchema] = None  # type: ignore
    update: typing.Optional[DataSchema] = None  # type: ignore


class BaseDataModel(BaseModel):
    id: str
    created: datetime
    updated: datetime


@dataclass
class MethodsToInclude:
    get_all: bool = True
    get_by_id: bool = True
    create: bool = True
    update: bool = True
    delete: bool = True


class Entity(str, Enum):
    USERS = "users"  # Comes from clerk
    USER_DETAILS = "user_details"  # What we add to user data
    ADMIN_USERS = "admin_users"
    SKILLS = "skills"
    COVER_LETTERS = "cover_letters"
    RESUMES = "resumes"
    COMPANIES = "companies"  # Comes from clerk
    COMPANY_DETAILS = "company_details"  # What we add to company data
    RECRUITERS = "recruiters"  # Comes from clerk
    RECRUITER_INVITATIONS = "recruiter_invitations"  # Comes from clerk
    RECRUITER_DETAILS = "recruiter_details"  # What we add to recruiter data
    JOBS = "jobs"
    APPLICATIONS = "applications"
    USER_NOTIFICATIONS = "user_notifications"
    SCHEDULED_EVENTS = "scheduled_events"


class Location(BaseModel):
    address_line_1: str
    address_line_2: str | None = None
    city: str
    state: str
    zipcode: str
    country: str
    lat: float
    lon: float

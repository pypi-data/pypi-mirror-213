import typing as t
from enum import Enum

from pydantic import BaseModel

from getajob.abstractions.models import EntityModels, BaseDataModel
from getajob.models.location import Location


class ScheduleType(str, Enum):
    FULL_TIME = "Full Time"
    PART_TIME = "Part Time"
    CONTRACT = "Contract"
    TEMPORARY = "Temporary"
    SEASONAL = "Seasonal"
    INTERNSHIP = "Internship"


class JobLocationType(str, Enum):
    REMOTE = "Remote"
    ON_SITE = "On Site"
    HYBRID = "Hybrid"


class JobContractLength(str, Enum):
    SHORT_TERM = "Short Term"
    LONG_TERM = "Long Term"


class PayType(str, Enum):
    HOURLY = "Hourly"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    YEARLY = "Yearly"


class Pay(BaseModel):
    pay_type: PayType
    pay_min: int
    pay_max: int
    exact_pay: t.Optional[int] = None
    includes_bonus: t.Optional[bool] = None
    includes_commission: t.Optional[bool] = None
    includes_equity: t.Optional[bool] = None
    includes_tips: t.Optional[bool] = None
    includes_vacation: t.Optional[bool] = None
    included_vacation_days: t.Optional[int] = None
    includes_relocation: t.Optional[bool] = None
    max_included_relocation_amount: t.Optional[int] = None
    includes_signing_bonus: t.Optional[bool] = None
    max_included_signing_bonus_amount: t.Optional[int] = None
    includes_stock: t.Optional[bool] = None


class UserCreateJob(BaseModel):
    position_title: str
    position_category: str
    description: str
    schedule: ScheduleType
    location: Location

    required_job_skills: t.Optional[t.List[str]]
    on_job_training_offered: t.Optional[bool]

    pay: Pay
    benefits: t.Optional[t.List[str]]
    background_check_required: t.Optional[bool]
    drug_test_required: t.Optional[bool]
    felons_accepted: t.Optional[bool]
    disability_accepted: t.Optional[bool]

    ideal_days_to_hire: t.Optional[int]
    internal_reference_code: t.Optional[str]
    job_associated_company_description: t.Optional[str]


class CreateJob(UserCreateJob):
    company_id: str
    view_count: int = 0


class UpdateJob(BaseModel):
    position_title: t.Optional[str] = None
    position_category: t.Optional[str] = None
    description: t.Optional[str] = None
    schedule: t.Optional[ScheduleType] = None
    location: t.Optional[Location] = None

    required_job_skills: t.Optional[t.List[str]] = None
    on_job_training_offered: t.Optional[bool] = None

    pay: t.Optional[Pay] = None
    benefits: t.Optional[t.List[str]] = None
    background_check_required: t.Optional[bool] = None
    drug_test_required: t.Optional[bool] = None
    felons_accepted: t.Optional[bool] = None
    disability_accepted: t.Optional[bool] = None

    ideal_days_to_hire: t.Optional[int] = None
    internal_reference_code: t.Optional[str]
    job_associated_company_description: t.Optional[str]


class InternalUpdateJob(UpdateJob):
    position_filled: t.Optional[bool] = None
    view_count: t.Optional[int] = None


class Job(CreateJob, BaseDataModel):
    position_filled: bool = False


entity_models = EntityModels(entity=Job, create=CreateJob, update=UpdateJob)

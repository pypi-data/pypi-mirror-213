from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from croniter import croniter

from getajob.abstractions.models import BaseDataModel


class ScheduledEventCategory(str, Enum):
    REPORT = "report"
    TASK = "task"
    EVENT = "event"


class CreateScheduledEvent(BaseModel):
    related_object_id: str
    name: str
    description: str
    cron: str
    event_category: ScheduledEventCategory
    event_type: str  # Any of the enums below, verified by scheduling service
    last_run_time: datetime | None = None
    next_run_time: datetime | None = None
    is_active: bool = True

    def calculate_next_invocation(self):
        cron = croniter(self.cron, datetime.utcnow())
        return cron.get_next(datetime)


class UpdateScheduledEvent(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    cron: str | None = None
    is_active: bool | None = None


class ScheduledEvent(BaseDataModel, CreateScheduledEvent):
    id: str


class ReportScheduledEvent(str, Enum):
    APPLICANT_SUMMARY = "applicant_summary"

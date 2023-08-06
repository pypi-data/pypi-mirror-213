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
    name: str
    description: str
    cron: str
    event_category: ScheduledEventCategory
    event_type: str  # Any of the enums below, verified by scheduling service
    last_run_time: datetime = None
    next_run_time: datetime = None
    is_active: bool = True

    def calculate_next_invocation(self):
        cron = croniter(self.cron, datetime.utcnow())
        return cron.get_next(datetime)


class UpdateScheduledEvent(BaseModel):
    name: str = None
    description: str = None
    start_date: datetime = None
    end_date: datetime = None
    cron: str = None
    is_active: bool = None


class ScheduledEvent(BaseDataModel, CreateScheduledEvent):
    id: str


class ReportScheduledEvent(str, Enum):
    APPLICANT_SUMMARY = "applicant_summary"

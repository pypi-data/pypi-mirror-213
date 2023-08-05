from typing import Any
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class DataModelAndFunction(BaseModel):
    model: Any  # BaseModel
    function: Any  # Callable


class KafkaTopic(str, Enum):
    users = "users"
    jobs = "jobs"
    companies = "companies"
    applications = "applications"
    candidates = "candidates"
    notifications = "notifications"
    communications = "communications"

    @classmethod
    def get_all_topics(cls):
        return [topic.value for topic in cls]


class KafkaEventConfig(BaseModel):
    topic: KafkaTopic
    get: bool = False
    create: bool = False
    update: bool = False
    delete: bool = False


class KafkaEventType(str, Enum):
    create = "create"
    update = "update"
    delete = "delete"
    get = "get"


class KafkaDeleteEvent(BaseModel):
    id: str


class BaseKafkaMessage(BaseModel):
    data: dict
    message_type: str
    message_time: datetime = datetime.now()


class KafkaNotificationsEnum(str, Enum):
    ...


class KafkaCommunicationsEnum(str, Enum):
    ...


class KafkaJobsEnum(str, Enum):
    create_jobs = "create_jobs"
    update_jobs = "update_jobs"
    delete_jobs = "delete_jobs"
    get_jobs = "get_jobs"


class KafkaCompaniesEnum(str, Enum):
    create_companies = "create_companies"
    update_companies = "update_companies"
    delete_companies = "delete_companies"


class KafkaApplicationsEnum(str, Enum):
    create_applications = "create_applications"
    update_applications = "update_applications"
    delete_applications = "delete_applications"
    get_applications = "get_applications"

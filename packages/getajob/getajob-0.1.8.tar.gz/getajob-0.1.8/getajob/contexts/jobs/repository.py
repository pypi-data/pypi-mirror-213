import typing as t
from getajob.vendor.firebase import FirestoreDB
from getajob.vendor.kafka.repository import KafkaRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic
from getajob.abstractions.repository import BaseRepository
from getajob.models.entities import Entity
from getajob.contexts.companies.repository import CompanyRepository

from .models import entity_models, CreateJob
from .unit_of_work import JobsUnitOfWork


class JobsRepository(BaseRepository):
    def __init__(self, db: FirestoreDB, kafka: t.Optional[KafkaRepository] = None):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.jobs, create=True, update=True, delete=True, get=True
        )
        super().__init__(
            db, Entity.JOBS.value, entity_models, kafka, kafka_event_config
        )
        self.kafka = kafka

    def create_job(self, job: CreateJob):
        return JobsUnitOfWork(self).create_job(
            company_repo=CompanyRepository(db=self.db, kafka=self.kafka), data=job
        )

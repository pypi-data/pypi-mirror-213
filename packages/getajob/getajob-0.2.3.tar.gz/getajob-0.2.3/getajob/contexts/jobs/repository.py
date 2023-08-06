import typing as t
from getajob.vendor.firebase import FirestoreDB
from getajob.vendor.kafka.repository import KafkaRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import Entity, EntityModels
from getajob.contexts.companies.repository import CompanyRepository

from .models import CreateJob, UpdateJob, Job
from .unit_of_work import JobsUnitOfWork


entity_models = EntityModels(entity=Job, create=CreateJob, update=UpdateJob)


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
            company_repo=CompanyRepository(db=self.db), data=job
        )

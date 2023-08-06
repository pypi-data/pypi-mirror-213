import typing as t
from getajob.vendor.firebase import FirestoreDB
from getajob.vendor.kafka.repository import KafkaRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic
from getajob.abstractions.repository import BaseRepository
from getajob.contexts.users.users.repository import UserRepository
from getajob.abstractions.models import Entity

from .models import entity_models, CreateCompany
from .unit_of_work import CompanyUnitOfWork


class CompanyRepository(BaseRepository):
    def __init__(self, db: FirestoreDB, kafka: t.Optional[KafkaRepository] = None):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.companies,
            create=True,
            update=True,
            delete=True,
        )
        super().__init__(
            db, Entity.COMPANIES.value, entity_models, kafka, kafka_event_config
        )
        self.kafka = kafka

    def create_company(self, data: CreateCompany):
        return CompanyUnitOfWork(
            user_repo=UserRepository(self.db), company_repo=self
        ).create_company(data)

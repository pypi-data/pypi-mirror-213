import typing as t

from getajob.vendor.firebase import FirestoreFilters, FirestoreDB
from getajob.vendor.kafka.repository import KafkaRepository
from getajob.abstractions.repository import BaseRepository
from getajob.contexts.users.resumes.repository import ResumeRepository
from getajob.contexts.jobs.repository import JobsRepository
from getajob.contexts.companies.repository import CompanyRepository
from getajob.contexts.users.cover_letters.repository import CoverLetterRepository
from getajob.contexts.users.users.repository import UserRepository
from getajob.contexts.notifications.repository import NotificationRepository
from getajob.contexts.applications.models import (
    CompanyUpdateApplication,
    UserUpdateApplication,
    Application,
    UserCreatedApplication,
)
from getajob.models.entities import Entity

from .models import entity_models
from .unit_of_work import ApplicationsUnitOfWork


class ApplicationRepository(BaseRepository):
    def __init__(self, db: FirestoreDB, kafka: KafkaRepository):
        super().__init__(db, Entity.APPLICATIONS.value, entity_models)
        self.kafka = kafka

    def user_creates_application(
        self, user_id: str, application: UserCreatedApplication
    ):
        return ApplicationsUnitOfWork(self, self.kafka).user_creates_application(
            user_id=user_id,
            resume_repo=ResumeRepository(self.db),
            cover_letter_repo=CoverLetterRepository(self.db),
            job_repo=JobsRepository(self.db, self.kafka),
            user_repo=UserRepository(self.db),
            create_application=application,
        )

    def get_applications_by_job(self, company_id: str, job_id: str):
        return super().query(
            filters=[
                FirestoreFilters(field="company_id", operator="==", value=company_id),
                FirestoreFilters(field="job_id", operator="==", value=job_id),
            ],
        )

    def get_application_by_job_and_application_id(
        self, job_application_id: str, company_id: str, job_id: str
    ):
        return super().get_with_filters(
            doc_id=job_application_id,
            filters=[
                FirestoreFilters(field="company_id", operator="==", value=company_id),
                FirestoreFilters(field="job_id", operator="==", value=job_id),
            ],
        )

    def do_company_application_update(
        self,
        job_application_id: str,
        company_id: str,
        job_id: str,
        update: CompanyUpdateApplication,
    ):
        application = self.get_application_by_job_and_application_id(
            job_application_id, company_id, job_id
        )
        application = t.cast(Application, application)
        return ApplicationsUnitOfWork(self, self.kafka).do_company_application_update(
            application,
            update,
            job_repo=JobsRepository(self.db, self.kafka),
            company_repo=CompanyRepository(self.db, self.kafka),
            notification_repo=NotificationRepository(self.db),
        )

    def get_applications_by_user(self, user_id):
        return super().query(
            filters=[
                FirestoreFilters(
                    field="user_id",
                    operator="==",
                    value=user_id,
                )
            ],
        )

    def get_application_by_user_id_and_application_id(
        self, user_id: str, job_application_id: str
    ):
        return super().get_with_filters(
            doc_id=job_application_id,
            filters=[
                FirestoreFilters(
                    field="user_id",
                    operator="==",
                    value=user_id,
                )
            ],
        )

    def do_user_application_update(
        self, user_id: str, job_application_id: str, update: UserUpdateApplication
    ):
        application = self.get_application_by_user_id_and_application_id(
            user_id, job_application_id
        )
        application = t.cast(Application, application)
        return ApplicationsUnitOfWork(self, self.kafka).do_user_application_update(
            application,
            update,
            notification_repo=NotificationRepository(self.db),
            user_repo=UserRepository(self.db),
            job_repo=JobsRepository(self.db, self.kafka),
        )

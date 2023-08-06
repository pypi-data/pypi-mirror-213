import typing as t

from getajob.models.entities import Entity
from getajob.abstractions.repository import BaseRepository
from getajob.exceptions import JobHasBeenFilledException, UserAlreadyAppliedException
from getajob.vendor.firebase import FirestoreFilters
from getajob.contexts.applications.models import (
    CompanyUpdateApplication,
    UserUpdateApplication,
    Application,
    CreateApplication,
    UserCreatedApplication,
)
from getajob.contexts.users.users.models import User
from getajob.contexts.notifications.models import CreateGenericNotification
from getajob.contexts.jobs.models import Job
from getajob.contexts.companies.models import Company
from getajob.contexts.users.cover_letters.models import CreateCoverLetter, CoverLetter
from getajob.vendor.kafka.repository import KafkaRepository


class ApplicationsUnitOfWork:
    def __init__(
        self,
        application_repo: BaseRepository,
        kafka_repo: t.Optional[KafkaRepository] = None,
    ):
        self.application_repo = application_repo
        self.kafka_repo = kafka_repo

    def user_creates_application(
        self,
        user_id: str,
        user_repo: BaseRepository,
        resume_repo: BaseRepository,
        cover_letter_repo: BaseRepository,
        job_repo: BaseRepository,
        create_application: UserCreatedApplication,
    ):
        # Check that the company and job is still viable
        job = job_repo.get(create_application.job_id)
        job = t.cast(Job, job)
        if job.position_filled:
            raise JobHasBeenFilledException

        # Check that user hasn't already applied to this job
        user_application = self.application_repo.query(
            filters=[
                FirestoreFilters(field="user_id", operator="==", value=user_id),
                FirestoreFilters(
                    field="job_id", operator="==", value=create_application.job_id
                ),
            ]
        )
        if user_application.data:
            raise UserAlreadyAppliedException

        # Update the application with the company id
        create_application = CreateApplication(
            **create_application.dict(), user_id=user_id, company_id=job.company_id
        )

        # Check that resume exists
        user = t.cast(User, user_repo.get(user_id))
        assert resume_repo.get(
            parent_collections={Entity.USERS.value: user_id},
            doc_id=create_application.resume_id,
        )

        # If cover letter provided, check ID
        if create_application.cover_letter_id:
            assert cover_letter_repo.get(
                parent_collections={Entity.USERS.value: user_id},
                doc_id=create_application.cover_letter_id,
            )
        else:
            # Otherwise, if cover letter content provided, create cover letter
            if create_application.cover_letter_content:
                created_cover_letter = cover_letter_repo.create(
                    parent_collections={Entity.USERS.value: user_id},
                    data=CreateCoverLetter(
                        cover_letter=create_application.cover_letter_content
                    ),
                )
                created_cover_letter = t.cast(CoverLetter, created_cover_letter)
                create_application.cover_letter_id = created_cover_letter.id

        # Create the application
        return self.application_repo.create(data=create_application)

    def do_company_application_update(
        self,
        application: Application,
        update: CompanyUpdateApplication,
        job_repo: BaseRepository,
        company_repo: BaseRepository,
        notification_repo: BaseRepository,
    ):
        application_as_dict = application.dict()
        application_as_dict.update(update.dict(exclude_unset=True))
        updated_application = Application(**application_as_dict)

        job = t.cast(Job, job_repo.get(updated_application.job_id))
        company = t.cast(Company, company_repo.get(doc_id=job.company_id))
        notification_repo.create(
            parent_collections={Entity.USERS.value: application.user_id},
            data=CreateGenericNotification(
                title=f"Application {update.company_application_status} for {job.position_title}",
                notification=f"{company.company_name} has {update.company_application_status} to your job application for {job.position_title}",
                application_id=application.id,
            ),
        )

        return self.application_repo.update(
            doc_id=updated_application.id,
            data=updated_application,
        )

    def do_user_application_update(
        self,
        application: Application,
        update: UserUpdateApplication,
        user_repo: BaseRepository,
        job_repo: BaseRepository,
        notification_repo: BaseRepository,
    ):
        application_as_dict = application.dict()
        application_as_dict.update(update.dict(exclude_unset=True))
        updated_application = Application(**application_as_dict)
        response = self.application_repo.update(
            doc_id=application.id, data=updated_application
        )

        user = t.cast(User, user_repo.get(doc_id=updated_application.user_id))
        job = t.cast(Job, job_repo.get(updated_application.job_id))
        notification_repo.create(
            parent_collections={Entity.COMPANIES.value: job.company_id},
            data=CreateGenericNotification(
                title=f"Applicant is{update.user_application_status} for {job.position_title}",
                notification=f"{user.first_name} {user.last_name} has {update.user_application_status} to your job posting for {job.position_title}",
                application_id=application.id,
            ),
        )

        return response

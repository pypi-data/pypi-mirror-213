import typing as t
from getajob.abstractions.repository import BaseRepository

from .models import CreateJob, Job


class JobsUnitOfWork:
    def __init__(self, job_repo: BaseRepository):
        self.repo = job_repo

    def create_job(self, company_repo: BaseRepository, data: CreateJob):
        # Check the company exists
        assert company_repo.get(data.company_id)
        job = self.repo.create(data)
        job = t.cast(Job, job)
        return job

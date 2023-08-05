import typing as t

from getajob.exceptions import (
    UserAlreadyRecruiterException,
    CompanyNameAlreadyTakenException,
)
from getajob.contexts.users.users.models import User, UpdateUser
from getajob.abstractions.repository import BaseRepository
from .models import CreateCompany, Company


class CompanyUnitOfWork:
    def __init__(
        self,
        user_repo: BaseRepository,
        company_repo: BaseRepository,
    ):
        self.user_repo = user_repo
        self.company_repo = company_repo

    def create_company(self, data: CreateCompany) -> Company:
        user = self.user_repo.get(data.company_admin_user_id)
        user = t.cast(User, user)

        if user.company_id is not None:
            raise UserAlreadyRecruiterException
        data.company_admin_user_id = user.id

        # Check if company name has been taken
        if self.company_repo.get_one_by_attribute("company_name", data.company_name):
            raise CompanyNameAlreadyTakenException

        # Create the company
        created_company = self.company_repo.create(data)
        created_company = t.cast(Company, created_company)

        # Update the user to be admin on this company
        self.user_repo.update(
            doc_id=user.id,
            data=UpdateUser(
                company_id=created_company.id,
                company_admin=True,
            ),
        )
        return created_company

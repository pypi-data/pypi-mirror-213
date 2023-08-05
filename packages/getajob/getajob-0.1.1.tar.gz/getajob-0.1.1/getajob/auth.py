import typing as t
from fastapi import Request

from getajob.vendor.firebase import FirestoreDB
from getajob.exceptions import (
    UserIsNotAdminException,
    UserAdminPermissionsNotHighEnoughException,
    UserIsNotRecruiterException,
    UserRecruiterPermissionsNotHighEnoughException,
)
from getajob.contexts.admin.users.models import AdminUser, AdminRole
from getajob.contexts.recruiters.models import Recruiter, RecruiterRole
from getajob.contexts.admin.users.repository import AdminUserRepository
from getajob.contexts.recruiters.repository import RecruiterRepository


def admin_user_permissions_high_enough(user_role: AdminRole, required_role: AdminRole):
    return user_role.get_precedence() >= required_role.get_precedence()


def recruiter_permissions_high_enough(
    user_role: RecruiterRole, required_role: RecruiterRole
):
    return user_role.get_precedence() >= required_role.get_precedence()


class AuthenticationRepository:
    def __init__(self, db: FirestoreDB):
        self.db = db

    async def get_admin_user(self, user_id: str) -> AdminUser:
        repo = AdminUserRepository(self.db)
        user = repo.get_by_user_id(user_id)
        if not user:
            raise UserIsNotAdminException
        return t.cast(AdminUser, user)

    async def get_recruiter(self, user_id: str) -> Recruiter:
        repo = RecruiterRepository(self.db)
        user = repo.get_by_user_id(user_id)
        if not user:
            raise UserIsNotRecruiterException
        return t.cast(Recruiter, user)

    async def check_admin_privilages(self, user_id: str, required_role: AdminRole):
        user = await self.get_admin_user(user_id)
        if not admin_user_permissions_high_enough(user.role, required_role):
            raise UserAdminPermissionsNotHighEnoughException

    async def check_recruiter_privilages(
        self, user_id: str, required_role: RecruiterRole
    ):
        user = await self.get_recruiter(user_id)
        if not recruiter_permissions_high_enough(user.role, required_role):
            raise UserRecruiterPermissionsNotHighEnoughException

    async def user_is_super_admin(self, request: Request):
        return await self.check_admin_privilages(
            request.state.user.id, AdminRole.SUPER_ADMIN
        )

    async def user_is_admin(self, request: Request):
        return await self.check_admin_privilages(request.state.user.id, AdminRole.ADMIN)

    async def user_is_read_only(self, request: Request):
        return await self.check_admin_privilages(
            request.state.user.id, AdminRole.READ_ONLY
        )

    async def recruiter_is_super_admin(self, request: Request):
        return await self.check_recruiter_privilages(
            request.state.user.id, RecruiterRole.SUPER_ADMIN
        )

    async def recruiter_is_admin(self, request: Request):
        return await self.check_recruiter_privilages(
            request.state.user.id, RecruiterRole.ADMIN
        )

    async def recruiter_is_read_only(self, request: Request):
        return await self.check_recruiter_privilages(
            request.state.user.id, RecruiterRole.READ_ONLY
        )

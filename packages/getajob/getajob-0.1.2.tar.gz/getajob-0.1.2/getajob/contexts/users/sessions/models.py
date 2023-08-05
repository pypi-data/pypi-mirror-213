import typing as t

from pydantic import BaseModel


class SessionData(BaseModel):
    email: str
    exp: int
    id: str
    name: str
    sid: t.Optional[str] = None
    sub: t.Optional[str] = None
    phone: t.Optional[str] = None
    company_id: t.Optional[str] = None
    company_admin: bool = False

import typing as t

from pydantic import BaseModel


class Location(BaseModel):
    address_line_1: str
    address_line_2: t.Optional[str] = None
    city: str
    state: str
    zipcode: str
    country: str
    lat: float
    lon: float

from pydantic import BaseModel

from getajob.abstractions.models import Entity


class AdminEntitySearch(BaseModel):
    entity_type: Entity
    sub_collection: bool = False

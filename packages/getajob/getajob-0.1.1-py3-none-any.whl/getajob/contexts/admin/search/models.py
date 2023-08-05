from pydantic import BaseModel

from getajob.models.entities import Entity


class AdminEntitySearch(BaseModel):
    entity_type: Entity
    sub_collection: bool = False

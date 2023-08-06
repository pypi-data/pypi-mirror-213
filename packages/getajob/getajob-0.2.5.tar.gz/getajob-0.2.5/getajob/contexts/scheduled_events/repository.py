from datetime import datetime
from getajob.vendor.firebase import FirestoreDB, FirestoreFilters, FirestorePagination
from getajob.abstractions.repository import BaseRepository
from getajob.abstractions.models import EntityModels, Entity

from .models import (
    CreateScheduledEvent,
    UpdateScheduledEvent,
    ScheduledEvent,
)

entity_models = EntityModels(
    entity=ScheduledEvent,
    create=CreateScheduledEvent,
    update=UpdateScheduledEvent,
)


class ScheduledEventsRepository(BaseRepository):
    def __init__(self, db: FirestoreDB):
        super().__init__(db, Entity.SCHEDULED_EVENTS.value, entity_models)

    def create_scheduled_event(self, data: CreateScheduledEvent):
        data.next_run_time = data.calculate_next_invocation()
        return super().create(data)

    def get_current_scheduled_events(self, page: dict | None = None):
        if not page:
            return self.query(
                filters=[
                    FirestoreFilters(
                        field="next_run_time", operator="<=", value=datetime.utcnow()
                    ),
                    FirestoreFilters(field="is_active", operator="==", value=True),
                ],
            )
        return self.query(
            filters=[
                FirestoreFilters(
                    field="next_run_time", operator="<=", value=datetime.utcnow()
                ),
                FirestoreFilters(field="is_active", operator="==", value=True),
            ],
            pagination=FirestorePagination(start_after=page),
        )

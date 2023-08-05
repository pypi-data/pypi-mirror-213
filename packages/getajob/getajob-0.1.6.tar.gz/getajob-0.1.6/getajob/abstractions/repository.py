import typing as t
from datetime import datetime

from pydantic import BaseModel

from getajob.utils import (
    generate_random_short_code,
)
from getajob.vendor.firebase import (
    FirestoreDocument,
    FirestorePagination,
    FirestoreFilters,
    FirestoreOrderBy,
    FirestorePaginatedResponse,
    FirestoreDB,
)
from getajob.vendor.kafka.repository import KafkaRepository
from getajob.vendor.kafka.models import (
    KafkaEventConfig,
    KafkaEventType,
    BaseKafkaMessage,
    KafkaDeleteEvent,
)
from .models import EntityModels, PaginatedResponse


def format_to_schema(document: FirestoreDocument, entity_model: BaseModel) -> BaseModel:
    id_included_dict = {
        "id": document.id,
        **document.data,
    }
    return entity_model(**id_included_dict)  # type: ignore


def format_paginated_response(
    res: FirestorePaginatedResponse, entity_model: t.Optional[BaseModel] = None
):
    if entity_model is None:
        data = res.results
    else:
        data = [
            format_to_schema(doc, entity_model) for doc in res.results  # type: ignore
        ]
    return PaginatedResponse(data=data, next=res.start_after)


def query_collection(
    db: FirestoreDB,
    collection_name: str,
    parent_collections: dict = {},
    entity_model: t.Optional[BaseModel] = None,
    filters: t.Optional[t.List[FirestoreFilters]] = None,
    order_by: t.Optional[FirestoreOrderBy] = None,
    pagination: FirestorePagination = FirestorePagination(),
):
    res = db.query(
        parent_collections=parent_collections,
        collection_name=collection_name,
        filters=filters,
        order_by=order_by,
        pagination=pagination,
    )
    return format_paginated_response(res, entity_model)


def query_subcollections(
    db: FirestoreDB,
    collection_name: str,
    entity_model: t.Optional[BaseModel] = None,
    filters: t.Optional[t.List[FirestoreFilters]] = None,
    order_by: t.Optional[FirestoreOrderBy] = None,
    pagination: FirestorePagination = FirestorePagination(),
):
    res = db.query_subcollections(
        collection_name=collection_name,
        filters=filters,
        order_by=order_by,
        pagination=pagination,
    )
    return format_paginated_response(res, entity_model)


class BaseRepository:
    def __init__(
        self,
        db: FirestoreDB,
        collection_name: str,
        entity_models: EntityModels,
        kafka: t.Optional[KafkaRepository] = None,
        kafka_event_config: t.Optional[KafkaEventConfig] = None,
    ):
        self.db = db
        self.collection_name = collection_name
        self.entity_models = entity_models
        self.kafka = kafka
        self.kafka_event_config = kafka_event_config

        # If kafka given but no configuration, complain about it
        if self.kafka and not self.kafka_event_config:
            raise ValueError("Kafka event topic must be provided")

    def _produce_repository_kafka_event(
        self, event_type: KafkaEventType, data: BaseModel
    ):
        if (
            not self.kafka
            or not self.kafka_event_config
            or not self.kafka_event_config.dict()[event_type]
        ):
            return
        self.kafka.publish(
            topic=self.kafka_event_config.topic,
            message=BaseKafkaMessage(
                message_type=f"{event_type.value}_{self.collection_name}",
                data=data.dict(),
            ),
        )

    def get(
        self,
        doc_id: str,
        parent_collections: dict = {},
    ) -> BaseModel:
        res = self.db.get(parent_collections, self.collection_name, doc_id)
        self._produce_repository_kafka_event(event_type=KafkaEventType.get, data=res)
        return format_to_schema(res, self.entity_models.entity)

    def get_with_filters(
        self,
        doc_id: str,
        filters: t.List[FirestoreFilters],
        parent_collections: dict = {},
    ) -> BaseModel:
        res = self.db.get_with_filters(
            parent_collections, self.collection_name, doc_id, filters
        )
        return format_to_schema(res, self.entity_models.entity)

    def create(
        self,
        data: BaseModel,
        parent_collections: dict = {},
        provided_id: t.Optional[str] = None,
    ) -> BaseModel:
        data_dict = data.dict()
        data_dict["created"] = datetime.now()
        data_dict["updated"] = datetime.now()
        document_id = provided_id or generate_random_short_code()
        res = self.db.create(
            parent_collections=parent_collections,
            collection_name=self.collection_name,
            document_id=document_id,
            document_data=data_dict,
        )
        self._produce_repository_kafka_event(event_type=KafkaEventType.create, data=res)
        return format_to_schema(res, self.entity_models.entity)

    def update(
        self,
        doc_id: str,
        data: BaseModel,
        parent_collections: dict = {},
    ) -> BaseModel:
        original_item = self.get(doc_id, parent_collections).dict()
        for key, val in data.dict().items():
            if val is not None:
                original_item[key] = val
        original_item["updated"] = datetime.now()
        res = self.db.update(
            parent_collections, self.collection_name, doc_id, original_item
        )
        self._produce_repository_kafka_event(event_type=KafkaEventType.update, data=res)
        return format_to_schema(res, self.entity_models.entity)

    def delete(
        self,
        doc_id: str,
        parent_collections: dict = {},
    ) -> bool:
        assert self.get(doc_id, parent_collections)
        self._produce_repository_kafka_event(
            event_type=KafkaEventType.delete, data=KafkaDeleteEvent(id=doc_id)
        )
        return self.db.delete(parent_collections, self.collection_name, doc_id)

    def get_one_by_attribute(
        self,
        attribute: str,
        value: t.Any,
        parent_collections: dict = {},
    ) -> t.Union[BaseModel, None]:
        res = self.db.get_one_by_attribute(
            parent_collections, self.collection_name, attribute, value
        )
        if not res:
            return None
        return format_to_schema(res, self.entity_models.entity)

    def query(
        self,
        parent_collections: dict = {},
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
    ) -> PaginatedResponse:
        return query_collection(
            db=self.db,
            collection_name=self.collection_name,
            entity_model=self.entity_models.entity,
            parent_collections=parent_collections,
            filters=filters,
            order_by=order_by,
            pagination=pagination,
        )

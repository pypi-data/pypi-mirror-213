import typing as t

from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.client import Client
from google.cloud.firestore_v1.base_query import BaseQuery

from getajob.config.settings import SETTINGS
from getajob.exceptions import EntityNotFound


class FirestorePagination(BaseModel):
    start_after: t.Optional[dict] = None
    limit: int = SETTINGS.DEFAULT_PAGE_LIMIT

    class Config:
        arbitrary_types_allowed = True


class FirestoreFilters(BaseModel):
    field: str
    operator: t.Literal[
        "==",
        ">",
        "<",
        ">=",
        "<=",
        "array-contains",
        "in",
        "array-contains-any",
        "not-in",
        "like",  # The like operator is custom soft text
    ]
    value: t.Any


class FirestoreOrderBy(BaseModel):
    field: str
    direction: t.Literal["ASCENDING", "DESCENDING"]


class FirestoreDocument(BaseModel):
    id: str
    data: t.Dict[str, t.Any]


class FirestorePaginatedResponse(BaseModel):
    results: t.List[FirestoreDocument]
    start_after: t.Optional[dict] = None
    count: int = 0

    class Config:
        arbitrary_types_allowed = True


class FirestoreBatchAction(BaseModel):
    action: t.Literal["create", "update", "delete"]
    parent_collections: dict
    collection_name: str
    document_id: str
    document_data: dict


class ParentAndCollection(BaseModel):
    parents: dict
    collection: str
    id: str


def list_of_parent_collections(input_dict: dict) -> t.List[ParentAndCollection]:
    output_list = []
    parent_dict: t.Dict[str, str] = {}
    for key in input_dict:
        parent_dict_copy = parent_dict.copy()
        output_list.append(
            ParentAndCollection(
                parents=parent_dict_copy, collection=key, id=input_dict[key]
            )
        )
        parent_dict[key] = input_dict[key]
    return output_list


def get_client():
    cred = credentials.Certificate(
        {
            "type": "service_account",
            "project_id": SETTINGS.FIRESTORE_PROJECT_ID,
            "private_key_id": SETTINGS.FIRESTORE_PRIVATE_KEY_ID,
            "private_key": SETTINGS.FIRESTORE_PRIVATE_KEY,
            "client_email": SETTINGS.FIRESTORE_CLIENT_EMAIL,
            "client_id": SETTINGS.FIRESTORE_CLIENT_ID,
            "auth_uri": SETTINGS.FIRESTORE_AUTH_URI,
            "token_uri": SETTINGS.FIRESTORE_TOKEN_URI,
            "auth_provider_x509_cert_url": SETTINGS.FIRESTORE_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": SETTINGS.FIRESTORE_CLIENT_X509_CERT_URL,
        }
    )
    firebase_admin.initialize_app(cred)
    return firestore.client()


def add_filters_to_query(query_reference: BaseQuery, filters: t.List[FirestoreFilters]):
    for _filter in filters:
        if _filter.operator == "like":
            query_reference = query_reference.where(
                _filter.field, ">=", _filter.value
            ).where(_filter.field, "<=", _filter.value + "\uf8ff")
        else:
            query_reference = query_reference.where(
                _filter.field, _filter.operator, _filter.value
            )
    return query_reference


class FirestoreDB:
    def __init__(self, client: Client):
        self._client = client

    def disconnect(self):
        if type(self._client) == Client:
            self._client.close()

    def _get_collection_ref(self, parent_collections: dict, collection_name: str):
        collection_ref = self._client
        for parent, parent_id in parent_collections.items():
            collection_ref = collection_ref.collection(parent).document(parent_id)  # type: ignore
        return collection_ref.collection(collection_name)

    def _verify_parent_exists(self, parent_collections: dict) -> None:
        if not parent_collections:
            return None
        all_parent_collections = list_of_parent_collections(parent_collections)
        for parent_collection in all_parent_collections:
            # This will raise an exception if the parent doesn't exist
            self.get(
                parent_collection.parents,
                parent_collection.collection,
                parent_collection.id,
            )

    def create(
        self,
        parent_collections: dict,
        collection_name: str,
        document_id: str,
        document_data: dict,
    ):
        self._verify_parent_exists(parent_collections)
        collection_ref = self._get_collection_ref(parent_collections, collection_name)
        doc_ref = collection_ref.document(document_id)
        doc_ref.set(document_data)
        return self.get(parent_collections, collection_name, doc_ref.id)

    def get(self, parent_collections: dict, collection_name: str, document_id: str):
        collection_ref = self._get_collection_ref(parent_collections, collection_name)
        doc_ref = collection_ref.document(document_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise EntityNotFound(collection_name, document_id)
        return FirestoreDocument(id=doc.id, data=doc.to_dict() or {})

    def get_with_filters(
        self,
        parent_collections: dict,
        collection_name: str,
        document_id: str,
        filters: t.List[FirestoreFilters],
    ):
        self._verify_parent_exists(parent_collections)
        document = self.get(parent_collections, collection_name, document_id)
        for f in filters:
            if document.data.get(f.field) != f.value:
                raise EntityNotFound(collection_name, document_id)
        return document

    def update(
        self,
        parent_collections: dict,
        collection_name: str,
        document_id: str,
        document_data: dict,
    ):
        collection_ref = self._get_collection_ref(parent_collections, collection_name)
        doc_ref = collection_ref.document(document_id)
        if not doc_ref.get().exists:
            raise EntityNotFound(collection_name, document_id)
        doc_ref.set(document_data, merge=True)
        return self.get(parent_collections, collection_name, doc_ref.id)

    def delete(
        self, parent_collections: dict, collection_name: str, document_id: str
    ) -> bool:
        collection_ref = self._get_collection_ref(parent_collections, collection_name)
        doc_ref = collection_ref.document(document_id)
        if not doc_ref.get().exists:
            raise EntityNotFound(collection_name, document_id)
        collection_ref = self._get_collection_ref(parent_collections, collection_name)
        doc_ref = collection_ref.document(document_id)
        doc_ref.delete()
        return True

    def query(
        self,
        parent_collections: dict,
        collection_name: str,
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
    ) -> FirestorePaginatedResponse:
        self._verify_parent_exists(parent_collections)
        query_reference = self._get_collection_ref(parent_collections, collection_name)
        return self.perform_query(
            query_reference=query_reference,  # type: ignore
            filters=filters,
            order_by=order_by,
            pagination=pagination,
        )

    def query_subcollections(
        self,
        collection_name: str,
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
    ) -> FirestorePaginatedResponse:
        if type(self._client) != Client:
            raise NotImplementedError(
                "Querying subcollections is not supported in local testing"
            )
        query_reference = self._client.collection_group(collection_name)
        return self.perform_query(
            query_reference=query_reference,
            filters=filters,
            order_by=order_by,
            pagination=pagination,
        )

    def perform_query(
        self,
        query_reference: BaseQuery,
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
    ):
        # Apply filters, sort, and pagination
        if filters:
            query_reference = add_filters_to_query(query_reference, filters)
        if order_by:
            query_reference = query_reference.order_by(
                order_by.field, direction=order_by.direction
            )
        if pagination.start_after is not None:
            query_reference = query_reference.start_after(pagination.start_after)
        query_reference = query_reference.limit(pagination.limit)

        # Get the results
        result_stream = list(query_reference.stream())
        if len(result_stream) == 0:
            return FirestorePaginatedResponse(results=[], start_after=None)
        return FirestorePaginatedResponse(
            results=[
                FirestoreDocument(id=result.id, data=result.to_dict())  # type: ignore
                for result in result_stream
            ],
            start_after=result_stream[-1].to_dict(),
        )

    def get_one_by_attribute(
        self,
        parent_collections: dict,
        collection_name: str,
        attribute: str,
        value: str,
    ) -> t.Union[FirestoreDocument, None]:
        res = self.query(
            parent_collections=parent_collections,
            collection_name=collection_name,
            filters=[FirestoreFilters(field=attribute, operator="==", value=value)],
        )
        if len(res.results) == 1:
            return res.results[0]
        elif len(res.results) > 1:
            raise Exception(
                f"More than one document found with attribute {attribute}={value}",
            )
        return None

    def batch_action(self, writes: t.List[FirestoreBatchAction]) -> list:
        batch = self._client.batch()
        for write in writes:
            if write.action == "create":
                collection_ref = self._get_collection_ref(
                    write.parent_collections, write.collection_name
                )
                doc_ref = collection_ref.document(write.document_id)
                batch.set(doc_ref, write.document_data)
            elif write.action == "update":
                collection_ref = self._get_collection_ref(
                    write.parent_collections, write.collection_name
                )
                doc_ref = collection_ref.document(write.document_id)
                batch.update(doc_ref, write.document_data)
            elif write.action == "delete":
                collection_ref = self._get_collection_ref(
                    write.parent_collections, write.collection_name
                )
                doc_ref = collection_ref.document(write.document_id)
                batch.delete(doc_ref)
        return batch.commit()

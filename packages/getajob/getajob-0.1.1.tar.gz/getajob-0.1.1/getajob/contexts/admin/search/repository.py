from getajob.abstractions.repository import query_subcollections, query_collection
from getajob.vendor.firebase import FirestoreDB

from .models import AdminEntitySearch


class AdminSearchRepository:
    def __init__(self, db: FirestoreDB):
        self.db = db

    def admin_collection_search(self, search: AdminEntitySearch):
        if search.sub_collection:
            return query_subcollections(
                db=self.db, collection_name=search.entity_type.value
            )
        return query_collection(db=self.db, collection_name=search.entity_type.value)

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from algoliasearch.search_client import SearchClient

from getajob.config.settings import SETTINGS


class IndexName(str, Enum):
    job_search = "job_search"
    company_search = "company_search"
    candidate_search = "candidate_search"


class SearchQuery(BaseModel):
    index_name: str
    query: str
    attributes_to_search: Optional[List[str]] = None
    filters: Optional[str] = None
    facet_filters: Optional[List[List[str]]] = None


class AlgoliaResult(BaseModel):
    hits: List[dict]
    nbHits: int
    page: int
    nbPages: int
    hitsPerPage: int
    exhaustiveNbHits: bool
    query: str
    params: str
    processingTimeMS: int
    serverTimeMS: int


class AlgoliaSearchRepository:
    def __init__(self, index_name: IndexName, client: Optional[SearchClient] = None):
        self.index_name = index_name.value
        self.client = client or SearchClient.create(
            SETTINGS.ALGOLA_APP_ID, SETTINGS.ALGOLIA_API_KEY
        )

    def search(self, search_query: SearchQuery):
        algolia_index = self.client.init_index(search_query.index_name)
        search_parameters = {}
        if search_query.attributes_to_search:
            search_parameters["restrictSearchableAttributes"] = ",".join(
                search_query.attributes_to_search
            )
        if search_query.filters:
            search_parameters["filters"] = search_query.filters
        if search_query.facet_filters:
            search_parameters["facetFilters"] = search_query.facet_filters  # type: ignore
        res = algolia_index.search(search_query.query, search_parameters)
        return AlgoliaResult(**res)

    def add_record(self, record: dict):
        algolia_index = self.client.init_index(self.index_name)
        algolia_index.save_object(record)

    def delete_record(self, record_id: str):
        algolia_index = self.client.init_index(self.index_name)
        algolia_index.delete_object(record_id)

    def update_record(self, record: dict):
        algolia_index = self.client.init_index(self.index_name)
        algolia_index.partial_update_object(record)

    def get_record(self, record_id: str):
        algolia_index = self.client.init_index(self.index_name)
        return algolia_index.get_object(record_id)

    def get_records(self, record_ids: List[str]):
        algolia_index = self.client.init_index(self.index_name)
        return algolia_index.get_objects(record_ids)  # type: ignore

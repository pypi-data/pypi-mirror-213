from algoliasearch.search_client import SearchClient

from .models import AlgoliaIndex, AlgoliaSearchParams


def get_client(app_id: str, api_key: str):
    return SearchClient.create(app_id, api_key)


class AlgoliaSearch:
    def __init__(self, client: SearchClient, index_name: AlgoliaIndex):
        self.index = client.init_index(index_name)

    def search(self, query: AlgoliaSearchParams):
        search_params = {
            "query": query.query,
            "page": query.page,
            "hitsPerPage": query.hits_per_page,
        }
        if query.filters:
            search_params["filters"] = query.filters
        if query.facet_filters:
            search_params["facetFilters"] = query.facet_filters
        if query.attributes_to_retrieve:
            search_params["attributesToRetrieve"] = query.attributes_to_retrieve
        return self.index.search(query, search_params)

    def get_object(self, object_id):
        return self.index.get_object(object_id)

    def add_object(self, object_data, object_id: str | None = None):
        if object_id:
            object_data["objectID"] = object_id
        return self.index.save_object(object_data)

    def update_object(self, object_id, object_data):
        return self.index.save_object(object_data, object_id)

    def delete_object(self, object_id):
        return self.index.delete_object(object_id)

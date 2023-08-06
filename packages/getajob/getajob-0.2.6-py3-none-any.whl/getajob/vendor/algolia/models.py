from enum import Enum
from pydantic import BaseModel
from typing import Optional, List


class AlgoliaIndex(str, Enum):
    job_search = "job_search"
    company_search = "company_search"
    candidate_search = "candidate_search"


class AlgoliaSearchParams(BaseModel):
    query: str
    filters: Optional[str] = None
    facet_filters: Optional[List[str]] = None
    attributes_to_retrieve: Optional[List[str]] = None
    page: int = 0
    hits_per_page: int = 10

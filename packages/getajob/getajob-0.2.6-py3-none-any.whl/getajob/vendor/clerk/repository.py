import requests
from requests import Response
from pydantic import BaseModel

from .exceptions import UserNotFoundException, CompanyNotFoundException
from .companies.models import ClerkCompany
from .users.models import ClerkUser
from .recruiter_invitation.models import ClerkCompanyInvitation
from .recruiters.models import ClerkCompanyMembership


class ClerkAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.clerk.dev"

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _make_request(
        self, method: str, endpoint: str, payload: dict | None = None
    ) -> Response:
        url = self.base_url + endpoint
        request = {"method": method, "url": url, "headers": self._get_headers()}
        if payload:
            request["json"] = payload
        response = requests.request(**request, timeout=10)
        return response

    def _format_response_to_model(self, response: Response, model: BaseModel):
        response_json = response.json()
        if "data" in response_json:
            response_json = response_json["data"]
        if isinstance(response_json, list):
            return [model(**item) for item in response_json]
        return model(**response_json)

    def get_user(self, user_id: str):
        endpoint = f"/v1/users/{user_id}"
        res = self._make_request("GET", endpoint)
        if res.status_code == 404:
            raise UserNotFoundException()
        return self._format_response_to_model(res, ClerkUser)

    def get_company(self, company_id: str):
        endpoint = f"/v1/organizations/{company_id}"
        res = self._make_request("GET", endpoint)
        if res.status_code == 404:
            raise CompanyNotFoundException()
        return self._format_response_to_model(res, ClerkCompany)

    def get_company_invitations(self, company_id: str):
        endpoint = f"/v1/organizations/{company_id}/invitations/pending"
        res = self._make_request("GET", endpoint)
        return self._format_response_to_model(res, ClerkCompanyInvitation)

    def get_company_recruiters(self, company_id):
        endpoint = f"/v1/organizations/{company_id}/memberships"
        res = self._make_request("GET", endpoint)
        return self._format_response_to_model(res, ClerkCompanyMembership)

    def get_companies_by_user_id(self, user_id):
        endpoint = f"/v1/users/{user_id}/organization_memberships"
        res = self._make_request("GET", endpoint)
        return self._format_response_to_model(res, ClerkCompanyMembership)

    def get_all_users(self):
        endpoint = "/v1/users"
        res = self._make_request("GET", endpoint)
        return self._format_response_to_model(res, ClerkUser)

    def get_all_companies(self):
        endpoint = "/v1/organizations"
        res = self._make_request("GET", endpoint)
        return self._format_response_to_model(res, ClerkCompany)

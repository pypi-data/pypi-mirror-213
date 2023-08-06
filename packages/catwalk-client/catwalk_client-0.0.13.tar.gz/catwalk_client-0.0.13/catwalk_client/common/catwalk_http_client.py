from os import environ
from json import loads

from urllib.request import Request

from ._http_client import HTTPClient
from .constants import (
    CATWALK_AUTH_HEADER,
    CATWALK_USER_AGENT_HEADER_VALUE,
    CATWALK_CLIENT_LOCATION,
)


class CatwalkHTTPClient(HTTPClient):
    def __init__(
        self,
        catwalk_url: str,
        auth_token: str,
        insecure: bool = True,
        timeout: int = 30,
        timezone: str = "UTC",
    ):
        super().__init__(
            catwalk_url or environ.get("CATWALK_URL"),
            auth_token or environ.get("CATWALK_AUTH_TOKEN"),
            insecure,
            timeout,
        )

        self.timezone = timezone

    def _apply_headers(self, request: Request):
        self._add_client_location_header(request)
        self._add_auth_token_header(request, self.auth_token)
        self._add_user_agent_header(request, CATWALK_USER_AGENT_HEADER_VALUE)

    def _add_auth_token_header(self, request: Request, header_value: str = ""):
        request.add_header(CATWALK_AUTH_HEADER, f"Bearer {header_value}")

    def _add_client_location_header(self, request: Request):
        request.add_header(CATWALK_CLIENT_LOCATION, self.timezone)

    def fetch_auth_token(self, email: str, password: str) -> str:
        response, success = self.post(
            "/api/auth/login", {"email": email, "password": password}
        )

        if not success:
            raise Exception(response)

        return loads(response)["token"]

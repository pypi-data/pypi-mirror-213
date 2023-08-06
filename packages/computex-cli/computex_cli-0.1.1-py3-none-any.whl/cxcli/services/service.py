from ..config import Config

from requests import Response, request


class CoreApiService:
    base_path: str = None

    def __init__(
        self,
        host: str = None,
        scheme: str = None,
        access_token: str = None,
        refresh_token: str = None,
    ):
        config = Config()
        self.host = host or config.core_api_host
        self.scheme = scheme or config.core_api_scheme
        self.access_token = access_token or config.core_api_access_token
        self.refresh_token = refresh_token or config.core_api_refresh_token

    def _request(
        self,
        http_method: str,
        path: str,
        headers: dict = None,
        authenticate: bool = True,
        **kwargs,
    ):
        full_path = self.base_path and f"{self.base_path}{path}" or path
        url = f"{self.scheme}://{self.host}{full_path}"
        _headers = {}
        if authenticate:
            _headers["Authorization"] = f"Bearer {self.access_token}"
        if headers:
            _headers.update(headers)
        return request(http_method, url, headers=_headers, **kwargs)

    def _get(
        self,
        path: str,
        headers: dict = None,
        authenticate: bool = True,
        **kwargs,
    ) -> Response:
        return self._request(
            "GET", path, headers=headers, authenticate=authenticate, **kwargs
        )

    def _delete(
        self,
        path: str,
        headers: dict = None,
        authenticate: bool = True,
        **kwargs,
    ) -> Response:
        return self._request(
            "DELETE", path, headers=headers, authenticate=authenticate, **kwargs
        )

    def _post(
        self,
        path: str,
        headers: dict = None,
        authenticate: bool = True,
        **kwargs,
    ) -> Response:
        return self._request(
            "POST", path, headers=headers, authenticate=authenticate, **kwargs
        )

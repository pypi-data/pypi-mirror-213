from pydantic import BaseModel

from .service import CoreApiService


class RefreshRequest(BaseModel):
    token: str
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str


class AuthService(CoreApiService):
    base_path: str = "/auth"

    def refresh(
        self, access_token: str = None, refresh_token: str = None
    ) -> RefreshResponse:
        access_token = access_token or self.access_token
        refresh_token = refresh_token or self.refresh_token
        r = self._post(
            "/refresh",
            authenticate=False,
            json=RefreshRequest(token=access_token, refresh_token=refresh_token).dict(),
        )
        r.raise_for_status()
        j = r.json()
        self.access_token = j["token"]
        self.refresh_token = j["refresh_token"]
        return RefreshResponse(
            access_token=self.access_token, refresh_token=self.refresh_token
        )

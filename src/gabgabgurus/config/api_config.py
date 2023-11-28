from dataclasses import dataclass
from enum import Enum


class APIVersions(str, Enum):
    V1 = "v1"


@dataclass(slots=True, frozen=True)
class APIConfig:
    BASE_URL_PREFIX = "api"
    OPENAPI_URL_PREFIX = "openapi"
    SWAGGER_URL_PREFIX = "swagger"
    REDOC_URL_PREFIX = "redoc"

    def get_open_api_url(self, api_version: str | None = None) -> str:
        url = f"/{self.openapi_path}"
        if api_version:
            return f"{url}?version={api_version}"
        return url

    @property
    def base_path(self) -> str:
        return self.BASE_URL_PREFIX

    @property
    def openapi_path(self) -> str:
        return f"{self.base_path}/{self.OPENAPI_URL_PREFIX}"

    @property
    def swagger_path(self) -> str:
        return f"{self.openapi_path}/{self.SWAGGER_URL_PREFIX}"

    @property
    def redoc_path(self) -> str:
        return f"{self.openapi_path}/{self.REDOC_URL_PREFIX}"


api_config = APIConfig()

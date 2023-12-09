# import pytest
#
# from gabgabgurus.config.api_config import APIConfig, api_config
#
# pytestmark = pytest.mark.unit
#
#
# class TestAPIConfig:
#     def test_base_path(self):
#         expected = APIConfig.BASE_URL_PREFIX
#
#         actual = api_config.base_path
#
#         assert actual == expected
#
#     def test_openapi_path(self):
#         expected = f"{APIConfig.BASE_URL_PREFIX}/{APIConfig.OPENAPI_URL_PREFIX}"
#
#         actual = api_config.openapi_path
#
#         assert actual == expected
#
#     def test_swagger_path(self):
#         expected = (
#             f"{APIConfig.BASE_URL_PREFIX}/{APIConfig.OPENAPI_URL_PREFIX}/{APIConfig.SWAGGER_URL_PREFIX}"
#         )
#
#         actual = api_config.swagger_path
#
#         assert actual == expected
#
#     def test_redoc_path(self):
#         expected = f"{APIConfig.BASE_URL_PREFIX}/
#         {APIConfig.OPENAPI_URL_PREFIX}/{APIConfig.REDOC_URL_PREFIX}"
#
#         actual = api_config.redoc_path
#
#         assert actual == expected
#
#     @pytest.mark.parametrize("api_version", ["v1", "v2", None])
#     def test_get_open_api_url(self, api_version):
#         if api_version:
#             expected = f"/{APIConfig.BASE_URL_PREFIX}/{APIConfig.OPENAPI_URL_PREFIX}?version={api_version}"
#         else:
#             expected = f"/{APIConfig.BASE_URL_PREFIX}/{APIConfig.OPENAPI_URL_PREFIX}"
#
#         actual = api_config.get_open_api_url(api_version=api_version)
#
#         assert actual == expected

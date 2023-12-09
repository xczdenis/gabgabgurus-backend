import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent


class BaseSettingsConfigMixin(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class TestSettings(BaseSettingsConfigMixin):
    UNIT_TESTS_FOLDER_NAME: str = "unit"
    INTEGRATION_TESTS_FOLDER_NAME: str = "integration"
    UNIT_TESTS_DIR: str = os.path.join(BASE_DIR, UNIT_TESTS_FOLDER_NAME)
    INTEGRATION_TESTS_DIR: str = os.path.join(BASE_DIR, INTEGRATION_TESTS_FOLDER_NAME)
    PREFIX_FOR_FAKE_OBJECTS: str = "test"


test_settings: TestSettings = TestSettings()

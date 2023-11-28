from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR.parent
ROOT_DIR = SRC_DIR.parent


class BaseConfigMixin(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")


class AppConfig(BaseConfigMixin):
    ENVIRONMENT: str = "production"
    SECRET_KEY: str
    ALLOWED_HOSTS: str
    CSRF_TRUSTED_ORIGINS: str
    CORS_ALLOWED_ORIGINS: str
    SUPERUSER_LOGIN: str
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str
    BATCH_SIZE_FOR_BULK_ACTION: int = 10000

    def get_allowed_hosts(self) -> list[str]:
        return [host.strip() for host in self.ALLOWED_HOSTS.split(",")]

    def get_csrf_trusted_origin_hosts(self) -> list[str]:
        return [host.strip() for host in self.CSRF_TRUSTED_ORIGINS.split(",")]

    def get_cors_allowed_origin_hosts(self) -> list[str]:
        return [host.strip() for host in self.CORS_ALLOWED_ORIGINS.split(",")]


class PGConfig(BaseConfigMixin):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int


class RedisConfig(BaseConfigMixin):
    REDIS_HOST: str
    REDIS_PORT: int


class JWTConfig(BaseConfigMixin):
    JWT_SIGNING_KEY: str = ""
    ACCESS_TOKEN_LIFETIME_MINUTES: int = 5
    REFRESH_TOKEN_LIFETIME_DAYS: int = 1


class OAuth2Config(BaseConfigMixin):
    REDIRECT_URI: str


app_config: AppConfig = AppConfig()
pg_config: PGConfig = PGConfig()
redis_config: RedisConfig = RedisConfig()
jwt_config: JWTConfig = JWTConfig()
oauth2_config: OAuth2Config = OAuth2Config()

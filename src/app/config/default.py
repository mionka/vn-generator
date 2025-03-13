from pydantic_settings import BaseSettings, SettingsConfigDict


class DefaultSettings(BaseSettings):
    ENV: str = "local"
    PATH_PREFIX: str = "/api/v1"
    APP_HOST: str = "http://127.0.0.1"
    APP_PORT: int = 8000

    POSTGRES_DB: str = "app_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "user"
    POSTGRES_PORT: int = 5432
    POSTGRES_PASSWORD: str = "1234"
    DB_CONNECT_RETRY: int = 20
    DB_POOL_SIZE: int = 15

    @property
    def database_settings(self) -> dict:
        return {
            "database": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
        }

    @property
    def database_uri(self) -> str:
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    @property
    def database_uri_sync(self) -> str:
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            **self.database_settings,
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

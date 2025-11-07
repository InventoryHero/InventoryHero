from pathlib import Path
from urllib import parse
from pydantic import BaseModel, PostgresDsn, field_validator
from abc import ABC, abstractmethod
from pydantic_settings import BaseSettings, SettingsConfigDict


class Provider(ABC):
    @property
    @abstractmethod
    def db_url(self) -> str: ...

    @property
    @abstractmethod
    def db_type(self) -> str: ...

    @property
    @abstractmethod
    def db_url_public(self) -> str: ...


class SQLiteProvider(Provider, BaseModel):
    data_dir: Path
    prefix: str = ""

    @field_validator("data_dir")
    @classmethod
    def ensure_dir(cls, v: Path):
        v.mkdir(parents=True, exist_ok=True)
        return v

    @property
    def db_path(self):
        return self.data_dir / f"{self.prefix}inventoryhero.db"

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_path.absolute()!s}"

    @property
    def db_url_public(self) -> str:
        return self.db_url

    @property
    def db_type(self) -> str:
        return 'SQLite'


class PostgresProvider(Provider, BaseSettings):

    IH_DB_HOST: str = "postgres"
    IH_DB_PASSWORD: str = "inventoryhero"
    IH_DB_USER: str = "inventoryhero"
    IH_DB_PORT: str = "5432"
    IH_DB_NAME: str = "inventoryhero"

    model_config = SettingsConfigDict(arbitrary_types_allowed=True, extra="allow")

    @property
    def db_type(self) -> str:
        return "Postgres"

    @property
    def db_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                username=self.IH_DB_USER,
                password=parse.quote(self.IH_DB_PASSWORD),
                host=f"{self.IH_DB_HOST}:{self.IH_DB_PORT}",
                path=f"{self.IH_DB_NAME or ''}",
            )
        )

    @property
    def db_url_public(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                username="***",
                password="***",
                host=f"{self.IH_DB_HOST}:{self.IH_DB_PORT}",
                path=f"{self.IH_DB_NAME or ''}",
            )
        )



def db_factory(provider: str, data_dir: Path, env_file: Path):
    if provider == "postgres":
        return PostgresProvider(_env_file=env_file, _env_file_encoding="utf-8")
    return SQLiteProvider(data_dir=data_dir)
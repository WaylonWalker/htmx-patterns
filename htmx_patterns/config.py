from datetime import datetime, timezone
from functools import lru_cache
import os
from typing import Optional
from urllib.parse import quote_plus

from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
import jinja2
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from sqlalchemy import create_engine
from sqlmodel import Session
from typing import TYPE_CHECKING

from htmx_patterns import models
from htmx_patterns.__about__ import __version__

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

__all__ = ["models"]

console = Console()

if hasattr(jinja2, "pass_context"):
    pass_context = jinja2.pass_context
else:
    pass_context = jinja2.contextfunction


class ApiServer(BaseModel):
    app: str = "htmx_patterns.app:app"
    port: int = 5000
    reload: bool = True
    log_level: str = "info"
    host: str = "0.0.0.0"
    workers: int = 1
    forwarded_allow_ips: str = "*"
    proxy_headers: bool = True


@pass_context
def url_for_query(context: dict, name: str, **params: dict) -> str:
    request = context["request"]
    url = str(request.url_for(name))

    from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

    # Parse the URL
    parsed_url = urlparse(url)

    # Parse the query parameters
    query_params = parse_qs(parsed_url.query)

    # Update the query parameters with the new ones
    query_params.update(params)

    # Rebuild the query string
    updated_query_string = urlencode(query_params, doseq=True)

    # Rebuild the URL with the updated query string
    updated_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            updated_query_string,
            parsed_url.fragment,
        )
    )

    if os.environ.get("ENV") in ["dev", "qa", "prod"]:
        updated_url = updated_url.replace("http", "https", 1)
    return updated_url


def get_templates(config: BaseSettings) -> Jinja2Templates:
    templates = Jinja2Templates(directory="templates")
    templates.env.filters["quote_plus"] = lambda u: quote_plus(str(u))
    templates.env.filters["timestamp"] = lambda u: datetime.fromtimestamp(
        u, tz=timezone.utc
    ).strftime("%B %d, %Y")
    templates.env.globals["url_for"] = url_for_query
    templates.env.globals["config"] = config
    console.print(f"Using environment: {os.environ.get('ENV')}")

    # if os.environ.get("ENV") in ["dev", "qa", "prod"]:
    #     templates.env.globals["url_for"] = https_url_for
    #     console.print("Using HTTPS")
    # else:
    #     console.print("Using HTTP")

    return templates


class Config(BaseSettings):
    env: str = "local"
    the_templates: Optional[Jinja2Templates] = Field(None, exclude=True)
    api_server: ApiServer = ApiServer()
    database_url: str = "sqlite:///database.db"
    app_version: str = __version__

    @property
    def templates(self) -> Jinja2Templates:
        if self.the_templates is None:
            self.the_templates = get_templates(self)
        return self.the_templates

    model_config = SettingsConfigDict(env_nested_delimiter="__")


class Database:
    def __init__(self, config: Config) -> None:
        self.config = config

        self.db_conf = {}
        if "sqlite" in self.config.database_url:
            self.db_conf = {
                "connect_args": {"check_same_thread": False},
                "pool_recycle": 3600,
                "pool_pre_ping": True,
            }

        # if os.environ.get("ENV") == "test":
        #     self._engine = create_engine(
        #         "sqlite://",
        #         connect_args={"check_same_thread": False},
        #         poolclass=StaticPool,
        #     )
        # else:
        self._engine = create_engine(self.config.database_url, **self.db_conf)

    @property
    def engine(self) -> "Engine":
        return self._engine

    @property
    def session(self) -> "Session":
        return Session(self.engine)


@lru_cache
def get_config(env: Optional[str] = None):
    if env is None:
        env = os.environ.get("ENV", "local")
    load_dotenv(dotenv_path=f".env.{env}")
    config = Config()

    return config


config = get_config()
database = Database(config)


def get_session() -> "Session":
    with Session(database.engine) as session:
        yield session

import os
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any, Optional
from urllib.parse import quote_plus

import jinja2
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console

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
def https_url_for(context: dict, name: str, **path_params: Any) -> str:
    request = context["request"]
    http_url = request.url_for(name, **path_params)
    return str(http_url).replace("http", "https", 1)


def get_templates(config: BaseSettings) -> Jinja2Templates:
    templates = Jinja2Templates(directory="templates")
    templates.env.filters["quote_plus"] = lambda u: quote_plus(str(u))
    templates.env.filters["timestamp"] = lambda u: datetime.fromtimestamp(
        u, tz=timezone.utc
    ).strftime("%B %d, %Y")
    templates.env.globals["https_url_for"] = https_url_for
    templates.env.globals["config"] = config
    console.print(f'Using environment: {os.environ.get("ENV")}')

    if os.environ.get("ENV") in ["dev", "qa", "prod"]:
        templates.env.globals["url_for"] = https_url_for
        console.print("Using HTTPS")
    else:
        console.print("Using HTTP")

    return templates


class Config(BaseSettings):
    env: str
    the_templates: Optional[Jinja2Templates] = Field(None, exclude=True)
    api_server: ApiServer = ApiServer()

    @property
    def templates(self) -> Jinja2Templates:
        if self.the_templates is None:
            self.the_templates = get_templates(self)
        return self.the_templates

    model_config = SettingsConfigDict(env_nested_delimiter="__")


@lru_cache
def get_config(env: Optional[str] = None):
    if env is None:
        env = os.environ.get("ENV", "local")
    load_dotenv(dotenv_path=f".env.{env}")
    config = Config()

    return config

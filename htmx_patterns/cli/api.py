import alembic
import typer
import uvicorn
from alembic.config import Config
from rich.console import Console

from htmx_patterns.config import get_config

api_app = typer.Typer()


@api_app.callback()
def api():
    "model cli"


@api_app.command()
def config(
    env: str = typer.Option(
        "local",
        help="the environment to use",
    ),
):
    config = get_config(env)
    Console().print(config)


@api_app.command()
def run(
    env: str = typer.Option(
        "local",
        help="the environment to use",
    ),
    alembic_revision: str = typer.Option(
        "head",
        help="the alembic revision to use",
    ),
):
    config = get_config(env)
    Console().print(config.api_server)
    Console().print(config.database_url)
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", config.database_url)
    alembic.command.upgrade(config=alembic_cfg, revision=alembic_revision)
    uvicorn.run(**config.api_server.dict())


if __name__ == "__main__":
    api_app()

import typer

from htmx_patterns.cli.api import api_app

app = typer.Typer()

app.add_typer(api_app, name="api")

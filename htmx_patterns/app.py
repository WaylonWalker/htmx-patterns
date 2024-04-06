from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse

from htmx_patterns.__about__ import __version__
from htmx_patterns.config import get_config
from htmx_patterns.infinite.router import infinite_router


def set_prefers(
    request: Request,
):
    hx_request_header = request.headers.get("hx-request")
    user_agent = request.headers.get("user-agent", "").lower()
    if hx_request_header:
        request.state.prefers_html = True
        request.state.prefers_partial = True
        request.state.prefers_json = False
    elif "mozilla" in user_agent or "webkit" in user_agent:
        request.state.prefers_html = True
        request.state.prefers_partial = False
        request.state.prefers_json = False
    else:
        request.state.prefers_html = False
        request.state.prefers_partial = False
        request.state.prefers_json = True


app = FastAPI(
    title="HTMX Patterns",
    version=__version__,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    dependencies=[Depends(set_prefers)],
)
config = get_config()

app.include_router(infinite_router)


@app.get("/")
async def read_main(request: Request):
    return config.templates.TemplateResponse("index.html", {"request": request})


@app.get("/favicon.ico")
async def favicon(request: Request):
    "use a proper static file server like nginx or apache in production"
    return FileResponse("templates/favicon.ico")


@app.get("/robots.txt")
async def robots(request: Request):
    "use a proper static file server like nginx or apache in production"
    return config.templates.TemplateResponse("robots.txt", {"request": request})


@app.get("/css")
async def app_css(request: Request):
    "use a proper static file server like nginx or apache in production"
    return FileResponse("templates/app.css")


@app.get("/htmx")
async def htmx(request: Request):
    "use a proper static file server like nginx or apache in production"
    return config.templates.TemplateResponse("htmx.js", {"request": request})

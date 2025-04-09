from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse

from htmx_patterns.__about__ import __version__
from htmx_patterns.boosted.router import boosted_router
from htmx_patterns.config import get_config
from htmx_patterns.infinite.router import infinite_router
from htmx_patterns.toast.router import toast_router
from htmx_patterns.websocket.router import websocket_router
from htmx_patterns.zpages.router import zpages_router


def set_prefers(
    request: Request = None,
):
    if request is None:
        return
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
app.include_router(boosted_router)
app.include_router(toast_router)
app.include_router(websocket_router)
app.include_router(zpages_router)


@app.get("/")
async def index(request: Request):
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


@app.get("/htmx.js")
async def htmx_js(request: Request):
    "use a proper static file server like nginx or apache in production"
    return config.templates.TemplateResponse("htmx.js", {"request": request})


@app.get("/ws.js")
async def ws_js(request: Request):
    "use a proper static file server like nginx or apache in production"
    return config.templates.TemplateResponse("ws.js", {"request": request})


@app.get("/tailwind.js")
async def tailwind_js(request: Request):
    "use a proper static file server like nginx or apache in production"
    return config.templates.TemplateResponse("tailwind.js", {"request": request})

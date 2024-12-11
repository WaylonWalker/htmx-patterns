from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse


from htmx_patterns.config import get_config

toast_router = APIRouter(prefix="/toast", tags=["toast"])

config = get_config()


@toast_router.get("/")
@toast_router.get("")
async def get_toast(
    request: Request,
):
    return config.templates.TemplateResponse(
        "toast/toast.html",
        {
            "request": request,
        },
    )


@toast_router.post("/")
@toast_router.post("")
async def post_toast(
    request: Request,
):
    return config.templates.TemplateResponse(
        "toast/toast-message.html",
        {
            "request": request,
            "message": "Submitted",
        },
    )


@toast_router.get("/null/")
@toast_router.get("/null")
@toast_router.delete("/null/")
@toast_router.delete("/null")
@toast_router.post("/null/")
@toast_router.post("/null")
async def null(
    request: Request,
):
    return PlainTextResponse("")

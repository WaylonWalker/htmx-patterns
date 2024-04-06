import asyncio
import time

from fastapi import APIRouter
from fastapi.requests import Request

boosted_router = APIRouter(prefix="/boosted", tags=["Shots Methods"])

from htmx_patterns.boosted.models import PersonFactory
from htmx_patterns.config import get_config

config = get_config()


@boosted_router.get("/")
@boosted_router.get("")
async def boosted(request: Request, id: int = 0):
    # simulate getting a person by id
    person = PersonFactory.build()

    if id > 0:
        prev_id = id - 1
        next_id = id + 1
    else:
        prev_id = None
        next_id = id + 1

    return config.templates.TemplateResponse(
        "boosted/person.html",
        {
            "request": request,
            "person": person,
            "person_id": id,
            "prev_id": prev_id,
            "next_id": next_id,
        },
    )

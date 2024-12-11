from typing import Annotated

from fastapi import APIRouter, Depends, Header
from fastapi.requests import Request
from sqlmodel import Session


from htmx_patterns.config import get_config, get_session
from htmx_patterns.models import Person

boosted_router = APIRouter(prefix="/boosted", tags=["Boosted"])

config = get_config()


@boosted_router.get("/")
@boosted_router.get("")
async def boosted(
    request: Request,
    id: int = 1,
    session: Session = Depends(get_session),
    user_agent: Annotated[str | None, Header()] = None,
):
    # person = PersonFactory.build()
    person = Person.get_by_id(session, id)

    if person is None:
        return config.templates.TemplateResponse(
            "boosted/person.html",
            {
                "request": request,
                "person": None,
                "person_id": id,
                "prev_id": None,
                "next_id": 1,
            },
        )

    if id > 1:
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

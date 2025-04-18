import asyncio

from fastapi import APIRouter
from fastapi.requests import Request

from htmx_patterns.config import get_config
from htmx_patterns.models import PersonFactory

infinite_router = APIRouter(prefix="/infinite", tags=["Infinite"])

config = get_config()


@infinite_router.get("/")
async def infinite(request: Request, page: int = 1, n: int = 10):
    # simulated last page
    if page == 5:
        return config.templates.TemplateResponse(
            "infinite/persons_partial.html", {"request": request, "persons": []}
        )

    persons = [PersonFactory.build() for _ in range(n)]

    if request.state.prefers_partial:
        await asyncio.sleep(1)
        return config.templates.TemplateResponse(
            "infinite/persons_partial.html",
            {
                "request": request,
                "persons": persons,
                "next_page": page + 1,
            },
        )

    return config.templates.TemplateResponse(
        "infinite/persons.html",
        {
            "request": request,
            "persons": persons,
            "next_page": page + 1,
        },
    )

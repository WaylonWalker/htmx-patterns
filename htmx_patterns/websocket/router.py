from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from htmx_patterns.websocket.dependencies import ConnectionManager

from htmx_patterns.config import get_config


websocket_router = APIRouter(prefix="/websocket", tags=["Websocket"])

manager = ConnectionManager()

config = get_config()


@websocket_router.get("/")
def websocket_index(request: Request):
    return config.templates.TemplateResponse(
        "websocket/index.html", {"request": request}
    )


@websocket_router.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket,
):
    await manager.connect(websocket)
    await manager.send_personal_message("Hello", websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Received:{data}", websocket)
            # import time
            #
            # time.sleep(1)
            # data = "hello"
            # await manager.send_personal_message(f"Received:{data}", websocket)
            #
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_personal_message("Bye!!!", websocket)

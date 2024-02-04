from fastapi import FastAPI, Request,HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from backend.routers.users import user_router
from backend.routers.chats import chat_router
from backend.database import EntityNotFoundException
app = FastAPI(
    title="Pony Express Chat",
    description="api for chatting",
    version="0.1.0")

app.include_router(user_router)
app.include_router(chat_router)
# added this default loading page to take to different documentations
@app.get("/", include_in_schema=False)
def default() -> str:
    return HTMLResponse(
        content=f"""
        <html>
            <body>
                <h1>{app.title}</h1>
                <p>{app.description}</p>
                <h2>API docs</h2>
                <ul>
                    <li><a href="/docs">Swagger</a></li>
                    <li><a href="/redoc">ReDoc</a></li>
                </ul>
            </body>
        </html>
        """,
    )



@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request,
    exception: EntityNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": {
                "type": "entity_not_found",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )

@app.exception_handler(HTTPException)
def handle_http_exception(request:Request,exception:HTTPException):
    return JSONResponse(status_code=exception.status_code,
                        content=exception.detail)



from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from routers.users import user_router
app = FastAPI(
    title="Pony Express Chat",
    description="api for chatting",
    version="0.1.0")

app.include_router(user_router)
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


if __name__=="__main__":
    import uvicorn
    uvicorn.run("backend.main:app",reload = True)


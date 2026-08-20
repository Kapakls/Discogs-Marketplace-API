from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from discogs_marketplace_api.routes.marketplace import (
    router as marketplace_router,
)

app = FastAPI()

app.include_router(
    marketplace_router,
    prefix="/marketplace",
)

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested endpoint does not exist.",
            "path": request.url.path,
        },
    )